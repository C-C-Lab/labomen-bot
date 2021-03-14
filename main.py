from transitions import Machine
import discord
import random
import datetime
import pickle
import settings

states = settings.STATES
transitions = settings.TRAMSITIONS


class Model(object):
    pass


mode = Model()
machine = Machine(model=mode, states=states, transitions=transitions, initial=states[0],
                  auto_transitions=False, ordered_transitions=False)

# ここまでtransitionsの設定

# discordの設定
ACCESS_TOKEN = settings.ACCESS_TOKEN
BOT_CH_IDS = settings.CHANNEL_IDS
ready_message = settings.READY_MESSAGE
random_contents = settings.RANDOM_CONTENTS
janken_hands = settings.JANKEN_HANDS
janken_hand_p = settings.JANKEN_HAND_P
janken_hand_c = settings.JANKEN_HAND_C
janken_hand_g = settings.JANKEN_HAND_G
janken_start_mes = settings.JANKEN_START_MES
janken_win_mes = settings.JANKEN_WIN_MES
janken_lose_mes = settings.JANKEN_LOSE_MES
janeken_favour_mes = settings.JANKEN_FAVOUR_MES

client = discord.Client()


# アプリスタート時に走るイベント
@client.event
async def on_ready():
    # 起動確認用バージョン情報
    print(ready_message)
    print(discord.__title__ + " ライブラリのバージョン：" + discord.__version__)
    print(discord.__copyright__)
    print('現在のモード: ' + mode.state)
    with open('timeout.pkl', 'wb') as dt_pkl:
        pickle.dump(datetime.datetime.now(), dt_pkl)


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
        if str(message.channel.id) in BOT_CH_IDS:
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
                bot_hand = random.choice(janken_hands)
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
        elif str(message.channel.id) not in BOT_CH_IDS:
            print('message.channel.id が不一致 -> 反応なし')
            return

client.run(ACCESS_TOKEN)
