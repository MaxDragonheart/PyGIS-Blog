#!/usr/bin/env bash

##### CHECK url before start!
# https://quarto.org/docs/get-started/

version="1.3.450"
url="https://github.com/quarto-dev/quarto-cli/releases/download/v${version}/quarto-${version}-linux-amd64.deb"

echo "--> Download Quarto v${version}"
echo "    from ${url}"

# Make download folder
mkdir "quarto"

# Start download
wget "${url}" -P quarto/

# Install Quarto
echo "--> Install Quarto"
dpkg -i "quarto/quarto-${version}-linux-amd64.deb"

# Remove download folder
rm -rf quarto