import os

from button import bot

BOT_DISCORD_TOKEN = os.environ["BOT_DISCORD_TOKEN"] 
BOT_DATA_DIRECTORY = os.environ["BOT_DATA_DIRECTORY"]

bot = bot.ButtonBot(BOT_DATA_DIRECTORY)

bot.run(BOT_DISCORD_TOKEN)