from transitions import Machine
import discord
import random

states = ['OFF', 'ON']    #状態の定義

transitions = [
    {'trigger':'switch_ON', 'source':'OFF', 'dest':'ON'},       # 状態OFFからONへの遷移定義
    {'trigger':'switch_OFF', 'source':'ON', 'dest':'OFF'},      # 状態ONからOFFへの遷移定義
]

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

janken_hand = ['パー','チョキ','グー']

client = discord.Client()

class Model(object):
    pass

model = Model()
machine = Machine(model=model, states=states, transitions=transitions, initial=states[0],
                  auto_transitions=False, ordered_transitions=False)

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
    if model.state == 'ON':
     pass
    elif model.state == 'OFF':
        if message.content == "にあちゃん":
          print('チャンネル名：' + str(message.channel))
          print('チャンネルID: ' + str(message.channel.id))
          print('メッセージ受信を確認。 内容：' + message.content)
          if message.channel.id == bot_ch_id and message.content == 'じゃんけん':
             model.switch_ON()
             print('じゃんけんモードに入ります')
             await message.channel.send('じゃんけんするんだね？いくよー！じゃんけん…')
          elif message.channel.id == bot_ch_id:
             content = random.choice(random_contents)
             await message.channel.send(content)
             print('IDが一致したため、反応を送信しました。 内容：' + content)
          elif message.channel.id != bot_ch_id:
             print('IDが一致しないため、返信しませんでした')

client.run(ACCESS_TOKEN)


# print(model.state)
# model.switch_ON()
# print(model.state)
# model.switch_OFF()
# print(model.state)
