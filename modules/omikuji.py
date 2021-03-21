import random
import datetime

from modules import utils
from settings import omikuji_words
from modules import slv
import asyncio


async def play_omikuji(message):
    """おみくじを実行します。
    結果に応じてメッセージを送信します。

    Args:
        message (any): discord.pyのmessageモデル
    """
    user = message.author
    user_id = str(user.id)
    user_slv = slv.get_user_slv_path(user_id)
    today = datetime.date.today()
    last_omikuji_date = slv.get_value(user_slv, 'omikuji', 'date')

    if last_omikuji_date != today:
        print('=========== おみくじを実行 ============')
        results = list(omikuji_words.OMIKUJI_RESULTS.keys())
        # サイコロの重み設定 大吉・中吉・小吉・吉・凶
        w = [20, 30, 40, 30, 10]
        omikuji_result_list = random.choices(results, k=1, weights=w)
        omikuji_result = omikuji_result_list[0]
        omikuji_mes = random.choice(
            omikuji_words.OMIKUJI_RESULTS[omikuji_result])
        head_message = random.choice(omikuji_words.HEADER_MES)
        await utils.send_reply(message, head_message)
        async with message.channel.typing():
            result_message = omikuji_result + '！！ \n' + omikuji_mes
            await asyncio.sleep(3)
            print('結果：' + omikuji_result)
            print(result_message)
            await utils.send_reply(message, result_message)
            # slvへ日付と結果を記録
            update_omikuji_slv(user, result_message)
    else:
        print('========= おみくじを実行不可 ==========')
        limit_mes = random.choice(omikuji_words.LIMIT_MES)
        repeat_mes = random.choice(omikuji_words.REPEAT_MES)
        repeat_intro_mes = random.choice(omikuji_words.REPEAT_INTRO_MES)
        last_omikuji_result = slv.get_value(user_slv, 'omikuji', 'result')
        bot_message = limit_mes + '\n' + repeat_mes + \
            '\n' + repeat_intro_mes + last_omikuji_result
        await utils.send_reply(message, bot_message)
        print(bot_message)


def update_omikuji_slv(user, result):
    """おみくじの日付をslvに保存します。

    Args:
        message (any): discord.pyのuserモデル
        result (str): 省略版の結果メッセージ
    """
    user_id = str(user.id)
    user_slv = slv.get_user_slv_path(user_id)
    today = datetime.date.today()
    slv.update_value(user_slv, 'omikuji', 'date', today)
    slv.update_value(user_slv, 'omikuji', 'result', result)
