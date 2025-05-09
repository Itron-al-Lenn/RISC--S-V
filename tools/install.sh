#! /bin/bash
echo "Link git hooks..."
for hook in "$(pwd)"/.githooks/*; do
  if [ -f "$hook" ]; then
    hook_name=$(basename "$hook")
    echo "Installing hook: $hook_name"
    ln -sfv "$hook" "$(pwd)/.git/hooks/$hook_name"
  fi
done

echo "Activate Python virtual environment..."
activate_file="$(pwd)/.venv/bin/activate"
if [ -f "$activate_file" ]; then
  echo "Activate: $activate_file"
  source "$activate_file"
else
  echo "No file at $activate_file"
fi

echo "Setup git 'main' branch protection rules..."
if ! git config --get branch.main.mergeoptions | grep -q -- "--no-ff"; then
  echo "Setting merge option --no-ff for main branch"
  git config branch.main.mergeoptions "--no-ff"
else
  echo "Merge option --no-ff for main branch already set"
fi
