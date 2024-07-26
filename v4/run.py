from secret import LOG_FILE
import bot

try:
    # Run the bot
    bot.run_discord_bot()

except Exception as e:
    print("(!) Something went wrong.")
    raise e