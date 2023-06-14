#!/bin/bash

cd /root/finary_api_perso/finary

virtualenv -p /usr/bin/python3.11 venv

source venv/bin/activate

pip install -r requirements.txt

python -m finary_api signin

python -m finary_api investments > Data/BalanceWealthDetailled.json

python -m finary_api fonds_euro > Data/BalanceFondsEuros.json

python ScriptExportCSVWealthDetailled.py

deactivate