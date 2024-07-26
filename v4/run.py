from secret import LOG_FILE
import logging
import bot
import sys

debug = False

RED = "\033[31m"
RESET = "\033[0m"

try:
    # Run the bot
    bot.run_discord_bot()

except Exception as e:
    print("(!) Something went wrong.")
    raise e