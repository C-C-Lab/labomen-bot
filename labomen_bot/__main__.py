from modules import debug
from modules import janken
from modules import omikuji
from modules import slv
from modules import utils
from settings import bot_words
from settings import discord_settings
from settings import dotenv
from settings import janken_words

import datetime
import random
import re

from discord import User, Reaction
from typing import Any

ACCESS_TOKEN = dotenv.ACCESS_TOKEN
BOT_CH_IDS = dotenv.CHANNEL_IDS
GUILDS_IDS_TO_GET_URL = dotenv.GUILDS_IDS_TO_GET_URL
bot_commands = bot_words.BOT_COMMANDS
client = discord_settings.client
random_contents = bot_words.RANDOM_CONTENTS

# アプリスタート時に走るイベント
@client.event
async def on_ready():
    utils.check_version()
    # shelvesディレクトリがない場合は作成
    utils.add_dir('shelves')
    utils.add_dir('shelves/users')
    print('=======================================')


# メッセージ待受イベント
@ client.event
async def on_message(message: Any):

    # botの発言を無視
    if message.author.bot:
        return
    else:
        # 変数を定義
        user: User = message.author
        user_name: str = utils.get_user_name(user)
        user_id = str(user.id)
        user_slv_path = slv.get_user_slv_path(user_id)
        now = utils.get_now()
        content: str = str(message.content)
        hiragana_content = utils.get_hiragana(content)
        guild_id = str(message.guild.id)
        channel_id = str(message.channel.id)
        is_url = True if 'http' in content else False

        # メッセージ内容をコンソールに表示
        utils.print_message_info(message)

        # slvに初期項目がなければ追記
        init_dict = slv.initialize_user(user)
        if init_dict == None:
            user_dict = slv.get_dict(user_slv_path)
        else:
            user_dict = init_dict

        # ユーザ名が以前と違う場合更新
        dict_user_name = user_dict['data']['name']
        if dict_user_name and user_name != dict_user_name:
            old_name = dict_user_name
            user_dict = slv.update_slv_dict(user_dict, 'data', {'name': user_name})
            print('ユーザー名を更新しました: {0} -> {1}'.format(old_name, user_name))

        # モード情報を取得
        user_mode = utils.get_mode(user_dict)

        # 20秒経過している場合normalへ遷移
        last_act_at = slv.get_dict_value(user_dict, 'data', 'last_act_at')
        if isinstance(last_act_at, datetime.datetime):
            time_passed = now - last_act_at
            if time_passed > datetime.timedelta(0, 20) and user_mode != 'normal':
                print('20秒以上経過 -> normalモードへ遷移')
                user_dict = slv.update_slv_dict(user_dict, 'data', {'mode': 'normal'})
                user_mode = 'normal'

        # URL記録機能
        if guild_id in GUILDS_IDS_TO_GET_URL and is_url:
            return

        # チャンネルIDを照合
        if channel_id in BOT_CH_IDS:

            # デバッグコマンド
            debug_response = debug.command_check(user_dict, message)
            if debug_response:
                user_dict = debug_response['user_dict']
                debug_content = debug_response['content']
                if debug_content:
                    return await utils.send_reply(message, debug_content)

            # じゃんけんモード
            if user_mode == 'janken':
                # じゃんけん処理
                user_hands = janken.USER_HANDS
                if utils.check_command(hiragana_content, user_hands):
                    user_dict = await janken.play(user_dict, message=message)
                # USER_HANDSと不一致
                else:
                    ignore_message = random.choice(janken_words.IGNORE_MES)
                    await utils.send_reply(message, ignore_message)
                    print('回答がJANKEN_HANDSと不一致')
                    # 発言時刻記録
                    user_dict = slv.update_slv_dict(user_dict, 'data', {'last_act_at': now})
            # 通常モード
            elif user_mode == 'normal':
                # じゃんけん起動
                if bot_commands['JANKEN'] in hiragana_content:
                    user_dict = await janken.start(user_dict, message)
                # おみくじ起動
                elif bot_commands['OMIKUJI'] in hiragana_content:
                    user_dict = await omikuji.play_omikuji(user_dict, message)
                # ヘルプコマンド
                elif re.search(bot_commands['HELP'], hiragana_content):
                    await utils.send_command_help(message)
                # 鳴き声機能
                elif bot_commands['NORMAL'] in hiragana_content:
                    content = random.choice(random_contents)
                    await utils.send_message(message.channel, content)
                    print('message.channel.id が一致 -> 反応：' + content)
                # メンションされたとき
                elif message.mentions:
                    if message.mentions[0].id == client.user.id:
                        random_mes = random.choice(random_contents)
                        hint_mes = bot_words.HINT_MESSAGE
                        content = '{0}\n{1}'.format(random_mes, hint_mes)
                        await utils.send_reply(message, content)
                # 未設定メッセージを受信時
                else:
                    print('未設定メッセージ -> 反応なし')
        # 最終処理
        user_dict['data']['updated_at'] = now
        slv.merge_dict(user_dict, user_slv_path)
        print('=======================================')


@ client.event
async def on_reaction_add(reaction: Reaction, user: User):
    if user.bot:
        return
    else:
        user_id = str(user.id)
        now = utils.get_now()
        user_slv_path = slv.get_user_slv_path(user_id)
        # slvに初期項目がなければ追記
        init_dict = slv.initialize_user(user)
        if init_dict == None:
            user_dict = slv.get_dict(user_slv_path)
        else:
            user_dict = init_dict
        user_mode = utils.get_mode(user_dict)
        if user_mode == 'janken':
            [last_message_id, reaction_message_id] = [str(user_dict['janken']['last_message_id']), str(reaction.message.id)]
            if last_message_id == reaction_message_id:
                user_dict = await janken.play(user_dict, user=user, reaction=reaction)
        # 最終処理
        user_dict['data']['updated_at'] = now
        slv.merge_dict(user_dict, user_slv_path)


client.run(ACCESS_TOKEN)
