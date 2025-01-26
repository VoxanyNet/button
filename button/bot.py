import json
import time
import os
from typing import Dict
import datetime

import discord
from discord.ext import tasks

from button import commands
from button.utils import format_elapsed_time_short
from button import utils
from button.high_score import HighScore

class ButtonBot(discord.Bot):

    default_button_data = {
        "last_press": time.time(),
        "high_scores": [],
        "cooldowns": {}
    }

    def __init__(self, button_data_directory, description=None, *args, **options):

        super().__init__(description, *args, **options)

        self.button_data_directory = button_data_directory

        # create button data file if it doesnt already exist
        if not os.path.exists(f"{self.button_data_directory}/buttondata.json"):

            os.makedirs(self.button_data_directory, exist_ok=True)

            with open(f"{self.button_data_directory}/buttondata.json", "w") as file:
                json.dump(ButtonBot.default_button_data, file)

        with open(f"{self.button_data_directory}/buttondata.json", "r") as file:
            data = json.load(file)

        self.last_press: int = data["last_press"]
        self.high_scores: Dict[HighScore] = data["high_scores"]
        self.last_kick_attempt: int = 0
        self.cooldowns = data["cooldowns"]

        self.add_application_command(commands.press)
        self.add_application_command(commands.highscores)
        self.add_application_command(commands.kickcaiden)
    
    def press_button(self) -> float:

        elapsed_time: float = time.time() - self.last_press

        self.last_press: float = time.time()

        return elapsed_time

    async def update_high_score(self, member: discord.Member, score: float) -> bool:
        """Update high score if member has new high score"""

        query = {
            "member_id": member.id
        }

        existing_high_score: HighScore = utils.find_one(query, self.high_scores)
        
        if existing_high_score:

            if existing_high_score["high_score"] < score:

                utils.delete_one(query, self.high_scores)
            
            else:
                return

        self.high_scores.append( 
            {
                "member_id": member.id,
                "high_score": score
            }
        )

    async def on_ready(self):
        self.update_status.start()
        self.ohboy.start()

    @tasks.loop(seconds=5.0)
    async def update_status(self):
        
        elapsed_time = time.time() - self.last_press

        # sneaky hack for now to get half days
        seconds = int(seconds)
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        formatted_elapsed_time = format_elapsed_time_short(elapsed_time)

        if hours > 12 and days > 1:
            activity_string = f"for {days}.5 days"
        else:
            activity_string = f"for {formatted_elapsed_time}"

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(activity_string)
        )
    
    @tasks.loop(seconds=45)
    async def ohboy(self):
        if datetime.datetime.now().hour == 3 and datetime.datetime.now().minute == 0:
            channel = await self.fetch_channel(945515760409792546)
            await channel.send("https://dl.vxny.io/3am.mp4")

    async def save_data(self):

        data = {
            "last_press": self.last_press,
            "high_scores": self.high_scores,
            "cooldowns": self.cooldowns
        }

        with open(f"{self.button_data_directory}/buttondata.json", "w") as file:
            json.dump(data, file)