# Copyright (C) 2022-2023 KaiYuanee.

import json

with open("setting.json", mode="r", encoding="utf-8") as jfile:
    jdata = json.load(jfile)

with open("elements.json", mode="r", encoding="utf-8") as elements:
    elements = json.load(elements)

import discord
from discord.ext import commands
import random
import datetime
import keep_alive
import pytz
import os
import requests
from replit import db

userList = ["KaiYuanee#9165", "Douglas_Chang#6086"]


def zenquotes():
    url = 'https://zenquotes.io/api/random'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)[0]
        return f">>> {data['q']}\n- {data['a']}"
    else:
        return f"ERROR：API 請求失敗！({response.status_code})"


def exchangerate(amount, init, final):
    try:
        if (amount < 0) or (amount >= 10**16):
            return "ERROR：金額必須為正數且不得大於等於 10 的 16 次方！"
        url = f'https://api.exchangerate-api.com/v4/latest/{init}'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            return f"{data['date']} (UTC)\n{amount:,.3f} {init} ≈ {data['rates'][final] * amount:,.3f} {final}"
        else:
            return f"ERROR：API 請求失敗！({response.status_code})"
    except:
        return "ERROR：您輸入的指令不符合形式或貨幣不存在！"


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)


@bot.event
async def on_ready():
    print(">> Bot is online <<")
    await bot.change_presence(activity=discord.Activity(
        name='~guide', type=discord.ActivityType.playing))


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(jdata["welcome_channel"]))
    await channel.send(f"歡迎 {member} 加入研究院，請至 #研究院守則 閱讀需遵守的事項！")


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(jdata["leave_channel"]))
    await channel.send(f"{member} 離開了研究院，謝謝您曾經在此做出貢獻！")


@bot.command()
async def guide(ctx):
    try:
        content = list(map(str, ctx.message.content.split()))
        if len(content) == 1:
            await ctx.send("""
感謝你瀏覽 KaiYuanite 使用指南！

指令前綴符號：半形波浪號「~」。
所有指令：
`~guide [指令]`：取得使用指南。
`~version`：查看我的目前版本。
`~upgrade [版本]`：查看所有版本更新內容。
`~hi`：說你好，並介紹我自己。
`~ping`：查看目前的 Ping 值。
`~now`：查看目前時間。
`~kaiyuanee`：提供我的作者 KaiYuanee 的 Instagram 帳號連結。
`~rdint [最小值] [最大值] [生成的數量] [是否允許重複]`：我會幫你生成隨機整數。(v1.2.1 起暫時刪除)
`~rickroll`：如果你想被 Rickroll 的話就……使用吧！
`~daily`：進行一次每日運勢的抽籤。
`~gsat [年份]`：取得學測倒數時間。
`~joke`：我會分享一則笑話給你。
`~quote`：我會分享一則格言，如果你需要正能量的話可以使用！
`~rate [金額] [原幣別] [欲兌換幣別]`：我會幫你進行根據今日的匯率進行幣值換算。
`~id [使用者]`：取得任何一位 Discord 使用者的 ID。
`~eco [子指令] …`：用於與經濟系統相關的指令，詳情請至`~guide eco`。
`~element [原子序]`：參數輸入原子序，我會給你關於該元素的資訊。

備註：經濟系統目前還不穩定，仍在測試階段，因此目前建立的所有帳戶僅供試用，之後可能會消失！
            """)
        elif len(content) == 2:
            await ctx.send(f"{jdata['guides'][content[1]]}")
        else:
            await ctx.send("ERROR：`~guide`後的參數最多只能有 1 個！")
    except:
        await ctx.send("ERROR：您輸入的指令不符合形式或欲搜尋的指令不存在！")


@bot.command()
async def version(ctx):
    version = jdata["version"]
    await ctx.send(f"Current version: {version}")


@bot.command()
async def upgrade(ctx):
    try:
        content = list(map(str, ctx.message.content.split()))
        if len(content) == 1:
            output = ""
            for i in jdata['upgrades']:
                output += jdata['upgrades'][i] + "\n\n"
            await ctx.send(output)
        elif len(content) == 2:
            await ctx.send(f"{jdata['upgrades'][content[1]]}")
        else:
            await ctx.send("ERROR：`~upgrade`後的參數最多只能有 1 個！")
    except:
        await ctx.send("ERROR：您輸入的指令不符合形式或欲搜尋的版本不存在！")


@bot.command()
async def hi(ctx):
    await ctx.send(random.choice(jdata["hiList"]))


@bot.command()
async def ping(ctx):
    await ctx.send(f"The ping time is {bot.latency*1000:.2f} (ms).")


@bot.command()
async def now(ctx):
    now = datetime.datetime.now()
    y, m, d, h, mi, s = now.year, now.month, now.day, now.hour, now.minute, now.second
    taipei_now = now + datetime.timedelta(hours=8)
    tpy, tpm, tpd, tph, tpmi, tps = taipei_now.year, taipei_now.month, taipei_now.day, taipei_now.hour, taipei_now.minute, taipei_now.second
    await ctx.send(
        f"Time in Greenwich, London, UK: {y}/{m:02d}/{d:02d}, {h:02d}:{mi:02d}:{s:02d}\nTime in Taipei, Taiwan: {tpy}/{tpm:02d}/{tpd:02d}, {tph:02d}:{tpmi:02d}:{tps:02d}"
    )


@bot.command()
async def kaiyuanee(ctx):
    await ctx.send(jdata["kaiYuanee_instagram"])


@bot.command()
async def rickroll(ctx):
    await ctx.send(
        "Okay. You've been rickrolled!\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )


@bot.command()
async def daily(ctx):
    fortuneList = ["上上"] * 5 + ["上中"] * 10 + ["上下"] * 10 + ["中上"] * 15 + [
        "中"
    ] * 20 + ["中下"] * 15 + ["下上"] * 10 + ["下中"] * 10 + ["下下"] * 5
    await ctx.send(f"{ctx.message.author} 抽到了「{random.choice(fortuneList)}」籤！")


@bot.command()
async def gsat(ctx):
    taipei = pytz.timezone('Asia/Taipei')
    now = datetime.datetime.now(taipei)
    todayDate = datetime.date(now.year, now.month, now.day)
    try:
        content = ctx.message.content
        contentList = list(map(str, content.split()))
        if len(contentList) == 1:
            contentList.append("113")
        if contentList[1] == "113":
            y, m, d = 2024, 1, 19
        elif len(contentList) == 2 and contentList[1] == "114":
            y, m, d = 2025, 1, 17
        else:
            raise Exception
        gsatDate = datetime.datetime(y, m, d, tzinfo=taipei).date()
        days = (gsatDate - todayDate).days
        if days > 0:
            sendContent = f"今天是中華民國 {todayDate.year - 1911} 年 {todayDate.month} 月 {todayDate.day} 日，距離 {contentList[1]} 年學測還剩 {days} 天！"
        elif -2 <= days <= 0:
            sendContent = f"今天是中華民國 {todayDate.year - 1911} 年 {todayDate.month} 月 {todayDate.day} 日，是 {contentList[1]} 年學測的第 {1-days} 天！"
        else:
            sendContent = f"今天是中華民國 {todayDate.year - 1911} 年 {todayDate.month} 月 {todayDate.day} 日，{contentList[1]} 年學測已經過去了 {-2-days} 天！"
        sendContent += f"\n{contentList[1]} 年學測日期：{y}/{m:02d}/{d:02d}" + (
            contentList[1] == "114") * "（暫定）"
        await ctx.send(sendContent)
    except:
        await ctx.send(f"ERROR：輸入的指令不符合形式、該年學測日期未有消息或年份在 112 年以前！")


@bot.command()
async def joke(ctx):
    await ctx.send(random.choice(jdata["jokeList"]))


@bot.command()
async def quote(ctx):
    await ctx.send(zenquotes())


@bot.command()
async def rate(ctx):
    try:
        content = ctx.message.content
        contentList = list(map(str, content.split()[1:]))
        contentList[1] = contentList[1].upper()
        contentList[2] = contentList[2].upper()
        await ctx.send(
            exchangerate(float(contentList[0]), contentList[1],
                         contentList[2]))
    except:
        if len(contentList) < 3:
            await ctx.send("ERROR：`~rate`後的參數必須為 3 個！")
        else:
            await ctx.send("ERROR：您輸入的指令不符合形式！")


@bot.command()
async def eco(ctx):
    content = ctx.message.content
    contentList = list(map(str, content.split()[1:]))
    contentList.extend([None] * (3 - len(contentList)))
    user_id = str(ctx.message.author.id)
    if contentList[0] == "register":
        if user_id not in db["economy"]:
            if db["economy"]["bank"][0] >= 10000:
                db["economy"]["bank"][0] -= 10000
                db["economy"][user_id] = [10000]
                await ctx.send(
                    f"> {ctx.message.author} 成功建立了自己的帳戶，起始餘額為 10,000 元！")
            else:
                await ctx.send("ERROR：銀行已經沒有足夠的錢幫您新增帳戶，請聯繫管理員（KaiYuanee#9165）！"
                               )
        else:
            await ctx.send(f"ERROR：{ctx.message.author} 已經建立帳戶！")
    elif contentList[0] == "balance":
        user = None
        if contentList[1]:
            try:
                user = await ctx.bot.fetch_user(int(contentList[1]))
            except:
                await ctx.send("ERROR：請輸入有效的 ID！")
                return
        else:
            user = ctx.author
        user_id = str(user.id)
        if user_id not in db["economy"]:
            await ctx.send(f"ERROR：{user.name}#{user.discriminator} 沒有建立帳戶！")
            return
        await ctx.send(
            f"{user.name}#{user.discriminator} 目前的餘額是 {db['economy'][user_id][0]:,} 元！"
        )
    elif contentList[0] == "transfer":
        if len(contentList) < 3:
            await ctx.send("ERROR：輸入的指令不完整，必須要有收款人 ID 及匯款金額！")
        else:
            fromUser = user_id
            toUser = contentList[1]
            if toUser not in db["economy"]:
                await ctx.send(f"ERROR：ID = {toUser} 帳戶不存在！")
            else:
                try:
                    amount = int(contentList[2])
                    if amount <= 0:
                        await ctx.send(f"ERROR：轉帳金額必須為正整數！")
                    elif amount >= 10**16:
                        await ctx.send(f"ERROR：轉帳金額不能大於等於 10 的 16 次方！")
                    elif db["economy"][fromUser][0] < amount:
                        await ctx.send(
                            f"ERROR：{ctx.message.author} 的餘額不足，轉帳失敗！")
                    else:
                        db["economy"][fromUser][0] -= amount
                        db["economy"][toUser][0] += amount
                        await ctx.send(
                            f"> {ctx.message.author} 成功將 {amount:,} 元轉帳給 ID = {toUser} 帳戶！"
                        )
                except ValueError:
                    await ctx.send(f"ERROR：轉帳金額必須為正整數！")
    else:
        await ctx.send("ERROR：`~eco`並不包含這個子指令")
    """
    elif contentList[0] == "delete":
        user = None
        if contentList[1]:
            try:
                user = await commands.UserConverter().convert(
                    ctx, contentList[1])
            except commands.errors.UserNotFound:
                try:
                    user = await commands.MemberConverter().convert(
                        ctx, contentList[1])
                except commands.errors.MemberNotFound:
                    pass
        if not user:
            user = ctx.author
        user_id = str(user.id)
        if user_id in db["economy"]:
            del db["economy"][user_id]
            await ctx.send(f"> {ctx.message.author} 的帳戶已經被刪除！")
        else:
            await ctx.send(f"ERROR：{ctx.message.author} 沒有建立帳戶！")
    """


@bot.command()
async def id(ctx, user: discord.Member = None):
    """
    Get the user ID of a specified member or the command caller.

    Usage: !id [member]
    """
    if user is None:
        user = ctx.author
    try:
        await ctx.send(f"{user.name}#{user.discriminator} 的使用者 ID 是 {user.id}！"
                       )
    except discord.HTTPException:
        await ctx.send("ERROR：無法發送訊息，請稍後再試。")
    except AttributeError:
        await ctx.send("ERROR：找不到指定的成員，請確認輸入是否正確。")
    except Exception as e:
        await ctx.send(f"ERROR：發生了一些錯誤！({e})")


@bot.command()
async def element(ctx):
    content = ctx.message.content
    contentList = list(map(str, content.split()))
    if len(contentList) != 1:
        if contentList[1] in elements:
            output = ""
            for i in elements[contentList[1]]:
                output += elements[contentList[1]][i] + '\n'
            await ctx.send(output)
        else:
            await ctx.send(
                f"ERROR：找不到原子序 {contentList[1]} 的元素，可能是該元素還未被加入至資料庫、該元素尚未被科學界找到、輸入含有非法字元或輸入的數字非正整數！"
            )
    else:
        await ctx.send("ERROR：`~element`後必須要接上`[原子序]`參數！")


# Easter egg
@bot.command()
async def zen(ctx):
    await ctx.send("""
>>> In the world of Discord bots,
With the prefix of a tilde,
I am here to serve you,
And with my functions abide.

You can ask for my guide,
And know my every move,
My version and upgrades,
Are there for you to approve.

Say hi and I'll greet you,
And my Ping value I'll show,
If you need the current time,
Just let me know.

My creator KaiYuanee,
Has an Instagram account to follow,
And if you want some random numbers,
I can make them with ease, just swallow.

If you want to get Rickrolled,
Just use my command with care,
For a daily dose of fortune,
My lottery can take you there.

If you need to know the countdown,
To the GSAT examination day,
I can help with the time,
And show it to you without delay.

I can share a joke or a quote,
To brighten up your day,
And with my rate conversion,
I can make your currency play.

So come and use my features,
And let me be of help,
For I am here to serve you,
And always be at your yelp.


The zen was generated by ChatGPT on March 7, 2023.
    """)


# Author only
@bot.command()
async def say(ctx):
    user = str(ctx.message.author)
    if user in userList:
        if len(ctx.message.content) > 5:
            content = ctx.message.content[5:]
            await ctx.send(content)
        else:
            await ctx.send("ERROR：您輸入的指令不符合形式或內容為空！")
    else:
        await ctx.send("ERROR：您沒有權限使用該指令！")


@bot.command()
async def allacc(ctx):
    user = str(ctx.message.author)
    if user in userList:
        output = "以下是所有帳戶的餘額：\n\n"
        totalExistMoney = 0
        totalInCirculationMoney = 0
        for key in db["economy"].keys():
            if key == "bank":
                output += f"銀行金庫：{db['economy'][key][0]:,}" + '\n'
                totalInCirculationMoney += db["economy"][key][0]
            else:
                member = await bot.fetch_user(int(key))
                output += f"{member.name}#{member.discriminator}：{db['economy'][key][0]:,}" + '\n'
                totalExistMoney += db["economy"][key][0]
                totalInCirculationMoney += db["economy"][key][0]
        output += "\n總流通金額：" + "{:,}".format(totalExistMoney) + " 元"
        output += "\n總存在金額：" + "{:,}".format(totalInCirculationMoney) + " 元"
        await ctx.send(output)
    else:
        await ctx.send("ERROR：您沒有權限使用該指令！")


keep_alive.keep_alive()
bot.run(os.environ['TOKEN'])
