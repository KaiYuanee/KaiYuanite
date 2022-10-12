import discord
from discord.ext import commands
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='~', intents=intents)
@bot.event
async def on_ready():
    print(">> Bot is online <<")
bot.run("MTAyOTcwMDU4MjkyOTM0MjUyNQ.GomMLk.j0yZxbD9Tv_hh2Gcc7ByFS890DzGAFRXd5kxwQ")