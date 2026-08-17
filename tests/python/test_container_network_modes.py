from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import cast

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DEVCONTAINER_ROOT = REPO_ROOT / ".devcontainer"

WORKSPACE_FILES = {
    "bind": ["compose.bind.yaml"],
    "copy": ["compose.copy.yaml"],
}
PERSISTENCE_FILES = {
    "ephemeral": ["compose.ephemeral.yaml"],
    "persistent": ["compose.persist.yaml"],
}
NETWORK_FILES = {
    "direct": ["compose.direct.yaml"],
    "proxy-ephemeral": ["compose.proxy.yaml", "compose.proxy-ephemeral.yaml"],
    "proxy-persistent": ["compose.proxy.yaml", "compose.proxy-persist.yaml"],
}


def docker_compose_available() -> bool:
    if shutil.which("docker") is None:
        return False
    return (
        subprocess.run(
            ["docker", "compose", "version"],
            check=False,
            capture_output=True,
        ).returncode
        == 0
    )


def compose_config(*files: str) -> dict[str, object]:
    command = ["docker", "compose", "--env-file", ".env.example"]
    for file in files:
        command.extend(("-f", file))
    command.extend(("config", "--format", "json"))

    environment = os.environ.copy()
    environment["COMPOSE_PROJECT_NAME"] = "programming-lab-network-mode-test"
    environment["V2RAYA_HTTP_PROXY"] = "http://127.0.0.1:20171"
    environment["V2RAYA_SOCKS_PROXY"] = "socks5h://127.0.0.1:20170"
    environment["V2RAYA_NO_PROXY"] = "localhost,127.0.0.1,::1"
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    value: dict[str, object] = json.loads(result.stdout)
    return value


@pytest.mark.skipif(not docker_compose_available(), reason="Docker Compose is unavailable")
@pytest.mark.parametrize("workspace", ["bind", "copy"])
@pytest.mark.parametrize("persistence", ["ephemeral", "persistent"])
def test_direct_mode_has_no_proxy_service_or_endpoint(workspace: str, persistence: str) -> None:
    files = [
        "compose.yaml",
        "compose.gpu-legacy.yaml",
        *WORKSPACE_FILES[workspace],
        *PERSISTENCE_FILES[persistence],
    ]
    if workspace == "copy" and persistence == "persistent":
        files.append("compose.copy-persist.yaml")
    files.extend(NETWORK_FILES["direct"])

    config = compose_config(*files)
    services_value = config["services"]
    assert isinstance(services_value, dict)
    services = cast(dict[str, object], services_value)
    assert set(services) == {"dev"}

    serialized = json.dumps(config)
    assert "127.0.0.1:20171" not in serialized
    assert "127.0.0.1:20170" not in serialized

    dev_value = services["dev"]
    assert isinstance(dev_value, dict)
    dev = cast(dict[str, object], dev_value)
    environment_value = dev["environment"]
    assert isinstance(environment_value, dict)
    environment = cast(dict[str, object], environment_value)
    assert environment["PROGRAMMING_LAB_PROXY_MODE"] == "direct"
    for name in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "NO_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
        "no_proxy",
    ):
        assert environment[name] == ""


@pytest.mark.skipif(not docker_compose_available(), reason="Docker Compose is unavailable")
@pytest.mark.parametrize("persistence", ["ephemeral", "persistent"])
def test_proxy_mode_includes_sidecar_and_endpoints(persistence: str) -> None:
    config = compose_config(
        "compose.yaml",
        "compose.gpu-legacy.yaml",
        "compose.bind.yaml",
        *PERSISTENCE_FILES[persistence],
        *NETWORK_FILES[f"proxy-{persistence}"],
    )
    services_value = config["services"]
    assert isinstance(services_value, dict)
    services = cast(dict[str, object], services_value)
    assert set(services) == {"dev", "proxy"}

    dev_value = services["dev"]
    assert isinstance(dev_value, dict)
    dev = cast(dict[str, object], dev_value)
    environment_value = dev["environment"]
    assert isinstance(environment_value, dict)
    environment = cast(dict[str, object], environment_value)
    assert environment["PROGRAMMING_LAB_PROXY_MODE"] == "proxy"
    assert environment["V2RAYA_HTTP_PROXY"] == "http://127.0.0.1:20171"
    assert environment["V2RAYA_SOCKS_PROXY"] == "socks5h://127.0.0.1:20170"
    expected_proxy_environment = {
        "HTTP_PROXY": "http://127.0.0.1:20171",
        "HTTPS_PROXY": "http://127.0.0.1:20171",
        "ALL_PROXY": "socks5h://127.0.0.1:20170",
        "NO_PROXY": "localhost,127.0.0.1,::1",
        "http_proxy": "http://127.0.0.1:20171",
        "https_proxy": "http://127.0.0.1:20171",
        "all_proxy": "socks5h://127.0.0.1:20170",
        "no_proxy": "localhost,127.0.0.1,::1",
    }
    for name, expected in expected_proxy_environment.items():
        assert environment[name] == expected


def test_devcontainer_network_variants_are_explicit() -> None:
    definitions = sorted(DEVCONTAINER_ROOT.glob("*/devcontainer.json"))
    assert len(definitions) == 8

    for definition in definitions:
        value = cast(dict[str, object], json.loads(definition.read_text(encoding="utf-8")))
        name = value["name"]
        files = value["dockerComposeFile"]
        services = value["runServices"]
        assert isinstance(name, str)
        assert isinstance(files, list)
        assert isinstance(services, list)
        if name.endswith(" + direct"):
            assert "../../compose.direct.yaml" in files
            assert services == ["dev"]
            assert "remoteEnv" not in value
        else:
            assert name.endswith(" + proxy")
            assert "../../compose.proxy.yaml" in files
            assert services == ["dev", "proxy"]
            assert "remoteEnv" not in value
