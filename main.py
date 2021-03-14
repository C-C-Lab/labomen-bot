import discord
import random

# 必要な設定を定義
ACCESS_TOKEN = 'ODIwMjcwNTYwOTUyMTg4OTQ4.YEyufQ.XtPyfFRuytMTU06fW85jnVbsCVE'
ready_message = "接続し、準備ができました"
# CC botチャンネル
# bot_ch_id = 813717329296228393
# Discord Test Server
bot_ch_id = 817733583833792515

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
    if message.content == "にあちゃん":
        print('チャンネル名：' + str(message.channel))
        print('チャンネルID: ' + str(message.channel.id))
        print('メッセージ受信を確認。 内容：' + message.content)
        if message.channel.id == bot_ch_id:
           content = random.choice(random_contents)

           await message.channel.send(content)
           print('IDが一致したため、反応を送信しました。 内容：' + content)
        elif message.channel.id != bot_ch_id:
           print('IDが一致しないため、返信しませんでした')

client.run(ACCESS_TOKEN)
