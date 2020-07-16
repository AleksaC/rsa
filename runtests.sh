#!/usr/bin/env bash

set -eou pipefail

cd algorithm
if ! pip freeze | grep -q "\-e git+git@github.com:AleksaC/rsa.git"; then
    pip install -e .
fi
pytest --cov=rsa --cov-config=../.coveragerc --doctest-modules
cd ..

cd web_app
pytest --cov=backend --cov-config=../.coveragerc backend/test_app.py
cd ..

coverage combine algorithm/.coverage web_app/.coverage
coverage html
