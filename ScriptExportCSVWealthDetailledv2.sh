#!/bin/bash

python -m finary_api signin

python -m finary_api investments > Data/BalanceWealthDetailled.json

python -m finary_api fonds_euro > Data/BalanceWealthFondsEuros.json

