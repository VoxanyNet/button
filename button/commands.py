from datetime import timedelta
from typing import Dict, List
import time
from typing import TYPE_CHECKING

import discord
import json 

from button.utils import format_elapsed_time, format_elapsed_time_short
from button.high_score import HighScore

@discord.commands.application_command(description="Press the button")
async def press(ctx: discord.ApplicationContext):
    
    elapsed_time = ctx.bot.press_button()
    
    await ctx.bot.update_high_score(ctx.author, elapsed_time)

    # send response
    formatted_elapsed_time = format_elapsed_time(elapsed_time)

    await ctx.respond(
        f"<@{ctx.author.id}> pressed the button, ending the streak of **{formatted_elapsed_time}**!"
    )

