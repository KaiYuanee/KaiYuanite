import json

with open("setting.json", mode="r", encoding="utf-8") as jfile:
    jdata = json.load(jfile)

import discord
from discord.ext import commands
import random
import datetime
import time

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
async def guide(ctx):
    content = """
感謝你瀏覽 KaiYuanite 使用指南！
指令前綴符號：半形波浪號「~」
所有指令：
`~guide`：取得使用指南
`~hi`：說你好，並介紹我自己。
`~ping`：查看目前的 Ping 值。
`~kaiyuanee`：提供我的作者 KaiYuanee 的 Instagram 帳號連結。
`~int_rand`：後面需加上 2 個整數參數，我會幫你在這兩個整數中隨機取出一個整數。
`~rickroll`：如果你想被 Rickroll 的話就...使用吧！
`~daily_fortune`：取得你的每日運勢。運勢共有 7 種，分別為「大吉」(5%)、「吉」(10%)、「中吉」(15%)、「小吉」(25%)、「末吉」(25%)、「凶」(15%)、「大凶」(5%)。僅供參考，請勿迷信！
`~gsat_timer`：取得學測倒數時間。
    """
    await ctx.send(content)


@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello, I am KaiYuanite, a robot made by KaiYuanee!")


@bot.command()
async def ping(ctx):
    await ctx.send(f"The ping time is {bot.latency*1000:.2f} (ms).")


@bot.command()
async def kaiyuanee(ctx):
    await ctx.send(jdata["35p_kaiYuanee_instagram"])


@bot.command()
async def int_rand(ctx):
    try:
        content = ctx.message.content
        contentList = list(map(int, content.split()[1:]))
        mi, ma = min(contentList), max(contentList)
        if len(contentList) == 2:
            await ctx.send(f"Random integer: {random.randint(mi, ma)}")
        else:
            await ctx.send(f"There must be 2 integers following \"~int_rand\"!")
    except:
        await ctx.send("The command contains some errors!")


@bot.command()
async def rickroll(ctx):
    await ctx.send("Okay. You've been rickrolled!\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ")


@bot.command()
async def daily_fortune(ctx):
    fortuneList = ["大吉"] * 5 + ["吉"] * 10 + ["中吉"] * 15 + \
        ["小吉"] * 25 + ["末吉"] * 25 + ["凶"] * 15 + ["大凶"] * 5
    await ctx.send(f"@{ctx.message.author} 的每日運勢：{random.choice(fortuneList)}")

@bot.command()
async def gsat_timer(ctx):
    yt, mt, dt = time.localtime(time.time()).tm_year, time.localtime(time.time()).tm_mon, time.localtime(time.time()).tm_mday
    todayDate = datetime.date(yt, mt, dt)
    gsatDate = datetime.date(2024, 1, 19)
    days = (gsatDate - todayDate).days
    if days > 0:
        await ctx.send(f"今天是中華民國 {yt - 1911} 年 {mt} 月 {dt} 日，距離 113 年學測還剩 {days} 天！")
    elif -2 <= days <= 0:
        await ctx.send(f"今天是中華民國 {yt - 1911} 年 {mt} 月 {dt} 日，是 113 年學測的第 {1-days} 天！")
    else:
        await ctx.send(f"今天是中華民國 {yt - 1911} 年 {mt} 月 {dt} 日，113 年學測已經過去了 {-2-days} 天！")
bot.run(jdata["TOKEN"])
