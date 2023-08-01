#!/bin/bash

cd /root/finary_api_perso/finary

virtualenv -p /usr/bin/python3.11 venv

source venv/bin/activate

pip install -r requirements.txt

python application.py

deactivate