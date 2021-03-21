import random
import datetime

from modules import utils
from settings import omikuji_words
from modules import slv
import asyncio

words = omikuji_words


# おみくじサイコロの重み設定 大吉・中吉・小吉・吉・凶
omikuji_weights = [30, 25, 25, 20, 15]


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
    last_date = slv.get_value(user_slv, 'omikuji', 'date')

    if last_date != today:
        print('=========== おみくじを実行 ============')
        results = list(words.OMIKUJI_RESULTS.keys())
        result_list = random.choices(results, k=1, weights=omikuji_weights)
        result = result_list[0]
        omikuji_mes = random.choice(words.OMIKUJI_RESULTS[result])
        head_message = random.choice(words.HEADER_MES)
        await utils.send_reply(message, head_message)
        async with message.channel.typing():
            result_message = result + '！ \n' + omikuji_mes
            await asyncio.sleep(3)
            print('結果：' + result)
            print(result_message)
            await utils.send_reply(message, result_message)
            # slvへ日付と結果を記録
            update_omikuji_slv(user, result_message)
    else:
        print('========= おみくじを実行不可 ==========')
        limit_mes = random.choice(words.LIMIT_MES)
        warning_mes = random.choice(words.WARNING_MES)
        repeat_intro_mes = random.choice(words.REPEAT_INTRO_MES)
        last_result = slv.get_value(user_slv, 'omikuji', 'result')
        bot_message = limit_mes + '\n' + warning_mes + \
            '\n' + repeat_intro_mes + last_result
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
