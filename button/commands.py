from datetime import timedelta
import time

import discord
import json 

from button.utils import format_elapsed_time

@discord.commands.application_command(description="Press the button")
async def press(ctx: discord.ApplicationContext):

    elapsed_time = time.time() - ctx.bot.last_press
    
    formatted_elapsed_time = format_elapsed_time(elapsed_time)

    await ctx.respond(
        f"<@{ctx.author.id}> pressed the button, ending the streak of **{formatted_elapsed_time}**!"
    )

    ctx.bot.last_press = time.time()

    with open("buttondata.json") as file:
        data = json.load(file)

    with open("buttondata.json", "w") as file:

        data["last_press"] = ctx.bot.last_press

        json.dump(data, file)

