# 此指令必須在 v1.3.0 發布前修復完畢
@bot.command()
async def rdint(ctx):
    try:
        content = ctx.message.content
        contentList = list(map(str, content.split()[1:]))
        if len(contentList) < 2:
            await ctx.send("ERROR：`~rdint`後的參數必須至少有 2 個！")
        else:
            contentList.extend([None] * (4 - len(contentList)))
            if contentList[2] == None: contentList[2] = 1
            if contentList[3] == None: contentList[3] = "true"
            contentList[0], contentList[1], contentList[2] = int(
                contentList[0]), int(contentList[1]), int(contentList[2])
            numList = list()
            contentList[3] = contentList[3].lower()
            if contentList[3] == "true":
                if contentList[2] <= 0 or contentList[2] > 300:
                    await ctx.send("ERROR：隨機數生成數量必須為正整數且不得大於 300 個！")
                numList = [
                    random.randint(contentList[0], contentList[1])
                    for i in range(contentList[2])
                ]
            elif contentList[3] == "false":
                rangeList = [
                    int(x) for x in range(contentList[0], contentList[1] + 1)
                ]
                numList = random.sample(rangeList, contentList[2])
            else:
                await ctx.send("ERROR：第三個參數只能填入 true 或 false (大小寫不影響)！")
            if len(numList) > 0: await ctx.send(f"隨機數字串列: {numList}")
    except:
        if (contentList[0] > 2147483647) or (contentList[0] < -2147483648) or (
                contentList[1] > 2147483647) or (contentList[1] < -2147483648):
            await ctx.send("ERROR：最小值與最大值必須介於 -2147483648 及 2147483647 之間！")
        elif contentList[0] > contentList[1]:
            await ctx.send("ERROR：最小值必須小於或等於最大值！")
        elif contentList[1] - contentList[0] + 1 < contentList[2]:
            await ctx.send("ERROR：欲生成數量大於限定的範圍！")
        else:
            await ctx.send("ERROR：您輸入的指令可能不符合形式或要求超出機器人的負荷！")