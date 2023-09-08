import bot

if __name__ == '__main__':
  #run the bot
  bot.run_discord_bot()

  print("hi there")
  restart_bot()

def restart_bot():
  os.execv(sys.executable, ['python'] + sys.argv)
