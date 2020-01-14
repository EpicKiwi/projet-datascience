#!/bin/bash

if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Aucun virtualenv detecté, démarrage du virtualenv..."
    ./venv.sh -c ./jupyter.sh
    exit 0
fi

jupyter-lab .
