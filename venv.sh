#!/usr/bin/env bash
set -e
if [ ! -f /usr/bin/python3 ]; then
    echo "Python 3 is required"
    exit 1
fi

CURRENT_PWD=$PWD
SCRIPT_DIR=$(dirname $(readlink -f $0))

cd ${SCRIPT_DIR}

python3 -m venv ${SCRIPT_DIR}/venv
source ${SCRIPT_DIR}/venv/bin/activate
python3 -m pip install --upgrade pip

set +e
python3 -m pip install -r ${SCRIPT_DIR}/requirements.txt

cd ${CURRENT_PWD}