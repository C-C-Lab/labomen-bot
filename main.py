import datetime
import random

import discord

from settings import bot_words
from settings import discord_settings
from settings import janken_words
from utils import janken
from utils import slv_utils
from utils import util


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
    util.version_check()
    # shelvesディレクトリがない場合は作成
    util.add_dir('shelves')
    print('---------------------------------------')


# メッセージ待受イベント
@ client.event
async def on_message(message):

    # botの発言を無視
    if message.author.bot:
        return
    # 送信者名を取得
    author = message.author
    slv_utils.slv_init(author)
    util.message_info(message)
    # チャンネルIDを照合
    if str(message.channel.id) in BOT_CH_IDS:
        # モード情報を取得
        user_mode = util.get_mode(author)
        # じゃんけんモード判定
        if user_mode == 'janken':
            # 20秒経過している場合normalへ遷移
            try:
                if util.get_now() - slv_utils.slv_load('user_data', author, 'last_update') > datetime.timedelta(0, 20):
                    print('20秒以上経過')
                    slv_utils.slv_save('user_data', author, 'mode', 'normal')
            # mode情報がない場合は例外を無視
            except TypeError:
                pass
            # じゃんけん処理
            if message.content in janken.USER_HANDS:
                await janken.janken_battle(message)
            # USER_HANDSと不一致
            else:
                await util.send_reply(message, 'あれ？　じゃんけんは？')
                print('回答がJANKEN_HANDSと不一致')
                # 発言時刻記録
                slv_utils.slv_save('user_data', author,
                                   'last_update', str(util.get_now()))
        # 通常モード
        else:
            # 鳴き声機能
            if commands['NORMAL'] in message.content:
                content = random.choice(random_contents)
                await message.channel.send(content)
                print('message.channel.id が一致 -> 反応：' + content)
            # じゃんけん起動
            elif commands['JANKEN'] in message.content:
                # モード切替
                slv_utils.slv_save(
                    'user_data', author, 'mode', 'janken')
                # 発言時刻記録
                slv_utils.slv_save('user_data', author,
                                   'last_update', util.get_now())
                # メッセージ送信
                content = random.choice(janken_start_mes)
                await util.send_reply(message, content)
            # 未設定メッセージを受信時
            else:
                print('未設定メッセージ -> 反応なし')
    # チャンネルIDが不一致
    elif str(message.channel.id) not in BOT_CH_IDS:
        print('message.channel.id が不一致 -> 反応なし')
        return
    print('=======================================')


client.run(ACCESS_TOKEN)
