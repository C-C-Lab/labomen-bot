import datetime
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
    # shelvesディレクトリがない場合は作成
    utilities.add_dir('shelves')
    print('---------------------------------------')


# メッセージ待受イベント
@client.event
async def on_message(message):

    # botの発言を無視
    if message.author.bot:
        return
    else:
        # 送信者名を取得
        mes_author = utilities.get_user_name(message.author)
        utilities.message_info(message)
        # チャンネルIDを照合
        if str(message.channel.id) in BOT_CH_IDS:
            # モード情報を取得
            user_mode = utilities.get_mode(mes_author)
            # じゃんけんモード判定
            if user_mode == 'janken':
                # 20秒経過している場合normalへ遷移
                try:
                    if utilities.get_time() - utilities.slv_load('user_data', mes_author, 'timeout') > datetime.timedelta(0, 20):
                        print('20秒以上経過')
                        utilities.slv_save('user_data', utilities.get_user_name(
                            message.author), 'mode', 'normal')
                # mode情報がない場合は例外を無視
                except TypeError:
                    pass
                # じゃんけん処理
                if message.content in janken.USER_HANDS:
                    await janken.janken_battle(message)
                # USER_HANDSと不一致
                else:
                    await message.channel.send(message.author.mention + '\nあれ？　じゃんけんは？')
                    print('回答がJANKEN_HANDSと不一致')
                    # 発言時刻記録
                    utilities.slv_save('user_data', mes_author,
                                       'timeout', str(utilities.get_time()))
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
                    utilities.slv_save(
                        'user_data', mes_author, 'mode', 'janken')
                    # 発言時刻記録
                    utilities.slv_save('user_data', mes_author,
                                       'timeout', utilities.get_time())
                    # メッセージ送信
                    content = random.choice(janken_start_mes)
                    await message.channel.send(message.author.mention + '\n' + content)
                # 未設定メッセージを受信時
                else:
                    print('未設定メッセージ -> 反応なし')
        # チャンネルIDが不一致
        elif str(message.channel.id) not in BOT_CH_IDS:
            print('message.channel.id が不一致 -> 反応なし')
            return
    print('=======================================')


client.run(ACCESS_TOKEN)
