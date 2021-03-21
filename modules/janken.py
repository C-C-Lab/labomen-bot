"""
じゃんけん機能に関連するメソッドをまとめたモジュールです。
"""
import random

from modules import slv
from modules import utils
from settings import janken_words


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


async def start(user_id, message):
    """jankenを開始します。

    Args:
        user_id (str or int): discordのユーザーid
        message (message): discord.pyのmessageモデル
    """
    now = utils.get_now()
    user_slv = slv.get_user_slv_path(user_id)
    START_MES = janken_words.START_MES
    # モード切替
    new_dict = {'data': {
        'mode': 'janken',
        'last_act_at': now
    }
    }
    slv.merge_dict(new_dict, user_slv)
    # メッセージ送信
    content = random.choice(START_MES)
    emoji_hands = EMOJI_HANDS.values()
    reply_message = await utils.send_reply(message, content)
    await utils.add_reaction_list(reply_message, emoji_hands)
    slv.update_value(user_slv, 'janken',
                     'last_message_id', reply_message.id)


async def play(user=None, message=None, reaction=None):
    """じゃんけんを実行します。

    Args:
        user_id (str or int): discordのuser_id
        message (message): discord.pyのmessageモデル
        reaction (reaction): discord.pyのreactionモデル
    """
    print('じゃんけんを実行')
    # 手に応じた整数をdictから取得
    bot_hand, bot_hand_num = random.choice(list(BOT_HANDS.items()))
    if message:
        await play_with_mes(message, bot_hand_num)
    else:
        await play_with_emoji(user, reaction, bot_hand_num)


async def play_with_emoji(user, reaction, bot_hand_num):
    """emojiによるじゃんけんを実行します。

    Args:
        user (user): discord.pyのuserモデル
        reaction (reaction): discord.pyのreactionモデル
        bot_hand_num (int): botの手を示す整数
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


async def play_with_mes(message, bot_hand_num):
    """メッセージによるじゃんけんを実行します。

    Args:
        user (user): discord.pyのuserモデル
        bot_hand_num (int): botの手を示す整数
    """
    user_id = str(message.author.id)
    hiragana_content = utils.get_hiragana(message.content)
    command_word = utils.get_command(hiragana_content, USER_HANDS)
    user_hand_num = USER_HANDS[command_word]
    result = bot_hand_num - user_hand_num
    result_mes = calculate_result(result, user_id)
    emoji_hand = EMOJI_HANDS[bot_hand_num]
    if result == 0:
        reply_message = await utils.send_reply(message, result_mes)
        await send_aiko_mes(user_id, reply_message)
    else:
        await utils.send_reply(message, emoji_hand)
        await utils.send_reply(message, result_mes)


async def send_aiko_mes(user_id, reply_message):
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


def calculate_result(result, user_id):
    """じゃんけんの結果を計算します。

    Args:
        result (int): じゃんけん結果を表す整数
        user_id (str or int): discordのuser_id

    Returns:
        str: 結果メッセージ文
    """
    if result in [-1, 2]:
        result_mes = get_result_mes(win_mes, '勝ち', user_id)
    elif result in [1, -2]:
        result_mes = get_result_mes(lose_mes, '負け', user_id)
    elif result == 0:
        result_mes = get_result_mes(favour_mes, 'あいこ', user_id)
    return result_mes


def get_result_mes(janken_mes, result, user_id):
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
