from secret import LOG_FILE
import logging
import v4.bot as bot
import sys

debug = False

RED = "\033[31m"
RESET = "\033[0m"

# Configure logging
logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s')

# Log that the bot is starting
logging.info('Starting client...')

try:
    # Run the bot
    bot.run_discord_bot(logging)

except Exception as e:
    if debug:
        raise e
    # Log any exception that occurs
    logging.exception('An error occurred while running the bot')

finally:
    # Log the shutdown message
    logging.info(f'BOT SHUTDOWN')
    sys.exit()
