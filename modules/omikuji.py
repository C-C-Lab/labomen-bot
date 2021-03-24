import random
import datetime
from typing import Union
from typing import Any

from modules import utils
from settings import omikuji_words
from settings import init_user_states
from datetime import date
import asyncio

words = omikuji_words
today = datetime.date.today()


# おみくじサイコロの重み設定 大吉・中吉・小吉・吉・凶
omikuji_weights = [27, 20, 20, 20, 10]


async def play_omikuji(user_dict: dict, message: Any) -> dict:
    """おみくじを実行します。
    結果に応じてメッセージを送信します。

    Args:
        user_dict (dict): user_slvから取り出したdict
        message (message): discord.pyのmessageモデル

    Returns:
        user_dict (dict): 更新済みuser_dict
    """
    omikuji_dict: dict = user_dict.get('omikuji', init_user_states.INITIAL_STATES['omikuji'])
    omikuji_count: int = omikuji_dict.get('count', 0)
    daikichi_count: int = omikuji_dict.get('daikichi_count', 0)
    kyo_count: int = omikuji_dict.get('kyo_count', 0)
    attention_count: int = omikuji_dict.get('attention_count', 0)
    last_date: Union[date, str] = omikuji_dict.get('date', '')

    if last_date != today:
        print('=========== おみくじを実行 ============')
        # おみくじ結果の名称リストを取得（大吉～凶）
        omikuji_results = list(words.OMIKUJI_RESULTS.keys())
        # 設定したサイコロの重みをもとにおみくじ結果を算出
        results = random.choices(omikuji_results, k=1, weights=omikuji_weights)
        result = results[0]
        omikuji_count += 1
        daikichi_count += 1 if result == '大吉' else 0
        kyo_count += 1 if result == '凶' else 0
        omikuji_mes = random.choice(words.OMIKUJI_RESULTS[result])
        head_message = random.choice(words.HEADER_MES)
        await utils.send_reply(message, head_message)
        async with message.channel.typing():
            result_message = result + '！ \n' + omikuji_mes
            await asyncio.sleep(3)
            print('結果：' + result)
            print(result_message)
            await utils.send_reply(message, result_message)
            omikuji_dict = {**omikuji_dict, **{'date': today, 'count': omikuji_count, 'daikichi_count': daikichi_count, 'kyo_count': kyo_count, 'result': result_message}}
            user_dict = {**user_dict, **{'omikuji': omikuji_dict}}
    else:
        print('========= おみくじを実行不可 ==========')
        attention_count += 1
        limit_mes = random.choice(words.LIMIT_MES)
        warning_mes = random.choice(words.WARNING_MES)
        repeat_intro_mes = random.choice(words.REPEAT_INTRO_MES)
        last_result = omikuji_dict.get('result', 'エラーです')
        bot_message = limit_mes + '\n' + warning_mes + \
            '\n' + repeat_intro_mes + last_result
        await utils.send_reply(message, bot_message)
        print(bot_message)
        omikuji_dict = {**omikuji_dict, **{'attention_count': attention_count}}
        user_dict = {**user_dict, **{'omikuji': omikuji_dict}}
    return user_dict
