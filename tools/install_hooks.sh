#!/bin/sh
set -eu

git config core.hooksPath tools/hooks
echo "Configured Git hooks path: tools/hooks"
