import datetime
import random

import discord

from settings import bot_words
from settings import discord_settings
from settings import janken_words
from modules import janken
from modules import omikuji
from modules import slv
from modules import utils

# discordの設定
ACCESS_TOKEN = discord_settings.ACCESS_TOKEN
BOT_CH_IDS = discord_settings.CHANNEL_IDS
bot_commands = bot_words.BOT_COMMANDS
random_contents = bot_words.RANDOM_CONTENTS
client = discord.Client()


# アプリスタート時に走るイベント
@client.event
async def on_ready():
    utils.check_version()
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
    # 変数を定義
    author = message.author
    user_name = utils.get_user_name(author)
    user_id = str(message.author.id)
    user_slv = slv.get_user_slv_path(user_id)
    now = utils.get_now()
    hiragana_content = utils.get_hiragana(message.content)

    # slvに初期項目がなければ追記
    slv.initialize_user(author)
    slv.update_user_value(user_id, 'name', user_name)
    utils.print_message_info(message)
    # チャンネルIDを照合
    if str(message.channel.id) in BOT_CH_IDS:
        # モード情報を取得
        user_mode = utils.get_mode(user_id)
        # 20秒経過している場合normalへ遷移
        time_passed = now - slv.get_value(user_slv, 'data', 'last_act_at')
        if time_passed > datetime.timedelta(0, 20):
            print('20秒以上経過')
            slv.update_user_value(user_id, 'mode', 'normal')
            user_mode = 'normal'
        # じゃんけんモード判定
        if user_mode == 'janken':
            # じゃんけん処理
            user_hands = janken.USER_HANDS
            if utils.check_command(hiragana_content, user_hands):
                await janken.play(message=message)
            # USER_HANDSと不一致
            else:
                ignore_message = random.choice(janken_words.IGNORE_MES)
                await utils.send_reply(message, ignore_message)
                print('回答がJANKEN_HANDSと不一致')
                # 発言時刻記録
                slv.update_user_value(user_id, 'last_act_at', now)
        # 通常モード
        elif user_mode == 'normal':
            # 鳴き声機能
            if bot_commands['NORMAL'] in hiragana_content:
                content = random.choice(random_contents)
                await utils.send_message(message.channel, content)
                print('message.channel.id が一致 -> 反応：' + content)
            # じゃんけん起動
            elif bot_commands['JANKEN'] in hiragana_content:
                await janken.start(user_id, message)
            # おみくじ起動
            elif bot_commands['OMIKUJI'] in message.content:
                await omikuji.play_omikuji(message)
            # 未設定メッセージを受信時
            else:
                print('未設定メッセージ -> 反応なし')
    # チャンネルIDが不一致
    elif str(message.channel.id) not in BOT_CH_IDS:
        return
    print('=======================================')


@ client.event
async def on_reaction_add(reaction, user):

    user_id = str(user.id)
    if user.bot:
        return
    user_mode = utils.get_mode(user_id)
    user_slv = slv.get_user_slv_path(user_id)
    if user_mode == 'janken':
        last_message_id = slv.get_value(user_slv, 'janken', 'last_message_id')
        if str(last_message_id) == str(reaction.message.id):
            await janken.play(user=user, reaction=reaction)


client.run(ACCESS_TOKEN)
