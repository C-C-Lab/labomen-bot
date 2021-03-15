import datetime
import os
import random

import discord
from transitions import Machine

from packages import (
    janken,
    settings,
    utilities
)

# ここからtransitionsの設定
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
commands = settings.COMMANDS
janken_start_mes = janken.JANKEN_START_MES
random_contents = settings.RANDOM_CONTENTS

client = discord.Client()


# アプリスタート時に走るイベント
@client.event
async def on_ready():
    utilities.version_check(mode.state)
    PKL_DIR = 'pickles'
    if not os.path.exists(PKL_DIR):
        os.makedirs(PKL_DIR)
    utilities.pkl_dump('timeout', utilities.get_time())


# メッセージ待受イベント
@client.event
async def on_message(message):
    print('現在のモード: ' + mode.state)

    # botの発言を無視
    if message.author.bot:
        return
    else:
        # 20秒経過している場合リセット
        if utilities.get_time() - utilities.pkl_load('timeout') > datetime.timedelta(0, 20):
            print('20秒以上経過　NORMALへ遷移')
            mode.to_NORMAL()
        utilities.pkl_dump('timeout', utilities.get_time())
        utilities.message_info(message)
        if str(message.channel.id) in BOT_CH_IDS:
            # 通常モード
            if mode.state == 'NORMAL':
                if commands['NORMAL'] in message.content:
                    content = random.choice(random_contents)
                    await message.channel.send(content)
                    print('message.channel.id が一致 -> 反応：' + content)
                # じゃんけん起動
                elif commands['JANKEN'] in message.content:
                    mode.to_JANKEN()
                    print('JANKENへ遷移')
                    utilities.pkl_dump(
                        'janken_userid', utilities.get_user_name(message.author))
                    print('ユーザーIDを取得')
                    content = random.choice(janken_start_mes)
                    await message.channel.send(content)
                else:
                    print('未設定メッセージ -> 反応なし')
            # じゃんけんモード
            elif mode.state == 'JANKEN':
                recent_janken_userid = utilities.pkl_load('janken_userid')
                if recent_janken_userid != utilities.get_user_name(message.author) \
                        and utilities.command_check(message.content):
                    await message.channel.send('今別の人と遊んでるの！　ちょっと待ってね！')
                    print('ユーザーIDが不一致(JANKEN)')
                elif message.content in janken.USER_HANDS:
                    await janken.janken_battle(message)
                elif recent_janken_userid == utilities.get_user_name(message.author):
                    await message.channel.send('あれ？　じゃんけんは？')
                    print('回答がJANKEN_HANDSと不一致')
        elif str(message.channel.id) not in BOT_CH_IDS:
            print('message.channel.id が不一致 -> 反応なし')
            return

client.run(ACCESS_TOKEN)
