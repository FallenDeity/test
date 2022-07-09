import discord
from discord.ext import commands, tasks
from datetime import datetime
from datetime import timedelta
import os

intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', activity=discord.Activity(type=discord.ActivityType.listening, name="to !help"), intents=intents)

lst = []
dct = {}

@client.command()
@commands.is_owner()
async def reminder(ctx):
    x = ctx.author.id
    if x in lst:
        lst.remove(x)
        await ctx.send("you have been de-registered for reminders")
    else:
        lst.append(x)
        await ctx.send("you have been registered for reminders")

@client.event
async def on_message(message):
    if message.author == 853629533855809596 and "is dropping the cards" in message.content:
        userId = ""
        for char in message.content:
            if char.isdigit():
                userId += char
                if userId in lst:
                    time_now = datetime.now()
                    ping_time = time_now + timedelta(minutes = 8)
                    dct[userId]= ping_time
                    emoji = '\N{THUMBS UP SIGN}'
                    await message.add_reaction(emoji)
    await client.process_commands(message)

@tasks.loop(seconds=5)
async def background_loop_new():
    await client.wait_until_ready()
    channel = client.get_channel(872000247361065012)
    for k, v in dct.items():
        if datetime.now() > v:
            await channel.send(f"<@{k}> drop your shit")
            
            
client.run(os.getenv('TOKEN'))
