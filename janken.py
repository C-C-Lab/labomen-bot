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

janken_hand = [
    'ぱー！　',
    'ちょき！　',
    'ぐー！　'
]

janken_hand_p = 'ぱー！　'

janken_hand_c = 'ちょき！　'

janken_hand_g = 'ぐー！　'

janken_start_mes = [
    'じゃんけんするんだね？いくよー！じゃんけん……'
]

janken_win_mes = [
    "私の勝ち！"
    "まだまだだね！"
]

janken_lose_mes = [
    "負けちゃった～"
    "くっそー、もう一回！"
]

janeken_favour_mes = [
    "あーいこーで……"
]

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
        bot_hand = random.choice(janken_hand)
        if message.channel.id == bot_ch_id:
            if message.content == "ぐー" and bot_hand == janken_hand_p \
                    or message.content == "ぱー" and bot_hand == janken_hand_c \
                    or message.content == "ちょき" and bot_hand == janken_hand_g:
                await message.channel.send(bot_hand + random.choice(janken_win_mes))
                print('結果：botの勝ち　じゃんけんモード終了')
                model.switch_OFF()
            elif message.content == "ぐー" and bot_hand == janken_hand_c \
                    or message.content == "ぱー" and bot_hand == janken_hand_g \
                    or message.content == "ちょき" and bot_hand == janken_hand_p:
                await message.channel.send(bot_hand + random.choice(janken_lose_mes))
                print('結果：botの負け　じゃんけんモード終了')
                model.switch_OFF()
            elif message.content in bot_hand:
                await message.channel.send(bot_hand + random.choice(janeken_favour_mes))
                print('結果：あいこ　じゃんけんモード継続')
    elif model.state == 'OFF':
        if message.content == "にあちゃん":
            print('チャンネル名：' + str(message.channel))
            print('チャンネルID: ' + str(message.channel.id))
            print('メッセージ受信：' + message.content)
            if message.channel.id == bot_ch_id:
                content = random.choice(random_contents)
                await message.channel.send(content)
                print('IDが一致　反応：' + content)
            elif message.channel.id != bot_ch_id:
                print('IDが不一致')
        elif message.channel.id == bot_ch_id and 'じゃんけん' in message.content:
            model.switch_ON()
            print('じゃんけんモードへ遷移')
            await message.channel.send(random.choice(janken_start_mes))


client.run(ACCESS_TOKEN)


# print(model.state)
# model.switch_ON()
# print(model.state)
# model.switch_OFF()
# print(model.state)
