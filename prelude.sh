#!/bin/bash -ue

python3 -m venv .venv
PIP=.venv/bin/pip
$PIP install requests requests-oauthlib


