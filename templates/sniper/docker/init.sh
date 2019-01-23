#!/bin/sh
python rewrite.py
echo $APPYAML > /etc/prom-conf/app.yaml
