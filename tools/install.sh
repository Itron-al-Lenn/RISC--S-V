#! /bin/bash
DIR=$(dirname "$0")
TOOL_PATH="$(pwd)/$DIR/tools.py"

chmod -v +x "$TOOL_PATH"

mkdir -pv ~/.local/bin
ln -sfv "$TOOL_PATH" ~/.local/bin/risc-tool
