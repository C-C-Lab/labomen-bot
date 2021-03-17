import datetime
import os
import pickle
import shelve
import traceback

import discord

from packages import settings
"""
utility.py 自作の便利関数をまとめたモジュールです。
"""


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
        str: user.name + '#' + user.discriminator
    """
    return str(user.name + '#' + user.discriminator)


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


def error_print(e):
    print(type(e))
    print(e.args)
    print(e)
    print('トレースバック：' + traceback.format_exc())


def slv_save(file, user, key, content):
    """shelveに情報を記録します。

    Args:
        file (str): shelveファイル名
        user (str): ユーザー名
        key (str): key
        content (any): 記録内容
    """
    print('---------------------------------------')
    s = shelve.open('./shelves/' + file + '.shelve')
    print(file + 'に記録')
    try:
        if user in s:
            data = s[user]
            data[key] = content
            s[user] = data
            print(user + 'の' + key + 'を変更 -> ' + str(content))
        else:
            s[user] = {key: content}
            print(user + 'の項目を作成')
            print(key + ' -> ' + str(content))
        s.close()
    except OSError as e:
        print('-----OSError-----')
        error_print(e)
    except LookupError as e:
        print('-----LookupError-----')
        error_print(e)
    except Exception as e:
        print('-----Error-----')
        error_print(e)


def slv_load(file, user, key):
    """shelveから情報を取得します。

    Args:
        file (str): shelveファイル名
        user (str): ユーザー名
        key (str): key

    Returns:
        any: value
    """
    print('---------------------------------------')
    try:
        s = shelve.open('./shelves/' + file + '.shelve')
        print(file + 'を参照')
        data = s[user]
        s.close()
        print(user + ':' + key + ' -> ' + str(data[key]))
        return data[key]
    except OSError as e:
        print('-----OSError-----')
        error_print(e)
    except KeyError:
        print('key情報なし')
    except Exception as e:
        print('-----Error-----')
        error_print(e)


def get_mode(mes_author):
    """現在のモードを取得します。

    Args:
        mes_author (str): メッセージ送信者ID

    Returns:
        str: モード名
    """
    user_mode = slv_load('user_data', mes_author, 'mode')
    try:
        print('現在のモード：' + user_mode)
    except KeyError:
        print('現在のモード：None')
    finally:
        return user_mode
