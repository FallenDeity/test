import discord
import os
from typing import *
from discord.ext import commands, tasks
from datetime import datetime, timedelta

client = commands.Bot(command_prefix='!', activity=discord.Activity(type=discord.ActivityType.listening, name="to !help"), intents= discord.Intents.all())

lst: List[int] = []
dct: Dict[int, timedelta] = {}

@client.command()
@commands.is_owner()
async def reminder(ctx: commands.Context) -> Optional[discord.Message]:
    if (x := ctx.author.id) in lst:
        lst.remove(x)
        return await ctx.send("you have been de-registered for reminders")
    lst.append(x)
    await ctx.send("you have been registered for reminders")

@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.id == 853629533855809596 and "is dropping the cards" in message.content:
        userId = ''.join([char for char in message.content if char.isdigit()])
        if (x := int(userId)) in lst:
            dct[x] = datetime.now() + timedelta(minutes = 8)
            await message.add_reaction('👍')
    await client.process_commands(message)

@tasks.loop(seconds=5)
async def background_loop_new():
    await client.wait_until_ready()
    channel = client.get_channel(872000247361065012) or await client.fetch_channel(872000247361065012)
    for k, v in dct.items():
        if datetime.now() > v:
            await channel.send(f"<@{k}> drop your shit")
            
            
client.run(os.getenv('TOKEN'))
