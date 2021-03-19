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

win_mes = janken_words.JANKEN_WIN_MES
lose_mes = janken_words.JANKEN_LOSE_MES
favour_mes = janken_words.JANKEN_FAVOUR_MES


async def play_janken(user=None, message=None, reaction=None):
    """じゃんけんを実行します。
    結果に応じてメッセージを送信します。

    Args:
        user_id (str or int): discordのuser_id
        message (message): discord.pyのmessageモデル
        reaction (reaction): discord.pyのreactionモデル
    """
    print('じゃんけんを実行')
    # 手に応じた整数をdictから取得
    bot_hand, bot_hand_num = random.choice(list(BOT_HANDS.items()))
    emoji_hand = EMOJI_HANDS[bot_hand_num]
    if message is not None:
        user_id = str(message.author.id)
        hiragana_content = utils.get_hiragana(message.content)
        command_word = utils.get_command(hiragana_content, USER_HANDS)
        user_hand_num = USER_HANDS[command_word]
        result = bot_hand_num - user_hand_num
    elif reaction is not None:
        message = reaction.message
        user_id = str(user.id)
        user_hand_num = utils.get_key_from_value(EMOJI_HANDS, reaction.emoji)
        result = bot_hand_num - user_hand_num
    # 取得した整数を比較
    # -1, 2なら勝利
    # 1, -2なら敗北
    if result in [-1, 2]:
        result_mes = get_result_mes(win_mes, '勝ち', emoji_hand, user_id)
    elif result in [1, -2]:
        result_mes = get_result_mes(lose_mes, '負け', emoji_hand, user_id)
    elif result == 0:
        result_mes = get_result_mes(favour_mes, 'あいこ', emoji_hand, user_id)
    # 結果メッセージを送信
        if reaction is not None:
            reply_message = await message.channel.send(user.mention + '\n' + emoji_hand + '\n' + result_mes)
        elif message is not None:
            await utils.send_reply(message, emoji_hand)
            reply_message = await utils.send_reply(message, result_mes)
        emoji_hands = EMOJI_HANDS.values()
        user_slv = slv.get_user_slv_path(user_id)
        slv.update_value(user_slv, 'janken',
                         'last_message_id', reply_message.id)
        await utils.add_reaction_list(reply_message, emoji_hands)
        return
    if reaction is not None:
        await message.channel.send(user.mention + '\n' + emoji_hand + '\n' + result_mes)
    elif message is not None:
        await utils.send_reply(message, emoji_hand)
        await utils.send_reply(message, result_mes)


def get_result_mes(janken_mes, result, emoji_hand, user_id):
    """じゃんけんの結果に応じたメッセージを取得します。

    Args:
        janken_mes (list): 結果に応じたlist
        result (str): 勝敗
        emoji_hand (str): bot_hand
        user_id (str or int): discordのuser_id

    Returns:
        str: じゃんけん結果メッセージ
    """
    bot_mes = random.choice(janken_mes)
    result_mes = bot_mes
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
