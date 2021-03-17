import random

from packages import utilities
"""
janken.py じゃんけん機能に関連する関数をまとめたモジュールです。
"""

BOT_HANDS = {
    'ぐー！　': 1,
    'ちょき！　': 2,
    'ぱー！　': 3
}

USER_HANDS = {
    'ぐー': 1,
    'ちょき': 2,
    'ぱー': 3
}

JANKEN_START_MES = [
    'じゃんけんするんだね？いくよー！じゃんけん……'
]

JANKEN_WIN_MES = [
    '私の勝ち！',
    'まだまだだね！'
]

JANKEN_LOSE_MES = [
    '負けちゃった～',
    'くっそー、もう一回！'
]

JANKEN_FAVOUR_MES = [
    'やるね！　あーいこーで……',
    'さすが！　あーいこーで……'
]

# じゃんけんゲーム本体


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
        result_mes = gen_result_mes(JANKEN_WIN_MES, '勝ち', bot_hand, message)
    elif result in [1, -2]:
        result_mes = gen_result_mes(JANKEN_LOSE_MES, '負け', bot_hand, message)
    elif result == 0:
        result_mes = gen_result_mes(
            JANKEN_FAVOUR_MES, 'あいこ', bot_hand, message)
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
    if janken_mes != JANKEN_FAVOUR_MES:
        print('結果：botの' + r)
        utilities.slv_save('user_data', utilities.get_user_name(
            message.author), 'mode', 'normal')
    else:
        print('結果：' + r)
        utilities.slv_save('user_data', utilities.get_user_name(message.author),
                           'timeout', str(utilities.get_time()))
    return result_mes
