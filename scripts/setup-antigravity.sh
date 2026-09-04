#!/usr/bin/env bash
# ==============================================================================
# Antigravity Environment Setup & Sync Script for Ubuntu
# Repository: https://github.com/adamphh/study-ai-antigravity-skills.git
# ==============================================================================

set -e

# Load NVM environment if available
if [ -d "$HOME/.nvm" ]; then
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

# Color definitions for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

REPO_SSH="git@github.com:adamphh/study-ai-antigravity-skills.git"
REPO_HTTPS="https://github.com/adamphh/study-ai-antigravity-skills.git"
PROJECTS_DIR="/mnt/projects"
TARGET_DIR="$PROJECTS_DIR/study-ai-antigravity-skills"
DEFAULT_BRANCH="dev"

echo -e "${BLUE}======================================================================${NC}"
echo -e "${CYAN}   🚀 Antigravity Environment Setup & Sync Script (Ubuntu)${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo ""

# ------------------------------------------------------------------------------
# 1. Ensure /mnt/projects directory exists with current user permissions
# ------------------------------------------------------------------------------
echo -e "${YELLOW}[1/7] Checking base directory: $PROJECTS_DIR...${NC}"
if [ ! -d "$PROJECTS_DIR" ]; then
    echo "Directory $PROJECTS_DIR does not exist. Creating..."
    if command -v sudo &>/dev/null; then
        sudo mkdir -p "$PROJECTS_DIR"
        sudo chown -R "$USER:$USER" "$PROJECTS_DIR"
    else
        mkdir -p "$PROJECTS_DIR"
    fi
    echo -e "${GREEN}✓ Created $PROJECTS_DIR with ownership $USER:$USER${NC}"
else
    if [ ! -w "$PROJECTS_DIR" ] && command -v sudo &>/dev/null; then
        echo "Updating permissions on $PROJECTS_DIR..."
        sudo chown -R "$USER:$USER" "$PROJECTS_DIR"
    fi
    echo -e "${GREEN}✓ $PROJECTS_DIR is ready.${NC}"
fi

# ------------------------------------------------------------------------------
# 2. Check system dependencies
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[2/7] Checking system dependencies...${NC}"

MISSING_PKGS=()
for cmd in git curl python3; do
    if ! command -v "$cmd" &>/dev/null; then
        MISSING_PKGS+=("$cmd")
    fi
done

if ! command -v node &>/dev/null && ! command -v nodejs &>/dev/null; then
    MISSING_PKGS+=("nodejs")
fi

if ! command -v npm &>/dev/null; then
    MISSING_PKGS+=("npm")
fi

if [ ${#MISSING_PKGS[@]} -gt 0 ]; then
    echo -e "${YELLOW}Missing packages detected: ${MISSING_PKGS[*]}${NC}"
    if command -v sudo &>/dev/null; then
        echo "Installing missing packages via apt-get..."
        sudo apt-get update -qq && sudo apt-get install -y -qq "${MISSING_PKGS[@]}"
        echo -e "${GREEN}✓ System packages installed successfully.${NC}"
    else
        echo -e "${RED}Please install missing packages manually: ${MISSING_PKGS[*]}${NC}"
    fi
else
    echo -e "${GREEN}✓ All core dependencies (git, curl, python3, node, npm) are present.${NC}"
fi

# Ensure PyYAML for Python indexer
if ! python3 -c "import yaml" &>/dev/null; then
    echo "Installing PyYAML for Python indexer..."
    pip3 install --user pyyaml --quiet 2>/dev/null || python3 -m pip install pyyaml --quiet 2>/dev/null || true
    if python3 -c "import yaml" &>/dev/null; then
        echo -e "${GREEN}✓ PyYAML installed.${NC}"
    else
        echo -e "${YELLOW}⚠ Could not install PyYAML automatically. Please run 'pip install pyyaml'.${NC}"
    fi
fi

# ------------------------------------------------------------------------------
# 3. Clone or update repository
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[3/7] Setting up study-ai-antigravity-skills repository...${NC}"

if [ ! -d "$TARGET_DIR/.git" ]; then
    echo "Cloning repository into $TARGET_DIR..."
    if git clone -b "$DEFAULT_BRANCH" "$REPO_SSH" "$TARGET_DIR" 2>/dev/null; then
        echo -e "${GREEN}✓ Cloned via SSH successfully.${NC}"
    else
        echo "SSH clone failed or key not configured. Falling back to HTTPS clone..."
        git clone -b "$DEFAULT_BRANCH" "$REPO_HTTPS" "$TARGET_DIR"
        echo -e "${GREEN}✓ Cloned via HTTPS successfully.${NC}"
    fi
else
    echo "Repository already exists. Updating from $DEFAULT_BRANCH..."
    cd "$TARGET_DIR"
    git fetch origin
    git checkout "$DEFAULT_BRANCH" 2>/dev/null || true
    git pull origin "$DEFAULT_BRANCH"
    echo -e "${GREEN}✓ Repository updated to latest commit.${NC}"
fi

# ------------------------------------------------------------------------------
# 4. Create necessary local directories
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[4/7] Preparing directory structure in home directory...${NC}"

mkdir -p "$HOME/.gemini/config/scripts"
mkdir -p "$HOME/.gemini/config/projects"
mkdir -p "$HOME/.agent/cache"
mkdir -p "$HOME/.agent/rules"
mkdir -p "$HOME/.agent/scripts"
mkdir -p "$HOME/.agent/skills/list-jira"
mkdir -p "$HOME/.local/bin"

echo -e "${GREEN}✓ Home configuration directories created.${NC}"

# ------------------------------------------------------------------------------
# 5. Setup Global Symlinks (Zero Manual Copying)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[5/7] Linking configuration symlinks...${NC}"

# 5.1 Link ~/.gemini/config/ components
ln -sf "$TARGET_DIR/AGENTS.md" "$HOME/.gemini/config/AGENTS.md"
ln -sfn "$TARGET_DIR/my-skills" "$HOME/.gemini/config/skills"
ln -sfn "$TARGET_DIR/rules" "$HOME/.gemini/config/rules"
ln -sfn "$TARGET_DIR/workflows" "$HOME/.gemini/config/workflows"
ln -sf "$TARGET_DIR/scripts/manage_jira_cache.py" "$HOME/.gemini/config/scripts/manage_jira_cache.py"

# 5.2 Link ~/.agent/ components (Directory-level symlinks)
mkdir -p "$HOME/.agent"
ln -sfn "$TARGET_DIR/rules" "$HOME/.agent/rules"
ln -sfn "$TARGET_DIR/my-skills" "$HOME/.agent/skills"
ln -sfn "$TARGET_DIR/scripts" "$HOME/.agent/scripts"
ln -sfn "$TARGET_DIR/workflows" "$HOME/.agent/workflows"

# 5.3 Make scripts executable & link to ~/.local/bin
chmod +x "$TARGET_DIR/scripts/manage_jira_cache.py"
chmod +x "$TARGET_DIR/scripts/index-refresh"
chmod +x "$TARGET_DIR/scripts/setup-antigravity.sh"
chmod +x "$TARGET_DIR/scripts/sync_project_mapping.py"
ln -sf "$TARGET_DIR/scripts/index-refresh" "$HOME/.local/bin/index-refresh"
ln -sf "$TARGET_DIR/scripts/setup-antigravity.sh" "$HOME/.local/bin/setup-antigravity"

echo -e "${GREEN}✓ All global symlinks configured successfully.${NC}"

# ------------------------------------------------------------------------------
# 6. Configure MCP Server (mcp_config.json)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[6/7] Checking MCP server configuration...${NC}"

MCP_TARGET="$HOME/.gemini/config/mcp_config.json"
MCP_SOURCE="$TARGET_DIR/mcp_config.json"

if [ ! -f "$MCP_TARGET" ]; then
    if [ -f "$MCP_SOURCE" ]; then
        cp "$MCP_SOURCE" "$MCP_TARGET"
        echo -e "${GREEN}✓ Created $MCP_TARGET from template.${NC}"
    fi
else
    echo -e "${GREEN}✓ $MCP_TARGET already exists.${NC}"
fi

# ------------------------------------------------------------------------------
# 7. Pre-generate Shared Core Indexes
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[7/7] Generating shared core indexes (Tầng 1)...${NC}"

if [ -f "$TARGET_DIR/scripts/index_core.py" ]; then
    python3 "$TARGET_DIR/scripts/index_core.py" || true
    echo -e "${GREEN}✓ Shared core index processed.${NC}"
fi

# Ensure ~/.local/bin is in PATH for current shell
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    export PATH="$HOME/.local/bin:$PATH"
fi

echo ""
echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN}   ✨ Antigravity Environment Setup Completed Successfully! ✨${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo ""
echo -e "💡 ${CYAN}Cách sử dụng cho dự án mới trên máy này:${NC}"
echo -e "   1. Chuyển vào thư mục dự án:"
echo -e "      ${YELLOW}cd /mnt/projects/<ten-du-an>${NC}"
echo -e "   2. Đấu nối cấu hình agent:"
echo -e "      ${YELLOW}ln -sf $TARGET_DIR/.agent .agent${NC}"
echo -e "   3. Mở Antigravity Chat UI và gõ: ${YELLOW}/index-refresh${NC} hoặc ${YELLOW}/list-jira${NC}"
echo ""
