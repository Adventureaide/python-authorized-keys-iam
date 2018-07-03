#!/bin/bash

SCRIPT_DIR=="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

"$SCRIPT_DIR"/env/bin/python "$SCRIPT_DIR"/authorized-keys-iam.py auth "$1"
