import json
import time
import os
from typing import Dict

import discord
from discord.ext import tasks

from button import commands
from button.utils import format_elapsed_time_short
from button import utils
from button.high_score import HighScore

class ButtonBot(discord.Bot):

    default_button_data = {
        "last_press": time.time(),
        "high_scores": []
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

        self.add_application_command(commands.press)
    
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

                old_high_score_role = member.guild.get_role(existing_high_score["role_id"])
                await old_high_score_role.delete()
            
            else:
                return
        
        formatted_elapsed_time = utils.format_elapsed_time_short(score)

        new_high_score_role = await member.guild.create_role(name=formatted_elapsed_time)

        await member.add_roles(new_high_score_role)

        self.high_scores.append( 
            {
                "member_id": member.id,
                "role_id": new_high_score_role.id,
                "high_score": score
            }
        )

    async def on_ready(self):
        self.update_status.start()
        self.save_data.start()

    @tasks.loop(seconds=5.0)
    async def update_status(self):
        
        elapsed_time = time.time() - self.last_press
        formatted_elapsed_time = format_elapsed_time_short(elapsed_time)

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"for {formatted_elapsed_time}")
        )

    async def save_data(self):

        data = {
            "last_press": self.last_press,
            "high_scores": self.high_scores
        }

        with open(f"{self.button_data_directory}/buttondata.json", "w") as file:
            json.dump(data, file)