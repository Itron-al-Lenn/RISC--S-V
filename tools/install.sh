#! /bin/bash
echo "Link git hooks..."
for hook in "$(pwd)"/.githooks/*; do
  if [ -f "$hook" ]; then
    hook_name=$(basename "$hook")
    echo "Installing hook: $hook_name"
    ln -sfv "$hook" "$(pwd)/.git/hooks/$hook_name"
  fi
done

echo "Setup git 'main' branch protection rules..."
git config branch.main.mergeoptions "--no-ff"
