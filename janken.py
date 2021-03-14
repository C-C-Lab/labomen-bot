from transitions import Machine
import discord
import random
import datetime


# ここからtransitionsの設定
# 状態の定義
states = ['NORMAL_MODE','JANKEN_MODE', 'TIMEOUT']

# 状態変化の定義
transitions = [
    {'trigger':'switch_NORMAL_MODE', 'source':'*', 'dest':'NORMAL_MODE'},
    {'trigger':'switch_JANKEN_MODE', 'source':'*', 'dest':'JANKEN_MODE'},
    {'trigger':'switch_TIMEOUT', 'source':'*', 'dest':'TIMEOUT'},
]

class Model(object):
    pass

mode = Model()
machine = Machine(model=mode, states=states, transitions=transitions, initial=states[0],
                  auto_transitions=False, ordered_transitions=False)

# ここまでtransitionsの設定

# discordの設定
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
    "私の勝ち！",
    "まだまだだね！"
]

janken_lose_mes = [
    "負けちゃった～",
    "くっそー、もう一回！"
]

janeken_favour_mes = [
    "やるね！　あーいこーで……",
    "さすが！　あーいこーで……"
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
    dt_now = str(datetime.datetime.now())

    if message.author.bot:
        return
    # じゃんけんモード
    elif mode.state == 'JANKEN_MODE':
        print('時刻：' + dt_now)
        bot_hand = random.choice(janken_hand)
        if message.channel.id == bot_ch_id:
            # bot勝利ルート
            if message.content == "ぐー" and bot_hand == janken_hand_p \
                    or message.content == "ぱー" and bot_hand == janken_hand_c \
                    or message.content == "ちょき" and bot_hand == janken_hand_g:
                result_mes = random.choice(janken_win_mes)
                await message.channel.send(bot_hand + result_mes)
                print('結果：botの勝ち　じゃんけんモード終了')
                mode.switch_NORMAL_MODE()
            # bot敗北ルート
            elif message.content == "ぐー" and bot_hand == janken_hand_c \
                    or message.content == "ぱー" and bot_hand == janken_hand_g \
                    or message.content == "ちょき" and bot_hand == janken_hand_p:
                result_mes = random.choice(janken_lose_mes)
                await message.channel.send(bot_hand + result_mes)
                print('結果：botの負け　じゃんけんモード終了')
                mode.switch_NORMAL_MODE()
            # あいこルート
            elif message.content in bot_hand:
                result_mes = random.choice(janeken_favour_mes)
                await message.channel.send(bot_hand + result_mes)
                print('結果：あいこ　じゃんけんモード継続')
    # 通常モード
    elif mode.state == 'NORMAL_MODE':
        print('時刻：' + dt_now)
        if message.content == "にあちゃん":
            print('チャンネル名：' + str(message.channel))
            print('チャンネルID: ' + str(message.channel.id))
            print('メッセージ受信：' + message.content)
            if message.channel.id == bot_ch_id:
                content = random.choice(random_contents)
                await message.channel.send(content)
                print('channel idが一致 -> 反応：' + content)
            elif message.channel.id != bot_ch_id:
                print('channel idが不一致 -> 反応なし')
        # じゃんけん起動
        elif message.channel.id == bot_ch_id and 'じゃんけん' in message.content:
            mode.switch_JANKEN_MODE()
            print('じゃんけんモードへ遷移')
            await message.channel.send(random.choice(janken_start_mes))


client.run(ACCESS_TOKEN)
