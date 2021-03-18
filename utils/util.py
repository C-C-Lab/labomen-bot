import datetime
import os
import pickle
import traceback

import discord

from settings import discord_settings
from settings import bot_words
from utils import slv_utils
"""
utility.py 自作の便利メソッドをまとめたモジュールです。
"""


def command_check(word):
    """有効なコマンドが存在するかをチェックします。

    Args:
        word (str): チェックしたい文字列。

    Returns:
        boolean
    """
    command_words = bot_words.COMMANDS.values()
    for command in command_words:
        if command in word:
            return True
    else:
        return False


def version_check():
    """起動確認用のバージョン情報を出力します。
    """
    print('---------------------------------------')
    print(discord_settings.READY_MESSAGE)
    print(discord.__title__ + ' ライブラリのバージョン：' + discord.__version__)
    print(discord.__copyright__)
    print('---------------------------------------')


def add_dir(dir):
    """ディレクトリを作成します。

    Args:
        dir (str): 作成したいディレクトリ名
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(dir + "ディレクトリを作成")


def message_info(message):
    """受信メッセージの情報を出力します。

    Args:
      message(Any): Message Model of discord.py
    """
    print('時刻：' + str(get_time()))
    print('チャンネル名：' + str(message.channel))
    print('チャンネルID: ' + str(message.channel.id))
    print('ユーザー名:' + get_user_name(message.author))
    print('メッセージ受信：' + message.content)


def get_user_name(user):
    """discord内のユーザー名を取得します。

    Args:
        user : User Model of discord.py

    Returns:
        str: user.name + '＃' + user.discriminator
    """
    return str(user.name + '＃' + user.discriminator)


def get_time():
    """現在時刻を取得します。

    Returns:
        str: 現在時刻
    """
    return datetime.datetime.now()


def pkl_dump(file, content):
    """.pklへdumpします。

    Args:
        file (str): ファイル名
        content (Any): dump内容

    note:
        引数に.pklは不要です。
    """
    try:
        with open('./pickles/' + file + '.pkl', 'wb') as pkl:
            pickle.dump(content, pkl)
    except Exception as e:
        error_print(e)


def pkl_load(file):
    """.pklからloadします。

    Args:
        file (str): ファイル名

    Returns:
        Any: load内容

    note:
        引数に.pklは不要です。
    """
    try:
        with open('./pickles/' + file + '.pkl', 'rb') as pkl:
            return pickle.load(pkl)
    except Exception as e:
        error_print(e)


def error_print(e):
    """Error内容を出力します。
    """
    print(type(e))
    print(e.args)
    print(e)
    print('トレースバック：' + traceback.format_exc())


def get_mode(mes_author):
    """現在のモードを取得します。

    Args:
        mes_author (str): メッセージ送信者ID

    Returns:
        str: モード名
    """
    user_mode = slv_utils.slv_load('user_data', mes_author, 'mode')
    try:
        print('現在のモード：' + user_mode)
    except KeyError:
        print('現在のモード：None')
    finally:
        return user_mode


async def send_mention(message, content):
    """メンション付メッセージを送信します。

    Args:
        message (Any): Message Model of discord.py
        content (str): メッセージ文
    """
    await message.channel.send(message.author.mention + '\n' + content)


async def send_reply(message, content):
    """リプライメッセージを送信します。

    Args:
        message (Any): Message Model of discord.py
        content (str): メッセージ文
    """
    await message.reply(content, mention_author=True)
