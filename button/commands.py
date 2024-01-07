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

    await ctx.bot.save_data()

@discord.commands.application_command(description="Display high scores")
async def highscores(ctx: discord.ApplicationContext):

    high_scores_embed = discord.Embed(title="High Scores")

    sorted_high_scores = sorted(
        ctx.bot.high_scores,
        key = lambda high_score: high_score["high_score"],
        reverse=True
    )

    print(sorted_high_scores)

    for high_score in sorted_high_scores:
        high_score: HighScore

        member = await ctx.guild.fetch_member(high_score["member_id"])
        
        formatted_high_score = format_elapsed_time(high_score["high_score"])

        high_scores_embed.add_field(
            name = formatted_high_score,
            value = member.mention,
            inline=False
        )
    
    await ctx.respond(embed=high_scores_embed)


