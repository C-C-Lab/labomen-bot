import datetime
import pickle

import discord

from packages import (
    settings,
    utilities
)


def command_check(word):
    """有効なコマンドが存在するかをチェックします。

    Args:
        word (str): チェックしたい文字列。

    Returns:
        boolean
    """
    command_words = settings.COMMANDS.values()
    for command in command_words:
        if command in word:
            return True
    else:
        return False


def version_check():
    """起動確認用のバージョン情報を出力します。
    """
    print('---------------------------------------')
    print(settings.READY_MESSAGE)
    print(discord.__title__ + ' ライブラリのバージョン：' + discord.__version__)
    print(discord.__copyright__)
    print('---------------------------------------')


def reset_pkl():
    """.pklをすべて初期化します。
    """
    utilities.pkl_dump('timeout', utilities.get_time())
    utilities.pkl_dump('janken_userid', 'initial value')
    print('.pklを初期化')


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
        str: user.name + '#' + user.discriminator
    """
    return user.name + '#' + user.discriminator


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
    with open('./pickles/' + file + '.pkl', 'wb') as pkl:
        pickle.dump(content, pkl)


def pkl_load(file):
    """.pklからloadします。

    Args:
        file (str): ファイル名

    Returns:
        Any: load内容

    note:
        引数に.pklは不要です。
    """
    with open('./pickles/' + file + '.pkl', 'rb') as pkl:
        return pickle.load(pkl)
