from transitions import Machine
import discord
import random
import datetime
import pickle
import settings

# ここからtransitionsの設定
# 状態の定義
states = ['NORMAL', 'JANKEN', 'TIMEOUT']

# 状態変化の定義
transitions = [
    {'trigger': 'to_NORMAL', 'source': '*', 'dest': 'NORMAL'},
    {'trigger': 'to_JANKEN', 'source': '*', 'dest': 'JANKEN'},
    {'trigger': 'to_TIMEOUT', 'source': '*', 'dest': 'TIMEOUT'},
]


class Model(object):
    pass


mode = Model()
machine = Machine(model=mode, states=states, transitions=transitions, initial=states[0],
                  auto_transitions=False, ordered_transitions=False)

# ここまでtransitionsの設定

# discordの設定
ACCESS_TOKEN = settings.ACCESS_TOKEN
bot_ch_id = settings.CHANNEL_ID
ready_message = "接続し、準備ができました"

# bot ch in CC
# 813717329296228393
# Discord Test Server
# 817733583833792515

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
    print('現在のモード: ' + mode.state)


# メッセージ待受イベント
@client.event
async def on_message(message):
    print('現在のモード: ' + mode.state)
    dt_now = datetime.datetime.now()

    if message.author.bot:
        return
    else:
        print('時刻：' + str(dt_now))
        with open('timeout.pkl', 'rb') as dt_pkl:
            dt_recent = pickle.load(dt_pkl)
            if dt_now - dt_recent > datetime.timedelta(0, 20):
                print('20秒以上経過　NORMALへ遷移')
                mode.to_NORMAL()
        with open('timeout.pkl', 'wb') as dt_pkl:
            pickle.dump(dt_now, dt_pkl)
        print('チャンネル名：' + str(message.channel))
        print('チャンネルID: ' + str(message.channel.id))
        print('メッセージ受信：' + message.content)
        if message.channel.id == int(bot_ch_id):
            # 通常モード
            if mode.state == 'NORMAL':
                if 'にあちゃん' in message.content:
                    content = random.choice(random_contents)
                    await message.channel.send(content)
                    print('message.channel.id が一致 -> 反応：' + content)
                # じゃんけん起動
                elif 'じゃんけん' in message.content:
                    mode.to_JANKEN()
                    print('JANKENへ遷移')
                    await message.channel.send(random.choice(janken_start_mes))
                else:
                    print('未設定メッセージ -> 反応なし')
            # じゃんけんモード
            elif mode.state == 'JANKEN':
                bot_hand = random.choice(janken_hand)
                # bot勝利ルート
                if message.content == "ぐー" and bot_hand == janken_hand_p \
                        or message.content == "ぱー" and bot_hand == janken_hand_c \
                        or message.content == "ちょき" and bot_hand == janken_hand_g:
                    result_mes = random.choice(janken_win_mes)
                    await message.channel.send(bot_hand + result_mes)
                    print('結果：botの勝ち　NORMALへ遷移')
                    mode.to_NORMAL()
                # bot敗北ルート
                elif message.content == "ぐー" and bot_hand == janken_hand_c \
                        or message.content == "ぱー" and bot_hand == janken_hand_g \
                        or message.content == "ちょき" and bot_hand == janken_hand_p:
                    result_mes = random.choice(janken_lose_mes)
                    await message.channel.send(bot_hand + result_mes)
                    print('結果：botの負け　NORMALへ遷移')
                    mode.to_NORMAL()
                # あいこルート
                elif message.content in bot_hand:
                    result_mes = random.choice(janeken_favour_mes)
                    await message.channel.send(bot_hand + result_mes)
                    print('結果：あいこ　JANKEN継続')
        elif message.channel.id != int(bot_ch_id):
            print('message.channel.id が不一致 -> 反応なし')
            return

client.run(ACCESS_TOKEN)
