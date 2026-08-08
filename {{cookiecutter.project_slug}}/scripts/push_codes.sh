#!/bin/sh
set -e

echo "Uploading codes dataset..."
uv run python src/upload.py codes
echo "Done!"
