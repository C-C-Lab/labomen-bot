import datetime
import os
import random

import discord

from packages import (
    janken,
    settings,
    utilities
)

# discordの設定
ACCESS_TOKEN = settings.ACCESS_TOKEN
BOT_CH_IDS = settings.CHANNEL_IDS
commands = settings.COMMANDS
janken_start_mes = janken.JANKEN_START_MES
random_contents = settings.RANDOM_CONTENTS

client = discord.Client()


# アプリスタート時に走るイベント
@client.event
async def on_ready():
    utilities.version_check()
    PKL_DIR = 'pickles'
    if not os.path.exists(PKL_DIR):
        os.makedirs(PKL_DIR)
    # 各pklファイルを初期化
    utilities.pkl_dump('timeout', utilities.get_time())
    utilities.pkl_dump('janken_userid', 'initial value')


# メッセージ待受イベント
@client.event
async def on_message(message):

    # botの発言を無視
    if message.author.bot:
        return
    else:
        # 20秒経過している場合リセット
        if utilities.get_time() - utilities.pkl_load('timeout') > datetime.timedelta(0, 20):
            utilities.pkl_dump('janken_userid', 'initial value')
            print('20秒以上経過')
            print('じゃんけんユーザーIDを初期化')
        utilities.pkl_dump('timeout', utilities.get_time())
        utilities.message_info(message)
        if str(message.channel.id) in BOT_CH_IDS:
            recent_janken_userid = utilities.pkl_load('janken_userid')
            # ユーザーがじゃんけん中か判定
            if recent_janken_userid == utilities.get_user_name(message.author):
                # じゃんけん処理
                if message.content in janken.USER_HANDS:
                    await janken.janken_battle(message)
                # USER_HANDSと不一致
                else:
                    await message.channel.send('あれ？　じゃんけんは？')
                    print('回答がJANKEN_HANDSと不一致')
            # 通常モード
            else:
                # 鳴き声機能
                if commands['NORMAL'] in message.content:
                    content = random.choice(random_contents)
                    await message.channel.send(content)
                    print('message.channel.id が一致 -> 反応：' + content)
                # じゃんけん起動
                elif commands['JANKEN'] in message.content:
                    utilities.pkl_dump(
                        'janken_userid', utilities.get_user_name(message.author))
                    print('じゃんけんユーザーIDを取得')
                    content = random.choice(janken_start_mes)
                    await message.channel.send(content)
                # 未設定メッセージを受信時
                else:
                    print('未設定メッセージ -> 反応なし')
        # チャンネルIDが不一致
        elif str(message.channel.id) not in BOT_CH_IDS:
            print('message.channel.id が不一致 -> 反応なし')
            return
    print('---------------------------------------')

client.run(ACCESS_TOKEN)
