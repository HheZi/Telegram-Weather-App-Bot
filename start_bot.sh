#!/bin/bash

source ./venv/bin/activate

echo "Starting the Telegram Bot..."

python bot.py

echo "Stop the the Telegram bot"

deactivate
