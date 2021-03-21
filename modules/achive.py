import random

from modules import utils


async def give(user, message, achive_title, bot_mes_list):
    """アチーブメントを付与します。

    Args:
        user (user): discord.pyのuserモデル
        message (message): discord.pyのmessageモデル
        achive_title (str): アチーブメントのタイトル
        bot_mes_list (list): botの発言リスト
    """
    user_name = user.display_name
    achive_mes = get_achive_mes(user_name, achive_title)
    bot_mes = random.choice(bot_mes_list)
    await send_mes(message, user, achive_mes, bot_mes)


def get_achive_mes(user_name, achive_title):
    """アチーブメントシステムメッセージを取得します。

    Args:
        user_name (str): discordのユーザー名
        achive_title (str): アチーブメントのタイトル

    Returns:
        str: アチーブメントシステムメッセージ
    """
    achive_mes = (
        '*```xl\n {0}さんが\'{1}\'を獲得しました。\n```*'.format(user_name, achive_title))
    return achive_mes


async def send_mes(message, user, achive_mes, bot_mes):
    """アチーブメントの付与メッセージを送信します。

    Args:
        message (message): discord.pyのmessageモデル
        user (user): discord.pyのuserモデル
        achive_mes (str): アチーブメントシステムメッセージ
        bot_mes (str): botのコメント
    """
    await utils.send_message(message.channel, achive_mes)
    await utils.send_mention(message, bot_mes, user=user)
