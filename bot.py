import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1025716914770681886)
    await channel.send(f"{member} join!")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1030103209609527306)
    await channel.send(f"{member} leave!")

bot.run("MTAyOTcwMDU4MjkyOTM0MjUyNQ.GomMLk.j0yZxbD9Tv_hh2Gcc7ByFS890DzGAFRXd5kxwQ")