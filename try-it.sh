#!/bin/bash

set -xeuo pipefail

dnf install 'dnf-command(builddep)' git make pip osbuild-composer -y

pushd /tmp

git clone https://github.com/osbuild/osbuild-composer.git
pushd osbuild-composer
sed -i 's|%gometa||' osbuild-composer.spec
dnf builddep osbuild-composer.spec -y
make build
cp bin/osbuild-pipeline /usr/bin/
popd

git clone https://github.com/msehnout/osbilder.git
pushd osbilder
pip install -r requirements.txt
mkdir test
python3 main.py init --workdir=test
cat > test/blueprints/test.toml << EOF
name = "base"
description = "A base system with bash"
version = "0.0.1"

[[packages]]
name = "bash"
version = "*"
EOF
python3 main.py build --distro=fedora-33 --image-type=qcow2 --blueprint=test --workdir=test