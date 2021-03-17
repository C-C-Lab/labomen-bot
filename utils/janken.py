import random

from utils import util
from settings import janken_words
"""
janken.py じゃんけん機能に関連するメソッドをまとめたモジュールです。
"""


bot_hands = janken_words.BOT_HANDS
user_hands = janken_words.USER_HANDS
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
    bot_hand, bot_hand_num = random.choice(list(bot_hands.items()))
    user_hand_num = user_hands[message.content]
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
    await message.channel.send(message.author.mention + '\n' + result_mes)


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
    if janken_mes != favour_mes:
        print('結果：botの' + r)
        util.slv_save('user_data', util.get_user_name(
            message.author), 'mode', 'normal')
    else:
        print('結果：' + r)
        util.slv_save('user_data', util.get_user_name(message.author),
                      'timeout', str(util.get_time()))
    return result_mes
