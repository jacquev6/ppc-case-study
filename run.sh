#!/bin/bash

set -o errexit

if ! (diff Makefile build/Makefile && diff builder/Dockerfile build/Dockerfile) >/dev/null 2>&1
then
  rm -rf build
  mkdir build
  cp Makefile build/Makefile
  cp builder/Dockerfile build/Dockerfile
  docker build builder
fi

image=$(docker build --quiet builder)

docker run \
  --rm \
  --user $(id -u):$(id -g) `# Avoid creating files as root`\
  --volume "$PWD:/wd" --workdir /wd \
  $image \
    make -j$(nproc) link

docker run \
  --rm \
  --user $(id -u):$(id -g) `# Avoid creating files as root`\
  --volume "$PWD:/wd" --workdir /wd \
  --gpus all \
  $image \
    make -j1 benchmark

if ! diff requirements.txt .venv/requirements.txt >/dev/null 2>&1
then
  rm -rf .venv
  virtualenv .venv
  . .venv/bin/activate
  pip install -r requirements.txt
  deactivate
  cp requirements.txt .venv/requirements.txt
fi

. .venv/bin/activate
rm -f *.png
python gen-figures.py README.md
