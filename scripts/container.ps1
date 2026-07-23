[CmdletBinding()]
# Keep this script's external behavior in sync with scripts/container.sh.
param(
    [Parameter(Position = 0)]
    [string] $Action,

    [Parameter(Position = 1)]
    [string] $WorkspaceMode,

    [Parameter(Position = 2)]
    [string] $PersistenceMode,

    [Parameter(Position = 3)]
    [string] $ExportDirectory = "container-export",

    [Parameter(Position = 4, ValueFromRemainingArguments = $true)]
    [string[]] $RemainingArguments
)

Set-StrictMode -Version 3.0
$ErrorActionPreference = "Stop"
$script:LastDockerExitCode = 0
$script:RequestedExitCode = 0

function Get-Usage {
    @'
Usage:
  powershell -ExecutionPolicy Bypass -File scripts/container.ps1 <action> <workspace> <persistence> [export-dir]
  pwsh -File scripts/container.ps1 <action> <workspace> <persistence> [export-dir]

Workspace modes:
  bind          Bind-mount the host repository to /workspace (two-way sync).
  copy          Copy a repository snapshot into the image (no host sync).

Persistence modes:
  persistent    Keep CMake/Cargo build trees, tool caches/venvs, and v2rayA
                configuration in named volumes. In copy mode, also keep
                /workspace in a named volume seeded once from the image.
  ephemeral     Keep CMake/Cargo build trees and v2rayA configuration in
                tmpfs; other generated environments/caches stay in the
                container writable layer, and image-baked tools remain in the
                image.

Compose versions:
  2.30+         Add compose.gpu.yaml with its gpus: all declaration.
  2.27-2.29     Add compose.gpu-legacy.yaml with a GPU device reservation.

Actions:
  build         Build the selected image target.
  up            Build if needed and start in the background.
  status        Show service status.
  logs          Follow recent dev and proxy service logs.
  shell         Open an interactive Bash shell in the running container.
  init          Run scripts/init-env.sh in the running container.
  stop          Stop without removing the container.
  down          Remove the container; named volumes are retained.
  destroy       Remove the container and selected named volumes.
  config        Print the fully merged Compose configuration.
  export        Copy /workspace from copy mode to export-dir (default:
                ./container-export).

Examples:
  powershell -ExecutionPolicy Bypass -File scripts/container.ps1 up bind persistent
  powershell -ExecutionPolicy Bypass -File scripts/container.ps1 up copy ephemeral
  powershell -ExecutionPolicy Bypass -File scripts/container.ps1 export copy persistent ./container-export
'@
}

function Get-ComposeVersion {
    if ($null -eq (Get-Command -Name "docker" -ErrorAction SilentlyContinue)) {
        throw "Docker is not installed or is not available on PATH."
    }

    $versionOutputLines = & docker compose version --short 2>$null
    $versionExitCode = $LASTEXITCODE

    if ($versionExitCode -ne 0) {
        $versionOutputLines = & docker compose version 2>$null
        $versionExitCode = $LASTEXITCODE
    }

    if ($versionExitCode -ne 0) {
        throw "Docker Compose v2 is not installed or is not available."
    }

    $versionOutput = ($versionOutputLines -join [Environment]::NewLine).Trim()
    $versionMatch = [regex]::Match(
        $versionOutput,
        '(?<major>\d+)\.(?<minor>\d+)(?:\.(?<patch>\d+))?'
    )
    if (-not $versionMatch.Success) {
        throw "Unable to parse Docker Compose version from: $versionOutput"
    }

    $patch = if ($versionMatch.Groups["patch"].Success) {
        $versionMatch.Groups["patch"].Value
    } else {
        "0"
    }

    [version] (
        "{0}.{1}.{2}" -f
        $versionMatch.Groups["major"].Value,
        $versionMatch.Groups["minor"].Value,
        $patch
    )
}

function Invoke-DockerCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string[]] $Arguments
    )

    & docker @Arguments
    if ($LASTEXITCODE -ne 0) {
        $script:LastDockerExitCode = $LASTEXITCODE
        throw "Docker command failed with exit code $LASTEXITCODE."
    }
}

$usage = Get-Usage
if ($null -ne $RemainingArguments -and $RemainingArguments.Count -gt 0) {
    [Console]::Error.WriteLine($usage)
    exit 2
}
if (
    [string]::IsNullOrEmpty($Action) -or
    @("help", "-h", "--help") -ccontains $Action
) {
    [Console]::Out.WriteLine($usage)
    exit 0
}

$validActions = @(
    "build", "up", "status", "logs", "shell", "init",
    "stop", "down", "destroy", "config", "export"
)
if ($validActions -cnotcontains $Action) {
    [Console]::Error.WriteLine($usage)
    exit 2
}
if (@("bind", "copy") -cnotcontains $WorkspaceMode) {
    [Console]::Error.WriteLine($usage)
    exit 2
}
if (@("persistent", "ephemeral") -cnotcontains $PersistenceMode) {
    [Console]::Error.WriteLine($usage)
    exit 2
}
if ([string]::IsNullOrEmpty($ExportDirectory)) {
    $ExportDirectory = "container-export"
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$locationPushed = $false
$exitCode = 0

try {
    Push-Location -Path $repoRoot
    $locationPushed = $true

    $composeVersion = Get-ComposeVersion
    $minimumComposeVersion = [version] "2.27.0"
    $modernGpuSyntaxVersion = [version] "2.30.0"

    if ($composeVersion -lt $minimumComposeVersion) {
        throw (
            "Docker Compose {0} is too old; version {1} or later is required." -f
            $composeVersion.ToString(3),
            $minimumComposeVersion.ToString(3)
        )
    }

    $gpuComposeFile = if ($composeVersion -ge $modernGpuSyntaxVersion) {
        "compose.gpu.yaml"
    } else {
        "compose.gpu-legacy.yaml"
    }
    [Console]::Error.WriteLine(
        (
            "Docker Compose {0} detected; using {1}." -f
            $composeVersion.ToString(3),
            $gpuComposeFile
        )
    )

    $composeArguments = @(
        "compose",
        "-f", "compose.yaml",
        "-f", $gpuComposeFile
    )
    if ($WorkspaceMode -ceq "bind") {
        $composeArguments += @("-f", "compose.bind.yaml")
    } else {
        $composeArguments += @("-f", "compose.copy.yaml")
    }

    if ($PersistenceMode -ceq "persistent") {
        $composeArguments += @("-f", "compose.persist.yaml")
        if ($WorkspaceMode -ceq "copy") {
            $composeArguments += @("-f", "compose.copy-persist.yaml")
        }
    } else {
        $composeArguments += @("-f", "compose.ephemeral.yaml")
    }

    switch -CaseSensitive ($Action) {
        "build" {
            Invoke-DockerCommand ($composeArguments + @("build"))
        }
        "up" {
            if ($WorkspaceMode -ceq "copy" -and $PersistenceMode -ceq "persistent") {
                Write-Output "Note: an existing workspace-data volume is not overwritten by a rebuilt image."
            }
            Invoke-DockerCommand ($composeArguments + @("up", "-d", "--build"))
        }
        "status" {
            Invoke-DockerCommand ($composeArguments + @("ps"))
        }
        "logs" {
            Invoke-DockerCommand ($composeArguments + @("logs", "--tail=200", "--follow"))
        }
        "shell" {
            Invoke-DockerCommand ($composeArguments + @("exec", "dev", "bash"))
        }
        "init" {
            Invoke-DockerCommand (
                $composeArguments + @("exec", "dev", "bash", "scripts/init-env.sh")
            )
        }
        "stop" {
            Invoke-DockerCommand ($composeArguments + @("stop"))
        }
        "down" {
            if ($WorkspaceMode -ceq "copy" -and $PersistenceMode -ceq "ephemeral") {
                [Console]::Error.WriteLine(
                    "Warning: removing this container discards changes made to its copied workspace."
                )
                [Console]::Error.WriteLine(
                    "Use the export action first if those changes are needed on the host."
                )
            }
            Invoke-DockerCommand ($composeArguments + @("down", "--remove-orphans"))
        }
        "destroy" {
            [Console]::Error.WriteLine(
                "Removing the container and all named volumes selected by this configuration..."
            )
            Invoke-DockerCommand (
                $composeArguments + @("down", "--volumes", "--remove-orphans")
            )
        }
        "config" {
            Invoke-DockerCommand ($composeArguments + @("config"))
        }
        "export" {
            if ($WorkspaceMode -cne "copy") {
                $script:RequestedExitCode = 2
                throw "The export action is only meaningful in copy workspace mode."
            }
            New-Item -ItemType Directory -Force -Path $ExportDirectory | Out-Null
            Invoke-DockerCommand (
                $composeArguments + @("cp", "dev:/workspace/.", $ExportDirectory)
            )
            Write-Output "Workspace exported to: $ExportDirectory"
        }
    }
} catch {
    if ($script:LastDockerExitCode -eq 0) {
        [Console]::Error.WriteLine($_.Exception.Message)
    }
    $exitCode = if ($script:LastDockerExitCode -ne 0) {
        $script:LastDockerExitCode
    } elseif ($script:RequestedExitCode -ne 0) {
        $script:RequestedExitCode
    } else {
        1
    }
} finally {
    if ($locationPushed) {
        Pop-Location
    }
}

exit $exitCode
