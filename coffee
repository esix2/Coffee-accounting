#!/bin/bash
SELF=$(readlink -f -- "$BASH_SOURCE")
source "${SELF%/*}/venv/bin/activate"
cd "${SELF%/*}/python"
exec python coffee.py
