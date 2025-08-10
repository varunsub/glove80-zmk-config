#!/bin/bash
# Setup script for local development

set -euo pipefail

echo "Setting up local ZMK for development..."

# Check if zmk directory exists, if not, create a symlink to the local repo
if [ ! -d "zmk" ]; then
    if [ -d "../zmk" ]; then
        echo "Creating symlink to ../zmk"
        ln -sf ../zmk zmk
    else
        echo "Error: ZMK directory not found at ../zmk"
        echo "Please make sure you have the ZMK repository cloned at ../zmk"
        exit 1
    fi
else
    echo "ZMK directory already exists"
fi

echo "Setup complete! You can now run local builds."
echo ""
echo "Available build options:"
echo "  ./build.sh          - Build using Docker (recommended)"
echo "  nix-build config -o combined && cp combined/glove80.uf2 .  - Direct Nix build"
