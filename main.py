import discord
import random

# 必要な設定を定義
ACCESS_TOKEN = 'ODIwMjcwNTYwOTUyMTg4OTQ4.YEyufQ.XtPyfFRuytMTU06fW85jnVbsCVE'
ready_message = "接続し、準備ができました"
bot_ch_id = 813717329296228393

random_contents = [
    "にゃーん",
    "わん！",
    "コケッコッコー",
    "お嬢",
    "みら姉"
]

client = discord.Client()

# アプリスタート時に走るイベント
@client.event
async def on_ready():
    # 起動確認用バージョン情報
    print(ready_message)
    print(discord.__title__ + " ライブラリのバージョン：" + discord.__version__)
    print(discord.__copyright__)

# メッセージ待受イベント
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == "にあちゃん" and message.channel.id == bot_ch_id:
        content = random.choice(random_contents)
        print('チャンネル名：' + str(message.channel))
        print('メッセージ受信を確認。 内容：' + message.content)
        await message.channel.send(content)
        print('反応を送信しました。 内容：' + content)

client.run(ACCESS_TOKEN)
