import json
import time
import os

import discord
from discord.ext import tasks

from button import commands
from button.utils import format_elapsed_time_short

class ButtonBot(discord.Bot):

    default_button_data = {
        "last_press": time.time()
    }

    def __init__(self, description=None, *args, **options):

        super().__init__(description, *args, **options)

        # create button data file if it doesnt already exist
        if not os.path.exists("button_data.json"):
            with open("buttondata.json", "w") as file:
                json.dump(ButtonBot.default_button_data, file)

        with open("buttondata.json", "r") as file:
            data = json.load(file)

        self.last_press: int = data["last_press"]

        self.add_application_command(commands.press)
    
    async def on_ready(self):
        self.update_status.start()
    
    @tasks.loop(seconds=5.0)
    async def update_status(self):
        
        elapsed_time = time.time() - self.last_press
        formatted_elapsed_time = format_elapsed_time_short(elapsed_time)

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"for {formatted_elapsed_time}")
        )