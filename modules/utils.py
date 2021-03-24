"""
自作の便利メソッドをまとめたモジュールです。
"""
import datetime
import os
import pickle
import traceback
from typing import Tuple, Union
from typing import Any

import discord
import jaconv

from settings import discord_settings
from modules import slv


def check_command(word: str, command_words: Union[list, dict]) -> bool:
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


def get_command(word: str, command_words: Union[dict, list]) -> Union[str, None]:
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


def add_dir(dir_name: str):
    """ディレクトリを作成します。

    Args:
        dir_name (str): 作成したいディレクトリ名
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(dir_name + "ディレクトリを作成")


def print_message_info(message: Any):
    """受信メッセージの情報を出力します。

    Args:
      message(message): discord.pyのmessageモデル
    """
    print('時刻:' + str(get_now()))
    print('チャンネル名:' + str(message.channel))
    print('チャンネルID: ' + str(message.channel.id))
    print('ユーザー名:' + get_user_name(message.author))
    print('ユーザーID:' + str(message.author.id))
    print('メッセージ受信:' + message.content)


def get_user_name(user: discord.User) -> str:
    """discord内のユーザー名を取得します。

    Args:
        user : discord.pyのuserモデル

    Returns:
        str: user.name + '_' + user.discriminator
    """
    return str(user.name + '_' + user.discriminator)


def get_now() -> datetime.datetime:
    """現在時刻を取得します。

    Returns:
        datetime: 現在時刻
    """
    now = datetime.datetime.now()
    return now


def save_pkl(file_name: str, content: Any):
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


def get_pkl(file_name: str) -> Any:
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


def print_error(error):
    """Error内容を出力します。
    """
    print(type(error))
    print(error.args)
    print(error)
    print('トレースバック：' + traceback.format_exc())


def get_mode(user_dict: dict) -> str:
    """現在のモードをslvから取得します。

    Args:
        user_dict (dict): user_slvから取り出したdict

    Returns:
        str: モード名
    """
    user_mode = slv.get_dict_value(user_dict, 'data', 'mode')
    print('現在のモード：' + user_mode)
    return user_mode


async def send_mention(message: Any, content: str, user: Union[discord.User, discord.Member] = None):
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
        return response
    except Exception as e:
        print('-----メンション送信に失敗-----')
        print_error(e)


async def send_reply(message: Any, content: str):
    """リプライメッセージを送信します。
    送信したメッセージのモデルを返します。

    Args:
        message (message): discord.pyのmessageモデル
        content (str): メッセージ文

    Returns:
        message: discord.pyのmessageモデル
    """
    try:
        response = await message.reply(content, mention_author=True)
        return response
    except Exception as e:
        print('-----リプライ送信に失敗-----')
        print_error(e)


async def send_message(channel: discord.TextChannel, content: str):
    """メッセージを送信します。

    Args:
        channel (TextChannel): discord.pyのchannelモデル
        content (str): メッセージ文

    Returns:
        message: discord.pyのmessageモデル
    """
    try:
        response = await channel.send(content)
        return response
    except Exception as e:
        print('-----メッセージ送信に失敗-----')
        print_error(e)


async def send_command_help(message):
    try:
        with open('./texts/help.txt', 'r') as txt:
            help_txt = txt.read()
        await send_message(message.channel, help_txt)
    except OSError as e:
        print(e)
    except Exception as e:
        print(e)


def get_hiragana(word: str) -> str:
    """文字列をひらがなに変換します。

    Args:
        word (str): 変換する文字列

    Returns:
        str: ひらがな文字列
    """
    converted_word = jaconv.kata2hira(word)
    return converted_word


async def add_reaction_list(message: Any, emoji_list: list):
    """リスト内のemojiをリアクションとして一括送信します。

    Args:
        message (message): discord.pyのmessageモデル
        emoji_list (list): emojiのlist
    """
    for emoji in emoji_list:
        await message.add_reaction(emoji)


def get_key_from_value(dict_name: dict, target_value: Any) -> Union[str, int]:
    """dictのvalueからkeyを取得します。

    Args:
        dict_name (dict): dict
        target_value (Any): 鍵となるvalue

    Returns:
        str or int: key()
    """
    for key, value in dict_name.items():
        if value == target_value:
            return key
    return ''


def get_text(file_name: str) -> list:
    """指定したテキストファイルを改行で区切ってリストに変換して返します。

    Args:
        file_name (str): 対象の拡張子を除いたファイル名

    Returns:
        list: 改行で区切った文字列のリスト
    """
    text_directory = './texts'
    path = text_directory + '/' + file_name + '.txt'
    _list = []
    try:
        with open(path, 'r') as txt:
            word_list = txt.read().split("\n")
            normalized_list = list(set(filter(None, word_list)))
            comment_list = [s for s in normalized_list if s.startswith('#')]
            _list = list(set(normalized_list) - set(comment_list))
    except OSError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        return _list


def update_user_flag(user_dict: dict, dict_key: str, flag_bit: int, _bool: bool) -> Tuple[dict, int]:
    """フラグを更新します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        dict_key (str): shelveのdict_key
        flag_bit (int): ビットフラグ
        _bool (bool): 真偽値

    Returns:
        user_dict (dict): 更新済みuser_dict
        int: ビットフラグ
    """
    flag = int(slv.get_dict_value(user_dict, 'flags', dict_key))
    if _bool:
        flag |= flag_bit
    else:
        flag -= flag & flag_bit
    user_dict = slv.update_slv_dict(user_dict, 'flags', {dict_key: flag})
    return user_dict, int(flag)


def get_user_flag(user_dict: dict, dict_key: str) -> int:
    """フラグ情報を取得します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        dict_key (str): shelveのdict_key

    Returns:
        int: ビットフラグ
    """
    flag = slv.get_dict_value(user_dict, 'flags', dict_key)
    return int(flag)
