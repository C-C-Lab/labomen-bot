import random

from modules import slv
from modules import utils
from settings import janken_words
"""
janken.py じゃんけん機能に関連するメソッドをまとめたモジュールです。
"""

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

win_mes = janken_words.JANKEN_WIN_MES
lose_mes = janken_words.JANKEN_LOSE_MES
favour_mes = janken_words.JANKEN_FAVOUR_MES


async def janken_battle(message):
    """じゃんけんを実行します。
    結果に応じてメッセージを送信します。

    Args:
        message (any): Message Model of discord.py
    """
    print('じゃんけんを実行')
    # 手に応じた整数をdictから取得
    bot_hand, bot_hand_num = random.choice(list(BOT_HANDS.items()))
    user_hand_num = USER_HANDS[message.content]
    # 取得した整数を比較
    # -1, 2なら勝利
    # 1, -2なら敗北
    result = bot_hand_num - user_hand_num
    if result in [-1, 2]:
        result_mes = gen_result_mes(win_mes, '勝ち', bot_hand, message)
    elif result in [1, -2]:
        result_mes = gen_result_mes(lose_mes, '負け', bot_hand, message)
    elif result == 0:
        result_mes = gen_result_mes(
            favour_mes, 'あいこ', bot_hand, message)
    # 結果メッセージを送信
    await utils.send_reply(message, result_mes)


def gen_result_mes(janken_mes, r, bot_hand, message):
    """じゃんけんの結果に応じたメッセージを生成します。

    Args:
        janken_mes (list): 結果に応じたlist
        r (str): 勝敗
        bot_hand (str): bot_hand
        message (any): message

    Returns:
        str: じゃんけん結果メッセージ
    """
    bot_mes = random.choice(janken_mes)
    result_mes = bot_hand + bot_mes
    user_id = str(message.author.id)
    # 勝利, 敗北処理
    if janken_mes != favour_mes:
        print('結果：botの' + r)
        slv.update_user_value(user_id, 'mode', 'normal')
    # あいこ処理
    else:
        print('結果：' + r)
        now = utils.get_now()
        slv.update_user_value(user_id, 'last_act_at', now)

    return result_mes
