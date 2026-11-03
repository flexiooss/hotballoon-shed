#!/usr/bin/env bash
set -e

CURRENT_PWD=$PWD
SCRIPT_DIR=$(dirname $(readlink -f $0))

cd ${SCRIPT_DIR}

if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
  echo "Python >= 3.10 is required (found $(python3 --version 2>&1))" >&2
  exit 1
fi

python3 -m venv ${SCRIPT_DIR}/venv
source ${SCRIPT_DIR}/venv/bin/activate
python3 -m pip install --upgrade pip

set +e
python3 -m pip install -r ${SCRIPT_DIR}/requirements.txt

cd ${CURRENT_PWD}