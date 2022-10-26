import json

with open("setting.json", mode="r", encoding="utf-8") as jfile:
    jdata = json.load(jfile)

import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(jdata["My_Space_welcome_channel"]))
    await channel.send(f"{member} join!")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(jdata["My_Space_leave_channel"]))
    await channel.send(f"{member} leave!")

@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello, I am KaiYuanite, a robot made by KaiYuanee!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"The ping time is {bot.latency*1000:.2f} (ms).")

bot.run(jdata["TOKEN"])