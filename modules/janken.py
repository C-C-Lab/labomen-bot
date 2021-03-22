"""
じゃんけん機能に関連するメソッドをまとめたモジュールです。
"""
import random
from typing import Union

import discord

from modules import achieve
from modules import slv
from modules import utils
from settings import achieve_words
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
easy = achieve_words.EASY
normal = achieve_words.NORMAL
hard = achieve_words.HARD
very_hard = achieve_words.VERY_HARD


async def start(user_id: Union[str, int], message: discord.Message):
    """jankenを開始します。

    Args:
        user_id (str or int): discordのユーザーid
        message (message): discord.pyのmessageモデル
    """
    now = utils.get_now()
    user_slv = slv.get_user_slv_path(user_id)
    START_MES = janken_words.START_MES
    message_id = message.id
    # モード切替
    slv.update_user_value(user_id, 'mode', 'janken')
    slv.update_user_value(user_id, 'last_act_at', now)
    # メッセージ送信
    content = random.choice(START_MES)
    emoji_hands = EMOJI_HANDS.values()
    reply_message = await utils.send_reply(message, content)
    await utils.add_reaction_list(reply_message, emoji_hands)
    slv.update_value(user_slv, 'janken',
                     'last_message_id', reply_message.id)
    slv.update_value(user_slv, 'janken', 'start_mes_id', message_id)


async def play(user: discord.User = None, message: discord.User = None, reaction: discord.Reaction = None):
    """じゃんけんを実行します。

    Args:
        user (str or int): discordのuser_id
        message (message): discord.pyのmessageモデル
        reaction (reaction): discord.pyのreactionモデル
    """
    print('じゃんけんを実行')
    # 手に応じた整数をdictから取得
    bot_hand, bot_hand_num = random.choice(list(BOT_HANDS.items()))
    if message:
        result = await play_with_mes(message, bot_hand_num)
        author = message.author
        if result in [1, -2]:
            await winning_achieve(author, message)
    else:
        result = await play_with_emoji(user, reaction, bot_hand_num)
        message = reaction.message
        if result in [1, -2]:
            await winning_achieve(user, message)


async def play_with_emoji(user: discord.User, reaction: discord.Reaction, bot_hand_num: int) -> int:
    """emojiによるじゃんけんを実行します。

    Args:
        user (user): discord.pyのuserモデル
        reaction (reaction): discord.pyのreactionモデル
        bot_hand_num (int): botの手を示す整数

    Return:
        int: 勝敗を示す整数
    """
    message = reaction.message
    user_id = str(user.id)
    user_hand_num = utils.get_key_from_value(EMOJI_HANDS, reaction.emoji)
    result = bot_hand_num - user_hand_num
    result_mes = calculate_result(result, user_id)
    emoji_hand = EMOJI_HANDS[bot_hand_num]
    if result == 0:
        reply_message = await message.channel.send(user.mention + '\n' + emoji_hand + '\n' + result_mes)
        await send_aiko_mes(user_id, reply_message)
    else:
        await message.channel.send(user.mention + '\n' + emoji_hand + '\n' + result_mes)
        return result


async def play_with_mes(message: discord.Message, bot_hand_num: int) -> int:
    """メッセージによるじゃんけんを実行します。

    Args:
        message (message): discord.pyのmessageモデル
        bot_hand_num (int): botの手を示す整数

    Return:
        int: 勝敗を示す整数
    """
    user_id = str(message.author.id)
    hiragana_content = utils.get_hiragana(message.content)
    command_word = utils.get_command(hiragana_content, USER_HANDS)
    user_hand_num = USER_HANDS[command_word]
    result = bot_hand_num - user_hand_num
    result_mes = calculate_result(result, user_id)
    emoji_hand = EMOJI_HANDS[bot_hand_num]
    if result == 0:
        await utils.send_reply(message, emoji_hand)
        reply_message = await utils.send_reply(message, result_mes)
        await send_aiko_mes(user_id, reply_message)
    else:
        await utils.send_reply(message, emoji_hand)
        await utils.send_reply(message, result_mes)
    return result


async def send_aiko_mes(user_id: Union[str, int], reply_message: discord.message):
    """あいこになった際のメッセージを送信します。

    Args:
        user_id (str or int): discordのuser_id
        reply_message (reply): discord.pyのreplyモデル
    """
    emoji_hands = EMOJI_HANDS.values()
    user_slv = slv.get_user_slv_path(user_id)
    slv.update_value(user_slv, 'janken',
                     'last_message_id', reply_message.id)
    await utils.add_reaction_list(reply_message, emoji_hands)


def calculate_result(result: int, user_id: Union[str, int]) -> str:
    """じゃんけんの結果を計算します。

    Args:
        result (int): じゃんけん結果を表す整数
        user_id (str or int): discordのuser_id

    Returns:
        str: 結果メッセージ文
    """
    if result in [-1, 2]:
        result_mes = get_result_mes(win_mes, '勝ち', user_id)
        record_count(user_id, 'lose')
    elif result in [1, -2]:
        result_mes = get_result_mes(lose_mes, '負け', user_id)
        record_count(user_id, 'win')
    elif result == 0:
        result_mes = get_result_mes(favour_mes, 'あいこ', user_id)
        record_count(user_id, 'favour')
    return result_mes


def get_result_mes(janken_mes: list, result: str, user_id: Union[str, int]) -> str:
    """じゃんけんの結果に応じたメッセージを取得します。

    Args:
        janken_mes (list): 結果に応じたlist
        result (str): 勝敗
        emoji_hand (str): bot_hand
        user_id (str or int): discordのuser_id

    Returns:
        str: じゃんけん結果メッセージ
    """
    result_mes = random.choice(janken_mes)
    # 勝利, 敗北処理
    if janken_mes != favour_mes:
        print('結果：botの' + result)
        slv.update_user_value(user_id, 'mode', 'normal')
    # あいこ処理
    else:
        print('結果：' + result)
        now = utils.get_now()
        slv.update_user_value(user_id, 'last_act_at', now)
    return result_mes


def record_count(user_id: Union[str, int], result: str):
    """じゃんけんの履歴をslvに記録します。

    Args:
        user_id (str or int): discordのuser_id
        result (str): じゃんけんの勝敗
    """
    key = result + '_count'
    user_slv = slv.get_user_slv_path(user_id)
    result_count = slv.get_value(user_slv, 'janken', key)
    if not result_count:
        result_count = 1
    else:
        result_count = result_count + 1
    slv.update_value(user_slv, 'janken', key, result_count)


async def winning_achieve(user: discord.User, message: discord.Message) -> int:
    """勝利数に応じたアチーブメントメッセージを送信します

    Args:
        user (user): discord.pyのuserモデル
        message (message): discord.pyのmessageモデル

    return:
        str: 累計勝利数
    """
    user_id = user.id
    user_slv = slv.get_user_slv_path(user_id)
    win_count = str(slv.get_value(user_slv, 'janken', 'win_count'))
    achieve_title = 'JANKEN_WIN_' + win_count
    achieve_dict = achievements.get(achieve_title)
    if achieve:
        if win_count == '1':
            flag_bit = await achieve.give(user, message, achieve_dict, easy)
        if win_count in ['10', '50', '100']:
            flag_bit = await achieve.give(user, message, achieve_dict, normal)
        if win_count in ['200', '500']:
            flag_bit = await achieve.give(user, message, achieve_dict, hard)
        elif win_count == '1000':
            flag_bit = await achieve.give(user, message, achieve_dict, very_hard)
        else:
            return int(win_count)
        utils.update_user_flag(user_id, 'achieve', flag_bit, True)


async def losing_achieve(user: discord.User, message: discord.Message) -> int:
    """敗北数に応じたアチーブメントメッセージを送信します

    Args:
        user (user): discord.pyのuserモデル
        message (message): discord.pyのmessageモデル

    return:
        int: 累計敗北数
    """
    user_id = user.id
    user_slv = slv.get_user_slv_path(user_id)
    lose_count = str(slv.get_value(user_slv, 'janken', 'lose_count'))
    achieve_title = 'JANKEN_LOSE_' + lose_count
    achieve_dict = achievements.get(achieve_title)
    if achieve:
        if lose_count == '1':
            flag_bit = await achieve.give(user, message, achieve_dict, easy)
        if lose_count in ['10', '50', '100']:
            flag_bit = await achieve.give(user, message, achieve_dict, normal)
        if lose_count in ['200', '500']:
            flag_bit = await achieve.give(user, message, achieve_dict, hard)
        elif lose_count == '1000':
            flag_bit = await achieve.give(user, message, achieve_dict, very_hard)
        else:
            return int(lose_count)
        utils.update_user_flag(user_id, 'achieve', flag_bit, True)
