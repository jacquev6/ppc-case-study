#!/bin/bash

set -o errexit

if ! diff requirements.txt .venv/requirements.txt >/dev/null 2>&1
then
  rm -rf .venv
  virtualenv .venv
  . .venv/bin/activate
  pip install -r requirements.txt
  deactivate
  cp requirements.txt .venv/requirements.txt
fi

if ! diff Makefile build/Makefile >/dev/null 2>&1
then
  rm -rf build
  mkdir build
  cp Makefile build/Makefile
fi

. .venv/bin/activate

make -j$(nproc) link
make -j1 benchmark

python report.py >README.md
