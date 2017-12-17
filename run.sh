#!/bin/bash -ue

docker build --tag ttd .
docker run -it ttd bash
# set environment variable and exec main.py

# webhookで適当に更新を投げるとか
# CodeDeployは、やりすぎかなあ
