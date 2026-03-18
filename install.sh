#!/usr/bin/env bash
# Claude Code installer
# Usage: curl -fsSL https://claude.ai/install.sh | bash
#
# This script installs Claude Code, Anthropic's official CLI for Claude.
# It detects your platform, ensures Node.js is available, and installs
# the @anthropic-ai/claude-code npm package globally.

set -euo pipefail

PACKAGE_NAME="@anthropic-ai/claude-code"
MIN_NODE_VERSION=18
BOLD=''
RESET=''
RED=''
GREEN=''
YELLOW=''
BLUE=''

# Enable colors if connected to a terminal
if [ -t 1 ]; then
    BOLD='\033[1m'
    RESET='\033[0m'
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
fi

info() {
    printf "${BLUE}${BOLD}info${RESET} %s\n" "$1"
}

success() {
    printf "${GREEN}${BOLD}success${RESET} %s\n" "$1"
}

warn() {
    printf "${YELLOW}${BOLD}warn${RESET} %s\n" "$1"
}

error() {
    printf "${RED}${BOLD}error${RESET} %s\n" "$1" >&2
}

# Detect OS and architecture
detect_platform() {
    local os arch

    os="$(uname -s)"
    arch="$(uname -m)"

    case "$os" in
        Linux)  OS="linux" ;;
        Darwin) OS="macos" ;;
        *)
            error "Unsupported operating system: $os"
            error "Claude Code supports Linux and macOS."
            exit 1
            ;;
    esac

    case "$arch" in
        x86_64|amd64)   ARCH="x64" ;;
        aarch64|arm64)   ARCH="arm64" ;;
        *)
            error "Unsupported architecture: $arch"
            exit 1
            ;;
    esac
}

# Compare semver: returns 0 if $1 >= $2
version_gte() {
    local IFS=.
    local i a=($1) b=($2)
    for ((i = 0; i < ${#b[@]}; i++)); do
        local va=${a[i]:-0}
        local vb=${b[i]:-0}
        if ((va > vb)); then return 0; fi
        if ((va < vb)); then return 1; fi
    done
    return 0
}

# Check if a command exists
has() {
    command -v "$1" >/dev/null 2>&1
}

# Find a suitable Node.js installation
find_node() {
    local node_cmd=""

    if has node; then
        node_cmd="node"
    elif has nodejs; then
        node_cmd="nodejs"
    fi

    if [ -n "$node_cmd" ]; then
        local node_version
        node_version="$($node_cmd --version 2>/dev/null | sed 's/^v//')"
        if version_gte "$node_version" "$MIN_NODE_VERSION.0.0"; then
            NODE_CMD="$node_cmd"
            NODE_VERSION="$node_version"
            return 0
        else
            warn "Found Node.js v${node_version}, but v${MIN_NODE_VERSION}+ is required."
            return 1
        fi
    fi

    return 1
}

# Find a suitable package manager (npm or yarn)
find_package_manager() {
    if has npm; then
        PKG_MANAGER="npm"
        return 0
    fi
    return 1
}

# Suggest how to install Node.js
suggest_node_install() {
    echo ""
    error "Node.js v${MIN_NODE_VERSION}+ is required but was not found."
    echo ""
    echo "Install Node.js using one of these methods:"
    echo ""

    if [ "$OS" = "macos" ]; then
        echo "  ${BOLD}Homebrew:${RESET}"
        echo "    brew install node"
        echo ""
        echo "  ${BOLD}Official installer:${RESET}"
        echo "    https://nodejs.org/en/download"
        echo ""
    elif [ "$OS" = "linux" ]; then
        echo "  ${BOLD}NodeSource:${RESET}"
        echo "    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -"
        echo "    sudo apt-get install -y nodejs"
        echo ""
        echo "  ${BOLD}Official installer:${RESET}"
        echo "    https://nodejs.org/en/download"
        echo ""
    fi

    echo "  ${BOLD}nvm (Node Version Manager):${RESET}"
    echo "    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash"
    echo "    nvm install --lts"
    echo ""
    echo "After installing Node.js, re-run this installer:"
    echo "  curl -fsSL https://claude.ai/install.sh | bash"
    echo ""
}

# Install Claude Code via npm
install_claude_code() {
    info "Installing ${PACKAGE_NAME}..."

    local install_cmd
    if [ "$PKG_MANAGER" = "npm" ]; then
        install_cmd="npm install -g ${PACKAGE_NAME}"
    fi

    # Try without sudo first; fall back to sudo on permission errors
    if $install_cmd 2>/dev/null; then
        return 0
    fi

    warn "Global install failed — retrying with sudo..."
    if has sudo; then
        if sudo $install_cmd; then
            return 0
        fi
    fi

    error "Installation failed. You may need to fix npm permissions."
    echo ""
    echo "See: https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally"
    echo ""
    return 1
}

# Verify the installation works
verify_installation() {
    if has claude; then
        local version
        version="$(claude --version 2>/dev/null || echo "unknown")"
        echo ""
        success "Claude Code ${version} has been installed!"
        echo ""
        echo "  Get started by running:"
        echo ""
        echo "    ${BOLD}claude${RESET}"
        echo ""
        return 0
    else
        echo ""
        error "Installation completed but 'claude' command was not found in PATH."
        echo ""
        echo "  You may need to restart your terminal or add npm's global bin"
        echo "  directory to your PATH."
        echo ""

        if has npm; then
            local npm_bin
            npm_bin="$(npm config get prefix 2>/dev/null)/bin"
            echo "  Try adding this to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
            echo ""
            echo "    export PATH=\"${npm_bin}:\$PATH\""
            echo ""
        fi
        return 1
    fi
}

main() {
    echo ""
    printf "${BOLD}Claude Code Installer${RESET}\n"
    echo ""

    detect_platform
    info "Detected platform: ${OS} (${ARCH})"

    # Check for Node.js
    if ! find_node; then
        suggest_node_install
        exit 1
    fi
    info "Found Node.js v${NODE_VERSION}"

    # Check for npm
    if ! find_package_manager; then
        error "npm is required but was not found."
        error "Please install npm and try again."
        exit 1
    fi
    info "Using package manager: ${PKG_MANAGER}"

    # Check if already installed
    if has claude; then
        local current_version
        current_version="$(claude --version 2>/dev/null || echo "")"
        if [ -n "$current_version" ]; then
            info "Claude Code is already installed (${current_version}). Updating..."
        fi
    fi

    # Install
    install_claude_code

    # Verify
    verify_installation
}

main "$@"
