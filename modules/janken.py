"""
じゃんけん機能に関連するメソッドをまとめたモジュールです。
"""
import random
from typing import Any, Union, Tuple

import discord

from modules import achieve
from modules import slv
from modules import utils
from settings import janken_words
from settings.flags import achievements


# botの手
BOT_HANDS = {
    'ぐー！　': 1,
    'ちょき！　': 2,
    'ぱー！　': 3
}

# ユーザーの手
USER_HANDS = {
    'ぐー': 1,
    'ちょき': 2,
    'ぱー': 3
}

EMOJI_HANDS = {
    1: "\N{RAISED FIST}",
    2: "\N{VICTORY HAND}",
    3: "\N{RAISED HAND}",
}

win_mes = janken_words.WIN_MES
lose_mes = janken_words.LOSE_MES
favour_mes = janken_words.FAVOUR_MES


async def start(user_dict: dict, message: Any) -> dict:
    """jankenを開始します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        message (message): discord.pyのmessageモデル

    Returns:
        user_dict (dict): 更新済みuser_dict
    """
    now = utils.get_now()
    START_MES = janken_words.START_MES
    message_id = message.id
    # モード切替
    new_data_dict = {'mode': 'janken', 'last_act_at': now}
    user_dict = slv.update_slv_dict(user_dict, 'data', new_data_dict)
    # メッセージ送信
    content = random.choice(START_MES)
    emoji_hands = list(EMOJI_HANDS.values())
    reply_message = await utils.send_reply(message, content)
    await utils.add_reaction_list(reply_message, emoji_hands)
    new_janken_dict = {'last_message_id': reply_message.id,
                       'start_mes_id': message_id}
    user_dict = slv.update_slv_dict(user_dict, 'janken', new_janken_dict)
    return user_dict


async def play(user_dict, user: discord.User = None, message: Any = None, reaction: discord.Reaction = None) -> dict:
    """じゃんけんを実行します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        user (str or int): discordのuser_id
        message (message): discord.pyのmessageモデル
        reaction (reaction): discord.pyのreactionモデル

    Returns:
        user_dict (dict): 更新済みuser_dict
    """
    print('じゃんけんを実行')
    # 手に応じた整数をdictから取得
    bot_hand_num = random.choice(list(BOT_HANDS.values()))
    if message:
        user_dict, result = await play_with_mes(user_dict, message, bot_hand_num)
        author = message.author
        user_dict = await check_achieve(user_dict, author, message, result)
    elif reaction:
        user_dict, result = await play_with_emoji(user_dict, user, reaction, bot_hand_num)
        message = reaction.message
        user_dict = await check_achieve(user_dict, user, message, result)
    else:
        pass
    return user_dict


async def play_with_emoji(user_dict: dict, user: Union[discord.User, None], reaction: discord.Reaction, bot_hand_num: int) -> Tuple[dict, int]:
    """emojiによるじゃんけんを実行します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        user (user): discord.pyのuserモデル
        reaction (reaction): discord.pyのreactionモデル
        bot_hand_num (int): botの手を示す整数

    Return:
        user_dict (dict): 更新済みuser_dict
        int: 勝敗を示す整数
    """
    message = reaction.message
    user_id = str(user.id)
    user_hand_num = utils.get_key_from_value(EMOJI_HANDS, reaction.emoji)
    result = bot_hand_num - int(user_hand_num)
    user_dict, result_mes = calculate_result(user_dict, result, user_id)
    emoji_hand = EMOJI_HANDS[bot_hand_num]
    if result == 0:
        reply_message = await message.channel.send(user.mention + '\n' + emoji_hand + '\n' + result_mes)
        user_dict = await send_favour_mes(user_dict, reply_message)
    else:
        await message.channel.send(user.mention + '\n' + emoji_hand + '\n' + result_mes)
    return user_dict, result


async def play_with_mes(user_dict: dict, message: Any, bot_hand_num: int) -> Tuple[dict, int]:
    """メッセージによるじゃんけんを実行します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        message (message): discord.pyのmessageモデル
        bot_hand_num (int): botの手を示す整数

    Return:
        user_dict (dict): 更新済みuser_dict
        int: 勝敗を示す整数
    """
    user_id = str(message.author.id)
    hiragana_content = utils.get_hiragana(message.content)
    result = 0
    command_word = utils.get_command(hiragana_content, USER_HANDS)
    if command_word:
        user_hand_num = int(USER_HANDS[command_word])
        result = bot_hand_num - user_hand_num
        user_dict, result_mes = calculate_result(user_dict, result, user_id)
        emoji_hand = EMOJI_HANDS[bot_hand_num]
        if result == 0:
            await utils.send_reply(message, emoji_hand)
            reply_message = await utils.send_reply(message, result_mes)
            user_dict = await send_favour_mes(user_dict, reply_message)
        else:
            await utils.send_reply(message, emoji_hand)
            await utils.send_reply(message, result_mes)
    return user_dict, result


async def send_favour_mes(user_dict: dict, reply_message: Any) -> dict:
    """あいこになった際のメッセージを送信します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        reply_message (reply): discord.pyのreplyモデル

    Returns:
        user_dict (dict): 更新済みuser_dict
    """
    emoji_hands = list(EMOJI_HANDS.values())
    user_dict = slv.update_slv_dict(
        user_dict, 'janken', {'last_message_id': reply_message.id})
    await utils.add_reaction_list(reply_message, emoji_hands)
    return user_dict


def calculate_result(user_dict, result: int, user_id: Union[str, int]) -> Tuple[dict, str]:
    """じゃんけんの結果を計算します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        result (int): じゃんけん結果を表す整数
        user_id (str or int): discordのuser_id

    Returns:
        user_dict (dict): 更新済みuser_dict
        str: 結果メッセージ文
    """
    if result in [-1, 2]:
        user_dict, result_mes = get_result_mes(user_dict, win_mes, '勝ち')
        user_dict = record_count(user_dict, 'lose')
    elif result in [1, -2]:
        user_dict, result_mes = get_result_mes(user_dict, lose_mes, '負け')
        user_dict = record_count(user_dict, 'win')
    else:
        user_dict, result_mes = get_result_mes(user_dict, favour_mes, 'あいこ')
        user_dict = record_count(user_dict, 'favour')
    return user_dict, result_mes


def get_result_mes(user_dict: dict, janken_mes: list, result: str) -> Tuple[dict, str]:
    """じゃんけんの結果に応じたメッセージを取得します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        janken_mes (list): 結果に応じたlist
        result (str): 勝敗

    Returns:
        user_dict (dict): 更新済みuser_dict
        str: じゃんけん結果メッセージ
    """
    result_mes = random.choice(janken_mes)
    # 勝利, 敗北処理
    if janken_mes != favour_mes:
        print('結果：botの' + result)
        user_dict = slv.update_slv_dict(user_dict, 'data', {'mode': 'normal'})
    # あいこ処理
    else:
        print('結果：' + result)
        now = utils.get_now()
        user_dict = slv.update_slv_dict(
            user_dict, 'data', {'last_act_at': now})
    return user_dict, result_mes


def record_count(user_dict: dict, result: str) -> dict:
    """じゃんけんの履歴をslvに記録します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        result (str): じゃんけんの勝敗

    Returns:
        user_dict (dict): 更新済みuser_dict
    """
    key = result + '_count'
    result_count = slv.get_dict_value(user_dict, 'janken', key)
    if not result_count:
        result_count = 1
    else:
        result_count = result_count + 1
    slv.update_slv_dict(user_dict, 'janken', {key: result_count})
    return user_dict


async def check_achieve(user_dict: dict, user: Union[discord.User, None], message: Any, result: Union[int, None]) -> dict:
    """勝敗に応じたアチーブメント処理を実行します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        user (user): discord.pyのuserモデル
        message (message): discord.pyのmessageモデル
        result (int): じゃんけん結果を表す整数

    Returns:
        user_dict (dict): 更新済みuser_dict
    """
    streak_counts = slv.get_dict_value(
        user_dict, 'janken', 'streak_counts', {})
    if result in [1, -2]:
        winning_streak = streak_counts.get('winning_streak', 0) + 1
        streak_count_dict = {'winning_streak': winning_streak,
                             'losing_streak': 0, 'favour_streak': 0}
        user_dict = await winning_achieve(user_dict, user, message, winning_streak)
    elif result in [-1, 2]:
        losing_streak = streak_counts.get('losing_streak', 0) + 1
        streak_count_dict = {'losing_streak': losing_streak,
                             'winning_streak': 0, 'favour_streak': 0}
        user_dict = await losing_achieve(user_dict, user, message, losing_streak)
    else:
        favour_streak = streak_counts.get('favour_streak', 0) + 1
        streak_count_dict = {'favour_streak': favour_streak}
        user_dict = await favour_achieve(user_dict, user, message, favour_streak)
    streak_counts.update(streak_count_dict)
    user_dict = slv.update_slv_dict(
        user_dict, 'janken', {'streak_counts': streak_counts})
    return user_dict


async def winning_achieve(user_dict: dict, user: Union[discord.User, None], message: Any, winning_streak: int) -> dict:
    """勝利数に応じたアチーブメントメッセージを送信します

    Args:
        user_dict (dict): user_slvから取り出したdict
        user (user): discord.pyのuserモデル
        message (message): discord.pyのmessageモデル

    return:
        user_dict (dict): 更新済みuser_dict
    """
    flag_bit = 0
    win_count = str(slv.get_dict_value(user_dict, 'janken', 'win_count'))
    achieve_title = 'JANKEN_WIN_' + win_count
    achieve_dict = achievements.get(achieve_title)
    if win_count == '1':
        flag_bit = await achieve.give(user, message, achieve_dict)
    elif win_count in ['10', '50', '100']:
        flag_bit = await achieve.give(user, message, achieve_dict)
    elif win_count in ['200', '500']:
        flag_bit = await achieve.give(user, message, achieve_dict)
    elif win_count == '1000':
        flag_bit = await achieve.give(user, message, achieve_dict)
    if winning_streak == 5:
        achieve_dict = achievements.get('WIN_5_STRAIGHT')
        flag_bit |= await achieve.give(user, message, achieve_dict)
    elif winning_streak == 10:
        achieve_dict = achievements.get('WIN_10_STRAIGHT')
        flag_bit |= await achieve.give(user, message, achieve_dict)
    else:
        return user_dict
    returned_tuple = utils.update_user_flag(
        user_dict, 'achieve', flag_bit, True)
    user_dict = returned_tuple[0]
    return user_dict


async def losing_achieve(user_dict: dict, user: Union[discord.User, None], message: Any, losing_streak: dict) -> dict:
    """敗北数に応じたアチーブメントメッセージを送信します

    Args:
        user_dict (dict): user_slvから取り出したdict
        user (user): discord.pyのuserモデル
        message (message): discord.pyのmessageモデル

    return:
        user_dict (dict): 更新済みuser_dict
    """
    flag_bit = 0
    lose_count = str(slv.get_dict_value(user_dict, 'janken', 'lose_count'))
    achieve_title = 'JANKEN_LOSE_' + lose_count
    achieve_dict = achievements.get(achieve_title)
    if lose_count == '1':
        flag_bit = await achieve.give(user, message, achieve_dict)
    if lose_count in ['10', '100']:
        flag_bit = await achieve.give(user, message, achieve_dict)
    elif lose_count == '1000':
        flag_bit = await achieve.give(user, message, achieve_dict)
    if losing_streak == 5:
        achieve_dict = achievements.get('LOSE_5_STRAIGHT')
        flag_bit |= await achieve.give(user, message, achieve_dict)
    elif losing_streak == 10:
        achieve_dict = achievements.get('LOSE_10_STRAIGHT')
        flag_bit |= await achieve.give(user, message, achieve_dict)
    else:
        return user_dict
    returned_tuple = utils.update_user_flag(
        user_dict, 'achieve', flag_bit, True)
    user_dict = returned_tuple[0]
    return user_dict


async def favour_achieve(user_dict: dict, user: Union[discord.User, None], message: Any, favour_streak: dict) -> dict:
    """あいこ数に応じたアチーブメントメッセージを送信します

    Args:
        user_dict (dict): user_slvから取り出したdict
        user (user): discord.pyのuserモデル
        message (message): discord.pyのmessageモデル

    return:
        user_dict (dict): 更新済みuser_dict
    """
    flag_bit = 0
    favour_count = str(slv.get_dict_value(user_dict, 'janken', 'favour_count'))
    achieve_title = 'JANKEN_FAVOUR_' + favour_count
    achieve_dict = achievements.get(achieve_title)
    if favour_count == '1':
        flag_bit = await achieve.give(user, message, achieve_dict)
    if favour_count in ['10', '100']:
        flag_bit = await achieve.give(user, message, achieve_dict)
    elif favour_count == '1000':
        flag_bit = await achieve.give(user, message, achieve_dict)
    if favour_streak == 5:
        achieve_dict = achievements.get('FAVOUR_5_STRAIGHT')
        flag_bit |= await achieve.give(user, message, achieve_dict)
    elif favour_streak == 10:
        achieve_dict = achievements.get('FAVOUR_10_STRAIGHT')
        flag_bit |= await achieve.give(user, message, achieve_dict)
    else:
        return user_dict
    returned_tuple = utils.update_user_flag(
        user_dict, 'achieve', flag_bit, True)
    user_dict = returned_tuple[0]
    return user_dict
