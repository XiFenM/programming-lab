#!/usr/bin/env bash
# Shared implementation for the two host entry points. Sourcing defines functions only.

host_configure() {
  host_profile="$1"
  repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
  case "${host_profile}" in
    cpu)
      route_name=host-cpu
      venv_path="${repo_root}/.venv"
      host_build_jobs="${HOST_CPU_BUILD_JOBS:-2}"
      ;;
    gpu)
      route_name=host-gpu
      venv_path="${repo_root}/.venv-host-gpu"
      host_build_jobs="${HOST_GPU_BUILD_JOBS:-2}"
      ;;
    *) printf 'Unsupported host profile: %s\n' "${host_profile}" >&2; return 2 ;;
  esac
  [[ "${host_build_jobs}" =~ ^[1-9][0-9]*$ ]] || \
    fail "HOST_${host_profile^^}_BUILD_JOBS must be a positive integer"

  host_cache="${repo_root}/.cache/${route_name}"
  downloads_dir="${host_cache}/downloads"
  uv_bin_dir="${HOME}/.local/bin"
  rustup_version=1.29.0
  rust_toolchain=1.97.1
  nvm_version=0.40.3

  # Select system compilers and user-installed language managers even when invoked
  # from an activated environment. Do not change the user's shell startup files.
  unset CC CXX CPP CFLAGS CXXFLAGS LDFLAGS LIBRARY_PATH LD_LIBRARY_PATH LD_PRELOAD \
    CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH PKG_CONFIG_PATH CMAKE_PREFIX_PATH \
    CMAKE_TOOLCHAIN_FILE CONDA_PREFIX CONDA_DEFAULT_ENV BASH_ENV ENV PROMPT_COMMAND \
    PYTHONHOME PYTHONPATH PYTHONUSERBASE VIRTUAL_ENV \
    RUSTC RUSTC_WRAPPER RUSTC_WORKSPACE_WRAPPER RUSTDOC RUSTDOCFLAGS RUSTFLAGS \
    CARGO_BUILD_RUSTC CARGO_BUILD_RUSTC_WRAPPER CARGO_BUILD_RUSTDOC CARGO_BUILD_TARGET \
    CARGO_CONFIG CARGO_ENCODED_RUSTFLAGS MAKEFLAGS MFLAGS CCACHE_CONFIGPATH \
    UV_ACTIVE UV_CONFIG_FILE UV_DEFAULT_GROUPS UV_ENV_FILE UV_EXTRA_INDEX_URL \
    UV_FROZEN UV_GROUP UV_INDEX UV_INDEX_URL UV_LOCKED UV_MANAGED_PYTHON UV_NO_CONFIG \
    UV_NO_DEFAULT_GROUPS UV_NO_DEV UV_NO_ENV_FILE UV_NO_GROUP UV_NO_MANAGED_PYTHON \
    UV_NO_SYNC UV_OFFLINE UV_ONLY_GROUP UV_PROJECT UV_PYTHON UV_PYTHON_DOWNLOADS \
    UV_WORKING_DIR NPM_CONFIG_PREFIX npm_config_prefix PREFIX
  export PATH="/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/sbin:/usr/local/bin"
  export CC=/usr/bin/gcc CXX=/usr/bin/g++
  export CARGO_HOME="${HOME}/.cargo" RUSTUP_HOME="${HOME}/.rustup"
  export RUSTUP_TOOLCHAIN="${rust_toolchain}"
  export NVM_DIR="${HOME}/.nvm"
  export UV_PROJECT_ENVIRONMENT="${venv_path}"
  export UV_PYTHON_INSTALL_DIR="${HOME}/.local/share/uv/python"
  export UV_PYTHON_BIN_DIR="${uv_bin_dir}"
  export UV_PYTHON_PREFERENCE=only-managed PYTHONNOUSERSITE=1
  export UV_CACHE_DIR="${HOME}/.cache/uv"
  export CARGO_TARGET_DIR="${repo_root}/target/${route_name}"
  export CARGO_BUILD_JOBS="${host_build_jobs}"
  export CCACHE_DIR="${host_cache}/ccache"
  export CCACHE_TEMPDIR="${CCACHE_DIR}/tmp"
  export PRE_COMMIT_HOME="${host_cache}/pre-commit" RUFF_CACHE_DIR="${host_cache}/ruff"
  export HISTFILE="${host_cache}/bash_history"
  export CUDA_CACHE_PATH="${host_cache}/nv/ComputeCache"
  export TILELANG_CACHE_DIR="${host_cache}/tilelang"
  export TORCH_EXTENSIONS_DIR="${host_cache}/torch-extensions"
  export TRITON_CACHE_DIR="${host_cache}/triton"
  export PROGRAMMING_LAB_HOST_PROFILE="${host_profile}"
  if [[ "${host_profile}" == cpu ]]; then
    unset CUDA_HOME CUDA_PATH CUDACXX CUDAHOSTCXX
    export UV_CONCURRENT_DOWNLOADS="${HOST_CPU_UV_CONCURRENT_DOWNLOADS:-2}"
    export CCACHE_MAXSIZE="${HOST_CPU_CCACHE_MAXSIZE:-1G}"
    export RUSTUP_DIST_SERVER="${HOST_CPU_RUSTUP_DIST_SERVER:-https://static.rust-lang.org}"
    export RUSTUP_UPDATE_ROOT="${HOST_CPU_RUSTUP_UPDATE_ROOT:-https://static.rust-lang.org/rustup}"
  else
    host_select_cuda
    export UV_CONCURRENT_DOWNLOADS="${HOST_GPU_UV_CONCURRENT_DOWNLOADS:-2}"
    export CCACHE_MAXSIZE="${HOST_GPU_CCACHE_MAXSIZE:-4G}"
    export RUSTUP_DIST_SERVER="${HOST_GPU_RUSTUP_DIST_SERVER:-https://static.rust-lang.org}"
    export RUSTUP_UPDATE_ROOT="${HOST_GPU_RUSTUP_UPDATE_ROOT:-https://static.rust-lang.org/rustup}"
  fi
  export PATH="${venv_path}/bin:${CARGO_HOME}/bin:${uv_bin_dir}:${PATH}"
  cd "${repo_root}" || fail "cannot enter ${repo_root}"
}

fail() {
  printf '%s: %s\n' "${route_name:-host}" "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "required command is missing: $1; run ${route_name}.sh init"
}

host_usage() {
  cat <<EOF
Usage: bash scripts/${route_name}.sh <command> [arguments]

Commands:
  init            Install APT tools, uv/Python 3.12, Rust ${rust_toolchain}, nvm/Node 24 and dependencies.
  init --skip-apt  Initialize user tools/dependencies after system packages were installed separately.
  install-system  Install system packages via APT (root or sudo required).
  doctor          Check system tools, managed Python, Rust, Node and dependencies.
  build           Configure and build the ${route_name} CMake preset.
  test            Run Python, C++ and Rust tests (plus native CUDA for the GPU route).
  lint            Run the route's format, lint and type checks.
  verify          Verify the environment without checking exercise code.
  shell           Open a shell with the host tools and project venv active.
  run -- CMD      Run a command with the host tools and project venv active.

System: Ubuntu 22.04/24.04 x86_64; init changes system APT packages and user tool directories.
APT sources: init/install-system show sources, measure download speeds, then ask keep/official/tuna.
For automation, explicitly set HOST_APT_SOURCE=keep|official|tuna. init --skip-apt skips this step.
Set HOST_APT_SPEED_TEST=0 to skip the download measurements (enabled by default).
EOF
  if [[ "${host_profile}" == gpu ]]; then
    echo 'GPU: reuses CUDA 12/13 and cuDNN 9; installs missing components without patch pins.'
    echo 'Set HOST_GPU_CUDA_HOME for a custom toolkit; verify includes PyTorch/Triton/TileLang GPU verification.'
  else
    echo 'CPU: doctor checks absence of GPU Python packages; CUDA and cuDNN are not installed.'
  fi
}

host_check_platform() {
  [[ "$(uname -s)-$(uname -m)" == Linux-x86_64 ]] || fail 'requires Linux x86_64'
  # shellcheck source=/dev/null
  . /etc/os-release
  [[ "${ID:-}" == ubuntu ]] || fail 'APT bootstrap supports Ubuntu 22.04 and 24.04 only'
  case "${VERSION_ID:-}" in
    22.04) ubuntu_codename=jammy; cuda_distro=ubuntu2204 ;;
    24.04) ubuntu_codename=noble; cuda_distro=ubuntu2404 ;;
    *) fail 'APT bootstrap supports Ubuntu 22.04 and 24.04 only' ;;
  esac
}

host_select_cuda() {
  local candidate compiler selected="${HOST_GPU_CUDA_HOME:-}"
  local -a candidates=()
  if [[ -z "${selected}" ]]; then
    mapfile -t candidates < <(printf '%s\n' /usr/local/cuda-* | sort -Vr)
    for candidate in /usr/local/cuda "${candidates[@]}"; do
      if [[ -x "${candidate}/bin/nvcc" ]]; then selected="${candidate}"; break; fi
    done
    if [[ -z "${selected}" ]] && compiler="$(command -v nvcc)"; then
      compiler="$(realpath -e "${compiler}")"
      selected="$(dirname "$(dirname "${compiler}")")"
    fi
  fi
  selected="${selected:-/usr/local/cuda}"
  if [[ -d "${selected}" ]]; then selected="$(realpath -e "${selected}")"; fi
  export CUDA_HOME="${selected}" CUDA_PATH="${selected}" CUDACXX="${selected}/bin/nvcc"
  export CUDAHOSTCXX="${CXX}" PATH="${selected}/bin:${PATH}"
}

host_cuda_release() {
  [[ -x "${CUDACXX}" ]] || return 1
  "${CUDACXX}" --version | sed -n 's/.*release \([0-9][0-9]*\.[0-9][0-9]*\).*/\1/p'
}

host_cuda_ready() {
  local release
  release="$(host_cuda_release)" || return 1
  [[ "${release}" =~ ^(12|13)\.[0-9]+$ ]] || return 1
  [[ -f "${CUDA_HOME}/include/cuda_runtime.h" ]] || return 1
  [[ -f "${CUDA_HOME}/lib64/libcudart.so" ||
     -f "${CUDA_HOME}/targets/x86_64-linux/lib/libcudart.so" ||
     -f "${CUDA_HOME}/lib/x86_64-linux-gnu/libcudart.so" ]]
}

host_cudnn_ready() (
  # Compile/link/load checks also support cuDNN installed without dpkg or Python.
  local probe_dir
  probe_dir="$(mktemp -d)" || return 1
  trap 'rm -rf -- "${probe_dir}"' EXIT
  if ! "${CXX}" -x c++ -std=c++20 -I"${CUDA_HOME}/include" \
    -L"${CUDA_HOME}/lib64" -Wl,-rpath,"${CUDA_HOME}/lib64" \
    -o "${probe_dir}/cudnn-check" - -lcudnn >/dev/null 2>&1 <<'CPP'
#include <cudnn.h>
int main() {
  return CUDNN_MAJOR == 9 && cudnnGetVersion() / 10000 == 9 ? 0 : 1;
}
CPP
  then
    return 1
  fi
  "${probe_dir}/cudnn-check" >/dev/null 2>&1
)

host_check_native_cuda() (
  local probe_dir
  probe_dir="$(mktemp -d)"
  trap 'rm -rf -- "${probe_dir}"' EXIT
  "${CUDACXX}" -std=c++20 -arch=native -ccbin "${CXX}" \
    "${repo_root}/scripts/check_cuda.cu" -o "${probe_dir}/check-cuda" || \
    fail '已有 CUDA 无法编译 C++20 环境检查程序；请检查工具链与主机编译器兼容性'
  "${probe_dir}/check-cuda" || fail 'CUDA 环境检查程序运行失败；请检查驱动与 GPU 兼容性'
)

host_check_gpu() {
  if [[ "${host_profile}" == gpu ]]; then
    require_command nvidia-smi
    nvidia-smi -L >/dev/null || fail 'fix the NVIDIA driver/device access before initializing'
  fi
}

host_root() {
  if ((EUID == 0)); then
    "$@"
  else
    require_command sudo
    sudo -- "$@"
  fi
}

download_cached_file() {
  local url="$1" destination="$2"
  if [[ -s "${destination}" ]]; then
    printf '复用已下载安装器：%s\n' "${destination##*/}"
    return
  fi
  printf '下载安装器：%s (连接超时 15 秒，单次最多 180 秒)\n' "${destination##*/}"
  curl --disable --proto '=https' --tlsv1.2 --fail --location --progress-bar \
    --retry 2 --retry-all-errors --retry-max-time 300 \
    --connect-timeout 15 --max-time 180 --speed-limit 1024 --speed-time 30 \
    -o "${destination}.part" "${url}" || \
    fail "下载失败：${destination##*/}；请检查网络后重新运行初始化，已安装的工具会复用"
  mv -- "${destination}.part" "${destination}"
}

host_apt_download_speed() {
  local uri="$1" metrics status=0
  # The same release index is small enough for bootstrap but larger than InRelease.
  # Disable curlrc/retries so user defaults cannot extend this bounded sample.
  metrics="$(LC_ALL=C curl --disable --silent --fail --location --globoff \
    --proto '=http,https' --proto-redir '=http,https' --max-redirs 3 \
    --connect-timeout 3 --max-time 10 --retry 0 --max-filesize 8388608 \
    --output /dev/null --write-out '%{http_code} %{size_download} %{speed_download} %{time_total}' \
    "${uri}/dists/${ubuntu_codename}/main/binary-amd64/Packages.xz" 2>/dev/null)" || status=$?
  LC_ALL=C awk -v status="${status}" -v metrics="${metrics}" 'BEGIN {
    split(metrics, m, " ")
    numeric = "^[0-9]+([.][0-9]+)?$"
    if ((status == 0 || status == 28) && m[1] ~ /^20[06]$/ &&
        m[2] ~ numeric && m[3] ~ numeric && m[4] ~ numeric && m[2]+0 > 0 && m[3]+0 > 0) {
      printf "%.2f MiB/s | %.2f MiB | %.2f s%s\n", m[3]/1048576, m[2]/1048576, m[4],
        (status == 28 ? " | 限时样本(未下载完整)" : "")
    } else if (status == 28) {
      print "超时(未取得有效样本)"
    } else if (m[1] ~ /^[45][0-9][0-9]$/) {
      printf "不可用(HTTP %s)\n", m[1]
    } else if (status != 0) {
      printf "测速失败(curl 状态 %d)\n", status
    } else {
      print "测速失败(无有效下载数据)"
    }
  }'
}

host_measure_apt_sources() {
  local source_file uris uri index result
  local -a labels=() candidates=()
  local -A current_seen=() results=()
  case "${HOST_APT_SPEED_TEST:-1}" in
    0) echo '已跳过 APT 源下载测速(HOST_APT_SPEED_TEST=0)。'; return ;;
    1) ;;
    *) fail 'HOST_APT_SPEED_TEST must be 0 or 1' ;;
  esac
  if ! command -v curl >/dev/null 2>&1; then
    echo '跳过 APT 源下载测速：尚未安装 curl；安装系统工具后可重新运行 install-system 测速。'
    return
  fi
  printf '\nAPT 源下载测速：同一份 %s/main/amd64 索引，每个地址最多 10 秒，连接超时 3 秒。\n' \
    "${ubuntu_codename}"
  echo '结果为本次下载的平均速度(含连接耗时)，仅供选源参考；相同地址复用结果。'
  for source_file in "$@"; do
    if ! uris="$(awk -v mode=uris -v format="${source_file##*.}" \
      -f "${repo_root}/scripts/host-apt-sources.awk" "${source_file}")"; then
      printf '无法读取测速地址：%s\n' "${source_file}"
      continue
    fi
    while IFS= read -r uri; do
      [[ -n "${uri}" && -z "${current_seen[${uri}]:-}" ]] || continue
      current_seen["${uri}"]=1
      labels+=('当前源')
      candidates+=("${uri}")
    done <<< "${uris}"
  done
  if ((${#candidates[@]} == 0)); then
    echo '当前源：未找到可识别的已启用 Ubuntu 镜像，跳过此项。'
  fi
  labels+=('官方源(archive)' '官方源(security)' '清华源')
  candidates+=('http://archive.ubuntu.com/ubuntu' 'http://security.ubuntu.com/ubuntu' \
    'https://mirrors.tuna.tsinghua.edu.cn/ubuntu')
  for index in "${!candidates[@]}"; do
    uri="${candidates[${index}]}"
    printf '  %s | %s/\n    ' "${labels[${index}]}" "${uri}"
    if [[ -n "${results[${uri}]:-}" ]]; then
      result="${results[${uri}]}(复用)"
    else
      result="$(host_apt_download_speed "${uri}")"
      results["${uri}"]="${result}"
    fi
    printf '%s\n' "${result}"
  done
}

host_review_apt_sources() (
  # Use a subshell so temporary-file cleanup never changes the caller's traps.
  local apt_root="${apt_sources_root:-/etc/apt}"
  local choice="${HOST_APT_SOURCE:-}" answer source_file format status relative backup stage
  local recognized=0
  local -a files=() changed_files=()
  for source_file in "${apt_root}/sources.list" \
    "${apt_root}/sources.list.d/"*.list "${apt_root}/sources.list.d/"*.sources; do
    [[ -f "${source_file}" ]] || continue
    files+=("${source_file}")
  done
  printf '当前 APT 源（%s）：\n' "${apt_root}"
  for source_file in "${files[@]}"; do
    printf '\n%s\n' "${source_file}"
    awk '/^[ \t]*(deb(-src)?[ \t]+|URIs:|Suites:)/ {
      line = $0
      gsub(/\/\/[^\/[:space:]@]+@/, "//***@", line)
      print "  " line
    }' "${source_file}"
  done
  ((${#files[@]} > 0)) || echo '未找到 .list 或 .sources 文件。'
  host_measure_apt_sources "${files[@]}"
  if [[ -z "${choice}" ]]; then
    cat <<'EOF'

是否修改 Ubuntu APT 源？
  1) 保持现状（默认）
  2) Ubuntu 官方源
  3) 清华 TUNA 源（包括 Ubuntu security 更新）
仅替换已识别的 Ubuntu 镜像地址，保留发行版、组件、签名选项和第三方源。
EOF
    while true; do
      printf '请选择 [1/2/3，回车保持现状]：' >&2
      IFS= read -r answer || fail '无法读取选择；自动化运行请设置 HOST_APT_SOURCE=keep|official|tuna'
      case "${answer}" in
        '' | 1 | keep) choice=keep; break ;;
        2 | official) choice=official; break ;;
        3 | tuna) choice=tuna; break ;;
        *) echo '无效选择，请输入 1、2 或 3。' >&2 ;;
      esac
    done
  fi
  case "${choice}" in
    keep) echo '保持当前 APT 源。'; return ;;
    official | tuna) ;;
    *) fail 'HOST_APT_SOURCE must be keep, official, or tuna' ;;
  esac

  stage="$(mktemp -d)"
  trap 'rm -rf -- "${stage}"' EXIT
  for source_file in "${files[@]}"; do
    relative="${source_file#"${apt_root}/"}"
    mkdir -p "${stage}/$(dirname "${relative}")"
    format="${source_file##*.}"
    status=0
    awk -v choice="${choice}" -v format="${format}" \
      -f "${repo_root}/scripts/host-apt-sources.awk" "${source_file}" \
      > "${stage}/${relative}" || status=$?
    case "${status}" in
      0)
        [[ ! -L "${source_file}" ]] || fail "源文件为符号链接，请手动修改：${source_file}"
        changed_files+=("${source_file}")
        recognized=1
        ;;
      3) recognized=1 ;;
      4) ;;
      *) fail "无法解析 APT 源：${source_file}" ;;
    esac
  done
  ((recognized)) || fail '未找到可识别的 Ubuntu 镜像地址；请检查上方配置或选择保持现状'
  if ((${#changed_files[@]} == 0)); then
    printf 'Ubuntu APT 源已匹配 %s，无需修改。\n' "${choice}"
    return
  fi
  backup="${apt_root}/programming-lab-source-backups/$(date -u +%Y%m%dT%H%M%SZ)-${BASHPID}"
  host_root install -d -m 0700 "${backup}"
  # Back up every affected file before making the first change.
  for source_file in "${changed_files[@]}"; do
    relative="${source_file#"${apt_root}/"}"
    host_root mkdir -p "${backup}/$(dirname "${relative}")"
    host_root cp -a -- "${source_file}" "${backup}/${relative}"
  done
  for source_file in "${changed_files[@]}"; do
    relative="${source_file#"${apt_root}/"}"
    host_root cp -- "${stage}/${relative}" "${source_file}"
  done
  printf 'Ubuntu APT 源已切换为 %s。原文件备份：%s\n' "${choice}" "${backup}"
)

host_apt_update() {
  # apt-get otherwise returns success for some failed downloads and keeps stale lists.
  host_root apt-get -o APT::Update::Error-Mode=any update || \
    fail 'APT 索引更新失败；请先修复上方源或网络错误，再重新运行初始化'
}

host_prepare_cuda_repository() {
  download_cached_file \
    "https://developer.download.nvidia.com/compute/cuda/repos/${cuda_distro}/x86_64/cuda-keyring_1.1-1_all.deb" \
    "${downloads_dir}/cuda-keyring-${cuda_distro}.deb"
  # Reinstalling an existing package normally preserves deleted conffiles. Images
  # often remove the NVIDIA source list while leaving cuda-keyring installed.
  # Restore missing source/pin files without overwriting existing customizations.
  host_root dpkg --force-confmiss -i "${downloads_dir}/cuda-keyring-${cuda_distro}.deb"
  host_apt_update
}

host_package_installed() {
  [[ "$(dpkg-query -W -f='${db:Status-Status}' "$1" 2>/dev/null)" == installed ]]
}

host_install_missing_packages() {
  local package
  local -a missing=()
  for package in "$@"; do
    if ! host_package_installed "${package}"; then missing+=("${package}"); fi
  done
  if ((${#missing[@]})); then
    host_root apt-get install -y --no-install-recommends --no-upgrade "${missing[@]}"
  fi
}

host_require_apt_candidates() {
  local package candidate
  for package in "$@"; do
    candidate="$(LC_ALL=C apt-cache policy "${package}" | awk '/Candidate:/ {print $2}')"
    [[ -n "${candidate}" && "${candidate}" != '(none)' ]] || \
      fail "APT 中没有可安装的 ${package}；请检查 NVIDIA 源及其索引"
  done
}

host_install_gpu_stack() {
  local release package prepared=0
  host_select_cuda
  if host_cuda_ready; then
    release="$(host_cuda_release)"
    printf '复用已有 CUDA %s：%s\n' "${release}" "${CUDA_HOME}"
  else
    if [[ -n "${HOST_GPU_CUDA_HOME:-}" ]]; then
      fail 'HOST_GPU_CUDA_HOME 指定的 CUDA 不完整或不受支持；请修复该目录或取消此设置'
    fi
    release="$(host_cuda_release)" || release=""
    if [[ -n "${release}" && ! "${release}" =~ ^(12|13)\.[0-9]+$ ]]; then
      fail "已有 CUDA ${release} 不支持本路线；需要 CUDA 12/13，未替换现有安装"
    fi
    host_prepare_cuda_repository
    prepared=1
    if [[ -z "${release}" ]]; then
      package="$(apt-cache pkgnames | awk '/^cuda-minimal-build-13-[0-9]+$/' | sort -V | tail -n 1)"
      [[ -n "${package}" ]] || fail 'NVIDIA APT 索引中没有 CUDA 13 最小构建包'
      release="${package#cuda-minimal-build-}"
      release="${release/-/.}"
    fi
    package="cuda-minimal-build-${release/./-}"
    host_require_apt_candidates "${package}"
    host_install_missing_packages "${package}"
    host_select_cuda
    host_cuda_ready || fail 'CUDA 编译器、头文件或运行库仍缺失；请检查现有安装'
    release="$(host_cuda_release)"
  fi
  if host_cudnn_ready; then
    echo '复用已有 cuDNN 9：头文件、链接及动态库加载检查通过。'
  else
    if ((prepared == 0)); then host_prepare_cuda_repository; fi
    package="libcudnn9-dev-cuda-${release%%.*}"
    host_require_apt_candidates "${package}"
    host_install_missing_packages "${package}"
    host_cudnn_ready || fail 'cuDNN 9 开发环境仍不可用；请检查头文件、动态库及其依赖'
  fi
}

host_install_system() {
  host_check_platform
  host_check_gpu
  host_review_apt_sources
  host_apt_update
  host_install_missing_packages \
    ca-certificates curl gpg git build-essential cmake ninja-build ccache \
    clang-format shellcheck ripgrep make pkg-config xz-utils unzip
  mkdir -p "${downloads_dir}"

  # Ubuntu 22.04 ships CMake 3.22; the repository requires 3.28+.
  if [[ "${ubuntu_codename}" == jammy ]] && ! host_cmake_ready; then
    download_cached_file https://apt.kitware.com/keys/kitware-archive-latest.asc \
      "${downloads_dir}/kitware.asc"
    gpg --batch --yes --dearmor -o "${downloads_dir}/kitware.gpg" "${downloads_dir}/kitware.asc"
    host_root install -m 0644 "${downloads_dir}/kitware.gpg" \
      /usr/share/keyrings/programming-lab-kitware.gpg
    printf '%s\n' \
      'deb [signed-by=/usr/share/keyrings/programming-lab-kitware.gpg] https://apt.kitware.com/ubuntu/ jammy main' \
      > "${downloads_dir}/kitware.list"
    host_root install -m 0644 "${downloads_dir}/kitware.list" /etc/apt/sources.list.d/programming-lab-kitware.list
    host_apt_update
    host_root apt-get install -y --no-install-recommends cmake kitware-archive-keyring
  fi

  if [[ "${host_profile}" == gpu ]]; then
    host_install_missing_packages clang clangd clang-tidy gdb lldb zlib1g
    host_install_gpu_stack
  fi
}

host_install_uv() {
  if [[ ! -x "${uv_bin_dir}/uv" ]]; then
    download_cached_file https://astral.sh/uv/install.sh "${downloads_dir}/uv-install.sh"
    UV_INSTALL_DIR="${uv_bin_dir}" UV_NO_MODIFY_PATH=1 sh "${downloads_dir}/uv-install.sh"
  fi
  uv python install 3.12
}

host_load_node() {
  [[ -s "${NVM_DIR}/nvm.sh" ]] || fail 'nvm is missing; run init'
  # nvm does not support nounset. Restore it after loading and selecting Node.
  local status=0
  set +u
  # shellcheck source=/dev/null
  . "${NVM_DIR}/nvm.sh" --no-use || status=$?
  if ((status == 0)); then nvm use --silent 24 || status=$?; fi
  set -u
  ((status == 0)) || fail 'Node 24 is missing; run init'
}

host_install_node() {
  local installed_version=""
  if [[ -s "${NVM_DIR}/nvm.sh" ]]; then
    # shellcheck source=/dev/null
    installed_version="$(set +u; . "${NVM_DIR}/nvm.sh" --no-use; nvm --version)"
  fi
  if [[ "${installed_version}" != "${nvm_version}" ]]; then
    printf '安装 nvm %s...\n' "${nvm_version}"
    mkdir -p "${NVM_DIR}"
    download_cached_file \
      "https://raw.githubusercontent.com/nvm-sh/nvm/v${nvm_version}/install.sh" \
      "${downloads_dir}/nvm-${nvm_version}-install.sh"
    PROFILE=/dev/null NVM_INSTALL_VERSION="v${nvm_version}" \
      bash "${downloads_dir}/nvm-${nvm_version}-install.sh"
  fi
  local status=0
  set +u
  # shellcheck source=/dev/null
  . "${NVM_DIR}/nvm.sh" --no-use || status=$?
  if ((status == 0)); then
    if nvm use --silent 24 >/dev/null 2>&1; then
      printf '复用已有 Node %s\n' "$(node --version)"
    else
      echo '下载并安装 Node 24...'
      nvm install 24 || status=$?
    fi
  fi
  set -u
  ((status == 0)) || fail 'could not install Node 24'
}

install_rust() {
  local installer_base=""
  local installer_dir=""
  local installer_path=""
  local component=""
  local sysroot=""
  local -a missing_components=()

  if [[ ! -x "${CARGO_HOME}/bin/rustup" ]]; then
    printf 'Installing pinned rustup %s without modifying shell startup files...\n' \
      "${rustup_version}"
    installer_dir="${downloads_dir}/rustup-${rustup_version}"
    mkdir -p "${installer_dir}"
    installer_base="${RUSTUP_UPDATE_ROOT%/}/archive/${rustup_version}/x86_64-unknown-linux-gnu"
    installer_path="${installer_dir}/rustup-init"
    download_cached_file "${installer_base}/rustup-init" "${installer_path}"
    download_cached_file "${installer_base}/rustup-init.sha256" "${installer_path}.sha256"
    (
      cd "${installer_dir}"
      sha256sum --check rustup-init.sha256
    ) || {
      rm -f -- "${installer_path}" "${installer_path}.sha256"
      fail "the cached rustup download failed checksum validation; rerun init to download it again"
    }
    chmod 0755 "${installer_path}"
    RUSTUP_INIT_SKIP_PATH_CHECK=yes \
      "${installer_path}" -y --no-modify-path --default-toolchain none --profile minimal
  fi

  if ! rustup run "${rust_toolchain}" rustc --version >/dev/null 2>&1; then
    if rustup toolchain list | grep -q "^${rust_toolchain}-"; then
      printf 'Removing the incomplete Rust %s toolchain...\n' \
        "${rust_toolchain}"
      rustup toolchain uninstall "${rust_toolchain}"
    fi
    printf 'Installing Rust %s and required components...\n' "${rust_toolchain}"
    rustup toolchain install "${rust_toolchain}" \
      --profile minimal --no-self-update \
      --component clippy \
      --component rustfmt \
      --component rust-src
  else
    printf 'The Rust %s toolchain is already installed.\n' "${rust_toolchain}"
    rustup run "${rust_toolchain}" cargo clippy --version >/dev/null 2>&1 || \
      missing_components+=(clippy)
    rustup run "${rust_toolchain}" rustfmt --version >/dev/null 2>&1 || \
      missing_components+=(rustfmt)
    sysroot="$(rustup run "${rust_toolchain}" rustc --print sysroot)"
    [[ -d "${sysroot}/lib/rustlib/src/rust/library" ]] || missing_components+=(rust-src)
    for component in "${missing_components[@]}"; do
      rustup component add "${component}" --toolchain "${rust_toolchain}"
    done
  fi
}

sync_python() {
  # UV_PYTHON_PREFERENCE=only-managed also applies to venv, sync and lock.
  # Recreate an environment whose interpreter came from an older installation.
  # Keep an already-correct environment so repeated init only synchronizes packages.
  [[ ! -L "${venv_path}" ]] || fail "virtual environment must not be a symlink: ${venv_path}"
  if [[ -d "${venv_path}" ]]; then
    if ! "${venv_path}/bin/python" -c \
      'import os, sys; from pathlib import Path; sys.exit(not (sys.version_info[:2] == (3, 12) and Path(sys.base_prefix).resolve().is_relative_to(Path(os.environ["UV_PYTHON_INSTALL_DIR"]).resolve())))' \
      >/dev/null 2>&1; then
      [[ -f "${venv_path}/pyvenv.cfg" ]] || fail "refusing to replace a non-venv directory: ${venv_path}"
      uv venv --clear --python 3.12 "${venv_path}"
    fi
  fi
  local -a arguments=(sync --locked --python 3.12)
  if [[ "${host_profile}" == cpu ]]; then
    arguments+=(--only-group dev)
  else
    arguments+=(--extra gpu --group dev)
  fi
  uv "${arguments[@]}"
  export VIRTUAL_ENV="${venv_path}"
}

assert_repo_command() {
  local command_name="$1"
  local expected_root="$2"
  local command_path=""

  require_command "${command_name}"
  command_path="$(command -v "${command_name}")"
  case "${command_path}" in
    "${expected_root}"/*)
      ;;
    *)
      fail "${command_name} resolved outside ${expected_root}: ${command_path}"
      ;;
  esac
}

validate_build_jobs() {
  printf '%s\n' "${host_build_jobs}"
}

assert_host_cmake_cache() {
  local cache_path="${repo_root}/build/${route_name}/CMakeCache.txt"
  local compiler_path=""
  local compiler_real_path=""
  local cuda_compiler_path=""
  local cuda_compiler_real_path=""
  local expected_cuda="OFF"

  if [[ "${host_profile}" == gpu ]]; then
    expected_cuda="ON"
  fi

  [[ -f "${cache_path}" ]] || return 0
  grep -q "^PROGRAMMING_LAB_ENABLE_CUDA:BOOL=${expected_cuda}$" "${cache_path}" || \
    fail "the ${route_name} CMake cache has the wrong CUDA setting"
  grep -q '^BUILD_TESTING:BOOL=ON$' "${cache_path}" || \
    fail "the ${route_name} CMake cache does not have tests enabled"

  compiler_path="$(sed -n 's/^CMAKE_CXX_COMPILER:[^=]*=//p' "${cache_path}")"
  [[ -n "${compiler_path}" && -x "${compiler_path}" ]] || \
    fail "the ${route_name} CMake cache has no executable C++ compiler"
  compiler_real_path="$(realpath -e "${compiler_path}")"
  case "${compiler_real_path}" in
    /usr/bin/*)
      ;;
    *)
      fail "CMake selected a compiler outside /usr/bin: ${compiler_real_path}"
      ;;
  esac

  if [[ "${host_profile}" == gpu ]]; then
    cuda_compiler_path="$(sed -n 's/^CMAKE_CUDA_COMPILER:[^=]*=//p' "${cache_path}")"
    [[ -n "${cuda_compiler_path}" && -x "${cuda_compiler_path}" ]] || \
      fail "the ${route_name} CMake cache has no executable CUDA compiler"
    cuda_compiler_real_path="$(realpath -e "${cuda_compiler_path}")"
    [[ "${cuda_compiler_real_path}" == "$(realpath -e "${CUDACXX}")" ]] || \
      fail "CMake selected an unexpected CUDA compiler: ${cuda_compiler_real_path}"
  fi
}

host_cmake_ready() {
  local version
  command -v cmake >/dev/null 2>&1 || return 1
  version="$(cmake --version | head -n 1)"
  dpkg --compare-versions "${version##* }" ge 3.28
}

host_check_system_tools() {
  local command_name
  for command_name in gcc g++ cmake ctest ninja ccache clang-format shellcheck rg make; do
    assert_repo_command "${command_name}" /usr/bin
  done
  host_cmake_ready || fail 'CMake >=3.28 required; run install-system'
  if [[ "${host_profile}" == gpu ]]; then
    for command_name in clang clangd clang-tidy gdb lldb; do
      assert_repo_command "${command_name}" /usr/bin
    done
    assert_repo_command nvcc "${CUDA_HOME}/bin"
    host_cuda_ready || fail 'CUDA 12/13 编译器、头文件或运行库缺失；请运行 init'
    host_cudnn_ready || fail 'cuDNN 9 头文件、链接或动态库加载检查失败；请运行 init'
    host_check_native_cuda
  fi
}

internal_doctor() {
  host_check_system_tools
  local command_name
  for command_name in python pytest ruff basedpyright; do
    assert_repo_command "${command_name}" "${venv_path}/bin"
  done
  assert_repo_command uv "${uv_bin_dir}"
  for command_name in cargo rustc rustfmt rustup clippy-driver; do
    assert_repo_command "${command_name}" "${CARGO_HOME}/bin"
  done
  [[ "$(rustc --version | awk '{print $2}')" == "${rust_toolchain}" ]] || fail 'unexpected Rust version'
  [[ "$(nvm --version)" == "${nvm_version}" ]] || fail 'expected nvm 0.40.3; run init'
  [[ "$(node -p 'process.versions.node.split(".")[0]')" == 24 ]] || fail 'expected Node 24'
  assert_repo_command node "${NVM_DIR}/versions/node"
  host_check_gpu
  python - <<'PYTHON'
import os
import sys
from importlib.metadata import distributions
from pathlib import Path

if Path(sys.prefix).resolve() != Path(os.environ["UV_PROJECT_ENVIRONMENT"]).resolve():
    raise SystemExit("Python is outside the project virtual environment")
if not Path(sys.base_prefix).resolve().is_relative_to(Path(os.environ["UV_PYTHON_INSTALL_DIR"]).resolve()):
    raise SystemExit("Python interpreter is not managed by uv; rerun init")
if sys.version_info[:2] != (3, 12):
    raise SystemExit("expected Python 3.12")
names = {str(dist.metadata.get("Name", "")).casefold().replace("_", "-") for dist in distributions()}
if os.environ["PROGRAMMING_LAB_HOST_PROFILE"] == "cpu":
    blocked = sorted(name for name in names if name in {"torch", "triton", "tilelang"}
                     or name.startswith(("cuda-", "nvidia-", "torch-")))
    if blocked:
        raise SystemExit("unexpected GPU Python packages: " + ", ".join(blocked))
else:
    import tilelang
    import torch
    import triton

    if not torch.cuda.is_available():
        raise SystemExit("PyTorch cannot access an NVIDIA GPU")
PYTHON
  uv lock --check --python 3.12
  local -a arguments=(sync --check --locked --python 3.12)
  if [[ "${host_profile}" == cpu ]]; then
    arguments+=(--only-group dev)
  else
    arguments+=(--extra gpu --group dev)
  fi
  uv "${arguments[@]}"
  uv pip check --python "${venv_path}/bin/python"
  cargo clippy --version >/dev/null
  assert_host_cmake_cache
  printf 'Host %s environment ready.\n' "${host_profile}"
  python --version
  uv --version
  rustc --version
  node --version
  cmake --version | head -n 1
  printf 'Python environment: %s\nSystem C++ compiler: %s\n' "${venv_path}" "${CXX}"
}

internal_build() {
  local jobs=""
  jobs="$(validate_build_jobs)"
  cmake --preset "${route_name}" --fresh
  cmake --build --preset "${route_name}" --parallel "${jobs}"
  assert_host_cmake_cache
}

internal_test() {
  internal_build
  ctest --preset "${route_name}" --no-tests=error
  if [[ "${host_profile}" == cpu ]]; then
    uv run --no-sync --no-env-file python -m pytest -q tests/python/leetcode
  else
    uv run --no-sync --no-env-file python -m pytest
  fi
  cargo test --workspace --all-targets --locked
}

internal_lint() {
  local source_file=""
  local -a clang_tidy_files=()
  local -a native_files=()
  local -a shell_files=()

  if [[ "${host_profile}" == cpu ]]; then
    uv run --no-sync --no-env-file ruff check leetcode/python tests/python/leetcode
    uv run --no-sync --no-env-file ruff format --check leetcode/python tests/python/leetcode
    uv run --no-sync --no-env-file basedpyright leetcode/python tests/python/leetcode
    mapfile -t native_files < <(rg --files leetcode/cpp tests/cpp -g '*.cpp' -g '*.hpp')
  else
    uv run --no-sync --no-env-file ruff check .
    uv run --no-sync --no-env-file ruff format --check .
    uv run --no-sync --no-env-file basedpyright
    mapfile -t native_files < <(
      rg --files \
        -g '*.c' -g '*.cc' -g '*.cpp' -g '*.cxx' \
        -g '*.h' -g '*.hh' -g '*.hpp' -g '*.hxx' \
        -g '*.cu' -g '*.cuh'
    )
  fi

  if ((${#native_files[@]} > 0)); then
    clang-format --dry-run --Werror "${native_files[@]}"
  fi

  if [[ "${host_profile}" == gpu ]]; then
    cmake --preset "${route_name}" --fresh
    mapfile -t clang_tidy_files < <(rg --files leetcode tests -g '*.cc' -g '*.cpp' -g '*.cxx')
    for source_file in "${clang_tidy_files[@]}"; do
      clang-tidy -p "build/${route_name}" "${source_file}"
    done
    assert_host_cmake_cache
  fi

  cargo fmt --all --check
  cargo clippy --workspace --all-targets --locked -- -D warnings

  mapfile -t shell_files < <(rg --files scripts docker -g '*.sh')
  shellcheck docker/bashrc "${shell_files[@]}"
}

host_activate() {
  [[ -x "${uv_bin_dir}/uv" && -x "${venv_path}/bin/python" && -x "${CARGO_HOME}/bin/rustup" ]] || \
    fail "environment is missing; run bash scripts/${route_name}.sh init"
  host_load_node
  export VIRTUAL_ENV="${venv_path}"
}

host_main() {
  local profile="$1"
  shift
  host_configure "${profile}"
  local action="${1:-help}"
  if (($# > 0)); then shift; fi
  case "${action}" in
    help | -h | --help) host_usage; return ;;
    init)
      [[ $# == 0 || ($# == 1 && "$1" == --skip-apt) ]] || fail 'usage: init [--skip-apt]'
      printf '\n[1/6] 准备并检查系统工具\n'
      host_check_platform
      host_check_gpu
      mkdir -p "${downloads_dir}" "${CCACHE_TEMPDIR}"
      if (($# == 0)); then host_install_system; fi
      host_check_system_tools
      printf '\n[2/6] 准备 uv 和 Python 3.12\n'
      host_install_uv
      printf '\n[3/6] 准备 Rust %s 及组件\n' "${rust_toolchain}"
      install_rust
      printf '\n[4/6] 准备 nvm %s 和 Node 24\n' "${nvm_version}"
      host_install_node
      printf '\n[5/6] 同步 Python 项目依赖\n'
      sync_python
      printf '\n[6/6] 执行最终环境诊断\n'
      internal_doctor
      ;;
    install-system)
      (($# == 0)) || fail 'install-system accepts no arguments'
      host_install_system
      ;;
    doctor | build | test | lint | verify | shell)
      (($# == 0)) || fail "${action} accepts no arguments"
      host_activate
      case "${action}" in
        doctor) internal_doctor ;;
        build) internal_build ;;
        test) internal_test ;;
        lint) internal_lint ;;
        verify)
          internal_doctor
          if [[ "${host_profile}" == gpu ]]; then
            uv run --no-sync --no-env-file python -m scripts.check_python_gpu
          fi
          ;;
        shell)
          export PS1="(programming-lab ${route_name}) \w $ "
          exec bash --noprofile --rcfile "${repo_root}/scripts/host-shell.sh" -i
          ;;
      esac
      ;;
    run)
      if [[ "${1:-}" == -- ]]; then shift; fi
      (($# > 0)) || fail "run requires a command after '--'"
      host_activate
      exec "$@"
      ;;
    *) fail "unknown command: ${action}" ;;
  esac
}
