#! /bin/bash
DIR=$(dirname "$0")
TOOL_PATH="$(pwd)/$DIR/tools.py"

echo "Link git hooks..."
for hook in "$(pwd)"/.githooks/*; do
  if [ -f "$hook" ]; then
    hook_name=$(basename "$hook")
    echo "Installing hook: $hook_name"
    ln -sfv "$hook" "$(pwd)/.git/hooks/$hook_name"
  fi
done

echo "Make Script executable..."
chmod +x "$TOOL_PATH"

mkdir -pv ~/.local/bin
ln -sfv "$TOOL_PATH" ~/.local/bin/risc-tool
