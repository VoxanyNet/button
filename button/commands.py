import random
import time
import asyncio

import discord

from button.utils import format_elapsed_time
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

@discord.commands.application_command(description="1% chance of kicking Caiden")
async def kickcaiden(ctx: discord.ApplicationContext):
    
    try:
        last_attempt: int = ctx.bot.cooldowns[ctx.author.id]
    except KeyError:
        last_attempt = 0
        pass

    time_since_last_kick = time.time() - last_attempt

    if time_since_last_kick < 60 * 720:

        time_until_next_kick_attempt = (60*720) - time_since_last_kick

        await ctx.respond(f"On cooldown, **{format_elapsed_time(time_until_next_kick_attempt)}** until you can try again.", ephemeral=True)

        return 
    
    kick_caiden = random.randrange(0, 100) == 1

    kick_interaction = await ctx.respond("🚨 Attempting to kick Caiden...")

    await asyncio.sleep(1)

    for i in reversed(range(3)):
        await kick_interaction.edit_original_response(content=f"🚨 Attempting to kick Caiden...\n\n**{i+1}**...")

        await asyncio.sleep(1)
    
    if kick_caiden:
        await kick_interaction.edit_original_response(content="🎉 **SUCCESSFULLY KICKED CAIDEN!** 🎉")

        asyncio.sleep(3)

        caiden_jones = await ctx.guild.fetch_member(763861457993334795)

        await ctx.bot.update_high_score(caiden_jones, 0)

        await caiden_jones.kick()
    
    if not kick_caiden:

        await kick_interaction.edit_original_response(content="❌ Failed to kick Caiden...")

    ctx.bot.cooldowns[ctx.author.id] = time.time()




