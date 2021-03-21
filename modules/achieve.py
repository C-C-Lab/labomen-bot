import random

from modules import utils


async def give(user, message, achieve_dict, bot_mes_list):
    """アチーブメントを付与します。

    Args:
        user (user): discord.pyのuserモデル
        message (message): discord.pyのmessageモデル
        achieve_dict (str): アチーブメントの辞書
        bot_mes_list (list): botの発言リスト
    """
    user_name = user.display_name
    achieve_mes, description_mes = get_achieve_mes(user_name, achieve_dict)
    bot_mes = random.choice(bot_mes_list)
    flag_bit = achieve_dict['bit']
    await utils.send_message(message.channel, achieve_mes)
    await utils.send_message(message.channel, description_mes)
    await utils.send_mention(message, bot_mes, user=user)
    return flag_bit


def get_achieve_mes(user_name, achieve_dict):
    """アチーブメントシステムメッセージを取得します。

    Args:
        user_name (str): discordのユーザー名
        achieve_dict (str): アチーブメントの辞書

    Returns:
        str: アチーブメントシステムメッセージ
    """
    name = achieve_dict['name']
    description = achieve_dict['description']
    requirement = achieve_dict['requirement']
    achieve_mes = (
        '*```xl\n{0}さんが\'『{1}』\'を獲得しました。\n```*'.format(user_name, name))
    description_mes = (
        '*```xl\n{0}\n獲得条件：{1}\n```*'.format(description, requirement))
    return achieve_mes, description_mes
