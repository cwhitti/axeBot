from secret import LOG_FILE
import logging
import bot

# Configure logging
logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                    format='%(asctime)s %(levelname)s %(message)s')

if __name__ == '__main__':
    # Log that the bot is starting
    logging.info('Starting client...')

    try:
        # Run the bot
        bot.run_discord_bot()
    except Exception as e:
        # Log any exception that occurs
        logging.exception('An error occurred while running the bot')
