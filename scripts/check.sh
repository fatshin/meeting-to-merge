#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m runtime.evaluate

