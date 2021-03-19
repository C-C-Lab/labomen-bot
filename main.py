import datetime
import random

import discord

from settings import bot_words
from settings import discord_settings
from settings import janken_words
from modules import janken
from modules import slv
from modules import utils

# discordの設定
ACCESS_TOKEN = discord_settings.ACCESS_TOKEN
BOT_CH_IDS = discord_settings.CHANNEL_IDS
commands = bot_words.COMMANDS
janken_start_mes = janken_words.JANKEN_START_MES
random_contents = bot_words.RANDOM_CONTENTS
client = discord.Client()


# アプリスタート時に走るイベント
@client.event
async def on_ready():
    utils.version_check()
    # shelvesディレクトリがない場合は作成
    utils.add_dir('shelves')
    utils.add_dir('shelves/users')
    print('---------------------------------------')


# メッセージ待受イベント
@ client.event
async def on_message(message):

    # botの発言を無視
    if message.author.bot:
        return
    # 送信者名を取得
    author = message.author
    user_name = utils.get_user_name(author)
    user_id = str(message.author.id)
    user_slv = './shelves/users/' + user_id + '.slv'
    slv.initialize_user(author)
    slv.update_value(user_slv, 'data', 'name', user_name)
    utils.message_info(message)
    now = utils.get_now()
    # チャンネルIDを照合
    if str(message.channel.id) in BOT_CH_IDS:
        # モード情報を取得
        user_mode = utils.get_mode(user_id)
        # 20秒経過している場合normalへ遷移
        time_passed = now - slv.get_value(user_slv, 'data', 'last_act_at')
        if time_passed > datetime.timedelta(0, 20):
            print('20秒以上経過')
            slv.update_value(user_slv, 'data', 'mode', 'normal')
            user_mode = 'normal'
        # じゃんけんモード判定
        if user_mode == 'janken':
            # じゃんけん処理
            if message.content in janken.USER_HANDS:
                await janken.janken_battle(message)
            # USER_HANDSと不一致
            else:
                await utils.send_reply(message, 'あれ？　じゃんけんは？')
                print('回答がJANKEN_HANDSと不一致')
                # 発言時刻記録
                slv.update_value(user_slv, 'data', 'last_act_at', now)
        # 通常モード
        elif user_mode == 'normal':
            # 鳴き声機能
            if commands['NORMAL'] in message.content:
                content = random.choice(random_contents)
                await message.channel.send(content)
                print('message.channel.id が一致 -> 反応：' + content)
            # じゃんけん起動
            elif commands['JANKEN'] in message.content:
                # モード切替
                slv.update_value(
                    user_slv, 'data', 'mode', 'janken')
                slv.update_value(user_slv, 'data', 'last_act_at', now)
                # メッセージ送信
                content = random.choice(janken_start_mes)
                await utils.send_reply(message, content)
            # 未設定メッセージを受信時
            else:
                print('未設定メッセージ -> 反応なし')
    # チャンネルIDが不一致
    elif str(message.channel.id) not in BOT_CH_IDS:
        return
    print('=======================================')


client.run(ACCESS_TOKEN)
