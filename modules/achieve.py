import random
from typing import Any, Union

import discord

from modules import utils
from settings import achieve_words

congrat = achieve_words.CONGRAT


async def give(user: Union[discord.User, None], message: Any, achieve_dict: Union[dict, None], difficulty: list) -> int:
    """アチーブメントを付与します。

    Args:
        user (user): discord.pyのuserモデル
        message (message): discord.pyのmessageモデル
        achieve_dict (dict): アチーブメントの辞書
        difficulty (list): 難易度に応じたコメントリスト
    Returns:
        int: ビットフラグ
    """
    user_name = user.display_name
    achieve_mes = get_achieve_mes(user_name, achieve_dict)
    description_mes = get_description_mes(achieve_dict)
    congrat_mes = random.choice(congrat)
    bot_comment = random.choice(difficulty)
    bot_mes = '{0}\n{1}'.format(congrat_mes, bot_comment)
    flag_bit = achieve_dict['bit']
    bot_system_mes = achieve_mes + '\n' + description_mes
    await utils.send_message(message.channel, bot_system_mes)
    await utils.send_mention(message, bot_mes, user=user)
    return flag_bit


def get_achieve_mes(user_name: str, achieve_dict: Union[dict, None]) -> str:
    """アチーブメントシステムメッセージを取得します。

    Args:
        user_name (str): discordのユーザー名
        achieve_dict (dict): アチーブメントの辞書

    Returns:
        str: アチーブメントシステムメッセージ
    """
    name = achieve_dict['name']
    achieve_mes = (
        '*```xl\n{0}さんが\'『{1}』\'を獲得しました。\n```*'.format(user_name, name))
    return achieve_mes


def get_description_mes(achieve_dict: Union[dict, None]) -> str:
    """アチーブメントの説明メッセージを取得します。

    Args:
        achieve_dict (str): アチーブメントの辞書

    Returns:
        str: アチーブメント説明メッセージ
    """
    name = achieve_dict['name']
    description = achieve_dict['description']
    requirement = achieve_dict['requirement']
    description_mes = (
        '*```xl\n\'『{0}』\'\n～～{1}～～\n獲得条件：{2}\n```*'.format(name, description, requirement))
    return description_mes
