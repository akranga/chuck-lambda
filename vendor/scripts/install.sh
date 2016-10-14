#!/bin/bash

# You need "virtualenv":
# pip install virtualenv

virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt -t lib --upgrade
