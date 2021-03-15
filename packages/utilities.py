import datetime
import pickle

import discord

from packages import (
    settings,
    utilities
)


# コマンド有無を確認
def command_check(word):
    command_words = settings.COMMANDS.values()
    for command in command_words:
        if command in word:
            return True
    else:
        return False


# 起動確認用バージョン情報
def version_check():
    print('---------------------------------------')
    print(settings.READY_MESSAGE)
    print(discord.__title__ + ' ライブラリのバージョン：' + discord.__version__)
    print(discord.__copyright__)
    print('---------------------------------------')


# .pklの初期化
def reset_pkl():
    """.pklをすべて初期化するメソッドです。
    """
    utilities.pkl_dump('timeout', utilities.get_time())
    utilities.pkl_dump('janken_userid', 'initial value')
    print('.pklを初期化')


# メッセージ受信情報
def message_info(message):
    """受信メッセージの情報を出力するメソッドです。

    Args:
      message(Any): Message Model of discord.py
    """
    print('時刻：' + str(get_time()))
    print('チャンネル名：' + str(message.channel))
    print('チャンネルID: ' + str(message.channel.id))
    print('ユーザー名:' + get_user_name(message.author))
    print('メッセージ受信：' + message.content)


# 送信者名を取得
def get_user_name(user):
    return user.name + '#' + user.discriminator


# 現在時刻を取得
def get_time():
    return datetime.datetime.now()


# pickleへdumpする
def pkl_dump(file, content):
    with open('./pickles/' + file + '.pkl', 'wb') as pkl:
        pickle.dump(content, pkl)


# pickleからloadする
def pkl_load(file):
    with open('./pickles/' + file + '.pkl', 'rb') as pkl:
        return pickle.load(pkl)
