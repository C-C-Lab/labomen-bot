import random


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
    """じゃんけんを行うメソッドです。
    結果に応じてメッセージを送信します。

    Args:
        message (any): Message Model of discord.py
    """
    # 手に応じた整数をdictから取得
    bot_hand, bot_hand_num = random.choice(list(BOT_HANDS.items()))
    user_hand_num = USER_HANDS[message.content]
    # 取得した整数を比較
    # -1, 2なら勝利
    # 1, -2なら敗北
    result = bot_hand_num - user_hand_num
    # bot勝利ルート
    if result in [-1, 2]:
        bot_mes = random.choice(JANKEN_WIN_MES)
        result_mes = bot_hand + bot_mes
        print('結果：botの勝ち　NORMALへ遷移')
    # bot敗北ルート
    elif result in [1, -2]:
        bot_mes = random.choice(JANKEN_LOSE_MES)
        result_mes = bot_hand + bot_mes
        print('結果：botの負け　NORMALへ遷移')
    # あいこルート
    elif result == 0:
        bot_mes = random.choice(JANKEN_FAVOUR_MES)
        result_mes = bot_hand + bot_mes
        print('結果：あいこ　JANKEN継続')
    # 結果メッセージを送信
    await message.channel.send(result_mes)
