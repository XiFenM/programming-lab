# syntax=docker/dockerfile:1.7

ARG BASE_IMAGE=nvidia/cuda:13.0.3-cudnn-devel-ubuntu24.04
FROM ${BASE_IMAGE} AS toolchain

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG USERNAME=coder
ARG USER_UID=1000
ARG USER_GID=1000
ARG PYTHON_VERSION=3.12
ARG UBUNTU_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/ubuntu
ARG UBUNTU_PORTS_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports
ARG NVIDIA_APT_MIRROR=https://developer.download.nvidia.cn/compute/cuda/repos
ARG PYPI_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ARG NVM_NODEJS_ORG_MIRROR=https://mirrors.tuna.tsinghua.edu.cn/nodejs-release
ARG RUSTUP_DIST_SERVER=https://mirrors.tuna.tsinghua.edu.cn/rustup
ARG RUSTUP_UPDATE_ROOT=https://mirrors.tuna.tsinghua.edu.cn/rustup/rustup

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8

# Replace Ubuntu and NVIDIA CUDA apt endpoints before the first apt update.
# Build arguments keep the mirrors overridable without editing this file.
RUN set -eux; \
    for source_file in /etc/apt/sources.list /etc/apt/sources.list.d/ubuntu.sources; do \
        if [[ -f "${source_file}" ]]; then \
            sed -i \
                -e "s|http://archive.ubuntu.com/ubuntu|${UBUNTU_MIRROR}|g" \
                -e "s|https://archive.ubuntu.com/ubuntu|${UBUNTU_MIRROR}|g" \
                -e "s|http://security.ubuntu.com/ubuntu|${UBUNTU_MIRROR}|g" \
                -e "s|https://security.ubuntu.com/ubuntu|${UBUNTU_MIRROR}|g" \
                -e "s|http://ports.ubuntu.com/ubuntu-ports|${UBUNTU_PORTS_MIRROR}|g" \
                -e "s|https://ports.ubuntu.com/ubuntu-ports|${UBUNTU_PORTS_MIRROR}|g" \
                "${source_file}"; \
        fi; \
    done; \
    for source_file in /etc/apt/sources.list.d/cuda*.list /etc/apt/sources.list.d/cuda*.sources; do \
        if [[ -f "${source_file}" ]]; then \
            sed -i \
                -e "s|https://developer.download.nvidia.com/compute/cuda/repos|${NVIDIA_APT_MIRROR}|g" \
                -e "s|https://developer.download.nvidia.cn/compute/cuda/repos|${NVIDIA_APT_MIRROR}|g" \
                "${source_file}"; \
        fi; \
    done; \
    printf '%s\n' \
        'Acquire::Retries "5";' \
        'Acquire::http::Timeout "30";' \
        'Acquire::https::Timeout "30";' \
        > /etc/apt/apt.conf.d/80-network-retries

# CUDA/C++ development tools and small command-line utilities used by the
# repository scripts. Python is intentionally not installed from apt.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash-completion \
        build-essential \
        ca-certificates \
        ccache \
        clang \
        clang-format \
        clang-tidy \
        clangd \
        cmake \
        curl \
        gdb \
        git \
        git-lfs \
        jq \
        less \
        lldb \
        locales \
        make \
        nano \
        ninja-build \
        openssh-client \
        pkg-config \
        ripgrep \
        shellcheck \
        sudo \
        unzip \
        vim-tiny \
        wget \
        zip \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Ubuntu 24.04 CUDA images may already reserve UID/GID 1000 for an `ubuntu`
# account. Reuse that numeric identity when present so bind-mount ownership
# still matches the WSL user while the development account remains `coder`.
RUN set -eux; \
    if [[ ! "${USER_UID}" =~ ^[1-9][0-9]*$ || ! "${USER_GID}" =~ ^[1-9][0-9]*$ ]]; then \
        echo "USER_UID and USER_GID must be positive non-root integers" >&2; \
        exit 64; \
    fi; \
    named_group_gid="$(getent group "${USERNAME}" | cut -d: -f3 || true)"; \
    if [[ -n "${named_group_gid}" && "${named_group_gid}" != "${USER_GID}" ]]; then \
        echo "group ${USERNAME} already exists with GID ${named_group_gid}" >&2; \
        exit 65; \
    fi; \
    if ! getent group "${USER_GID}" >/dev/null; then \
        groupadd --gid "${USER_GID}" "${USERNAME}"; \
    fi; \
    uid_username="$(getent passwd "${USER_UID}" | cut -d: -f1 || true)"; \
    named_user_uid="$(getent passwd "${USERNAME}" | cut -d: -f3 || true)"; \
    if [[ -n "${named_user_uid}" && "${named_user_uid}" != "${USER_UID}" ]]; then \
        echo "user ${USERNAME} already exists with UID ${named_user_uid}" >&2; \
        exit 65; \
    fi; \
    if [[ -n "${uid_username}" && "${uid_username}" != "${USERNAME}" ]]; then \
        usermod --login "${USERNAME}" "${uid_username}"; \
    elif [[ -z "${uid_username}" ]]; then \
        useradd \
            --uid "${USER_UID}" \
            --gid "${USER_GID}" \
            --home-dir "/home/${USERNAME}" \
            --create-home \
            --shell /bin/bash \
            "${USERNAME}"; \
    fi; \
    current_home="$(getent passwd "${USERNAME}" | cut -d: -f6)"; \
    if [[ "${current_home}" != "/home/${USERNAME}" ]]; then \
        if [[ -d "${current_home}" && ! -e "/home/${USERNAME}" ]]; then \
            usermod --home "/home/${USERNAME}" --move-home "${USERNAME}"; \
        else \
            usermod --home "/home/${USERNAME}" "${USERNAME}"; \
        fi; \
    fi; \
    usermod --gid "${USER_GID}" --shell /bin/bash "${USERNAME}"; \
    printf '%s ALL=(root) NOPASSWD:ALL\n' "${USERNAME}" > "/etc/sudoers.d/${USERNAME}"; \
    chmod 0440 "/etc/sudoers.d/${USERNAME}"; \
    mkdir -p \
        /workspace \
        "/home/${USERNAME}/.cache/ccache" \
        "/home/${USERNAME}/.cache/tilelang" \
        "/home/${USERNAME}/.cache/triton" \
        "/home/${USERNAME}/.cache/uv" \
        "/home/${USERNAME}/.cargo/git" \
        "/home/${USERNAME}/.cargo/registry" \
        "/home/${USERNAME}/.venvs"; \
    chown -R "${USER_UID}:${USER_GID}" /workspace "/home/${USERNAME}"

COPY --chown=${USER_UID}:${USER_GID} docker/bashrc /home/${USERNAME}/.bashrc
COPY --chown=${USER_UID}:${USER_GID} docker/cargo-config.toml /home/${USERNAME}/.cargo/config.toml
COPY docker/entrypoint.sh /usr/local/bin/programming-lab-entrypoint
RUN chmod 0755 /usr/local/bin/programming-lab-entrypoint

USER ${USERNAME}
WORKDIR /workspace

ENV HOME=/home/${USERNAME} \
    UV_PROJECT_ENVIRONMENT=/home/${USERNAME}/.venvs/programming-lab \
    UV_CACHE_DIR=/home/${USERNAME}/.cache/uv \
    UV_PYTHON_INSTALL_DIR=/home/${USERNAME}/.local/share/uv/python \
    UV_PYTHON_PREFERENCE=only-managed \
    UV_LINK_MODE=copy \
    UV_DEFAULT_INDEX=${PYPI_INDEX_URL} \
    PIP_INDEX_URL=${PYPI_INDEX_URL}

# Install uv with Astral's official command, then let uv install managed
# CPython. No distro Python interpreter is used for the project environment.
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH=${HOME}/.local/bin:${PATH}
RUN uv python install "${PYTHON_VERSION}"

# Install nvm and the latest Node.js 24.x using the official nvm command.
ENV NVM_DIR=${HOME}/.nvm \
    NVM_NODEJS_ORG_MIRROR=${NVM_NODEJS_ORG_MIRROR}
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash \
    && . "${NVM_DIR}/nvm.sh" \
    && nvm install 24 \
    && nvm alias default 24 \
    && node_version_dir="$(dirname "$(dirname "$(nvm which 24)")")" \
    && ln -sfn "${node_version_dir}" "${NVM_DIR}/current"
ENV PATH=${NVM_DIR}/current/bin:${PATH}

# Rust is installed per-user so rustup, cargo, rustfmt and clippy can be
# upgraded without modifying the system toolchain.
ENV RUSTUP_DIST_SERVER=${RUSTUP_DIST_SERVER} \
    RUSTUP_UPDATE_ROOT=${RUSTUP_UPDATE_ROOT}
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
        | sh -s -- -y --profile minimal --default-toolchain stable \
    && . "${HOME}/.cargo/env" \
    && rustup component add clippy rustfmt rust-src
ENV PATH=${HOME}/.cargo/bin:${PATH}

ENV CCACHE_DIR=${HOME}/.cache/ccache \
    CMAKE_GENERATOR=Ninja \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1

LABEL org.opencontainers.image.title="programming-lab" \
      org.opencontainers.image.description="CUDA, Triton, TileLang and LeetCode development environment"

ENTRYPOINT ["/usr/local/bin/programming-lab-entrypoint"]
CMD ["sleep", "infinity"]

# Optional snapshot target: source files are copied once at image build time.
# The default runtime target deliberately contains no repository snapshot.
FROM toolchain AS workspace-copy
ARG USER_UID=1000
ARG USER_GID=1000
COPY --chown=${USER_UID}:${USER_GID} . /workspace

FROM toolchain AS runtime
