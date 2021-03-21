"""
自作の便利メソッドをまとめたモジュールです。
"""
import datetime
import os
import pickle
import traceback

import discord
import jaconv

from settings import discord_settings
from modules import slv


def check_command(word, command_words):
    """有効なコマンドが存在するかをチェックします。

    Args:
        word (str): チェックしたい文字列。
        command_words (set): コマンド一覧を含むsetオブジェクト

    Returns:
        bool
    """
    for command in command_words:
        if command in word:
            return True
    else:
        return False


def get_command(word, command_words):
    """文字列に有効なコマンドが含まれていれば該当コマンドを取得します。

    Args:
        word (str): チェックしたい文字列。
        command_words (set): コマンド一覧を含むsetオブジェクト

    Returns:
        str: コマンド
    """
    for command in command_words:
        if command in word:
            return command
    else:
        return None


def check_version():
    """起動確認用のバージョン情報を出力します。
    """
    print('---------------------------------------')
    print(discord_settings.READY_MESSAGE)
    print(discord.__title__ + ' ライブラリのバージョン：' + discord.__version__)
    print(discord.__copyright__)
    print('---------------------------------------')


def add_dir(dir_name):
    """ディレクトリを作成します。

    Args:
        dir_name (str): 作成したいディレクトリ名
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(dir_name + "ディレクトリを作成")


def print_message_info(message):
    """受信メッセージの情報を出力します。

    Args:
      message(Any): discord.pyのmessageモデル
    """
    print('時刻:' + str(get_now()))
    print('チャンネル名:' + str(message.channel))
    print('チャンネルID: ' + str(message.channel.id))
    print('ユーザー名:' + get_user_name(message.author))
    print('ユーザーID:' + str(message.author.id))
    print('メッセージ受信:' + message.content)


def get_user_name(user):
    """discord内のユーザー名を取得します。

    Args:
        user : discord.pyのuserモデル

    Returns:
        str: user.name + '_' + user.discriminator
    """
    return str(user.name + '_' + user.discriminator)


def get_now():
    """現在時刻を取得します。

    Returns:
        datetime: 現在時刻
    """
    now = datetime.datetime.now()
    return now


def save_pkl(file_name, content):
    """pklへ記録します。

    Args:
        file_name (str): ファイル名
        content (Any): 記録内容
    """
    try:
        with open('./pickles/' + file_name + '.pkl', 'wb') as pkl:
            pickle.dump(content, pkl)
    except Exception as e:
        print_error(e)


def get_pkl(file_name):
    """pklから内容を取得します。

    Args:
        file_name (str): ファイル名

    Returns:
        Any: 取得内容
    """
    try:
        with open('./pickles/' + file_name + '.pkl', 'rb') as pkl:
            return pickle.load(pkl)
    except Exception as e:
        print_error(e)


def print_error(e):
    """Error内容を出力します。
    """
    print(type(e))
    print(e.args)
    print(e)
    print('トレースバック：' + traceback.format_exc())


def get_mode(user_id):
    """現在のモードをslvから取得します。

    Args:
        user_id (str): user_id

    Returns:
        str: モード名
    """
    slv_path = slv.get_user_slv_path(user_id)
    user_mode = slv.get_value(slv_path, 'data', 'mode')
    print('現在のモード：' + user_mode)
    return user_mode


async def send_mention(message, content, user=None):
    """メンション付メッセージを送信します。

    Args:
        message (message): discord.pyのmessageモデル
        content (str): メッセージ文
        user (user): discordのuserモデル

    Returns:
        message: discord.pyのmessageモデル
    """
    if not user:
        user = message.author
    try:
        response = await message.channel.send(user.mention + '\n' + content)
    except Exception as e:
        print('-----メンション送信に失敗-----')
        print_error(e)
    return response


async def send_reply(message, content):
    """リプライメッセージを送信します。
    送信したメッセージのモデルを返します。

    Args:
        message (Any): discord.pyのmessageモデル
        content (str): メッセージ文

    Returns:
        message: discord.pyのmessageモデル
    """
    try:
        response = await message.reply(content, mention_author=True)
    except Exception as e:
        print('-----リプライ送信に失敗-----')
        print_error(e)
    return response


async def send_message(channel, content):
    """メッセージを送信します。

    Args:
        channel (Any): discord.pyのchannelモデル
        content (str): メッセージ文

    Returns:
        message: discord.pyのmessageモデル
    """
    try:
        response = await channel.send(content)
    except Exception as e:
        print('-----メッセージ送信に失敗-----')
        print_error(e)
    return response


def get_hiragana(word):
    """文字列をひらがなに変換します。

    Args:
        word (str): 変換する文字列

    Returns:
        str: ひらがな文字列
    """
    converted_word = jaconv.kata2hira(word)
    return converted_word


async def add_reaction_list(message, emoji_list):
    """リスト内のemojiをリアクションとして一括送信します。

    Args:
        message (message): discord.pyのmessageモデル
        emoji_list (list): emojiのlist
    """
    for emoji in emoji_list:
        await message.add_reaction(emoji)


def get_key_from_value(dict_name, target_value):
    """dictのvalueからkeyを取得します。

    Args:
        dict_name (str): dict名
        target_value (Any): 鍵となるvalue

    Returns:
        Any: key
    """
    for key, value in dict_name.items():
        if value == target_value:
            return key


def get_text(file_name):
    """指定したテキストファイルを改行で区切ってリストに変換して返します。

    Args:
        file_name (str): 対象の拡張子を除いたファイル名

    Returns:
        list: 改行で区切った文字列のリスト
    """
    text_directory = './texts'
    path = text_directory + '/' + file_name + '.txt'
    try:
        with open(path, 'r') as txt:
            word_list = txt.read().split("\n")
            normalized_list = list(set(filter(None, word_list)))
            comment_list = [s for s in normalized_list if s.startswith('#')]
            _list = list(set(normalized_list) - set(comment_list))
            return _list
    except OSError as e:
        print(e)
    except Exception as e:
        print(e)
