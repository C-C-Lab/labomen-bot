import random
import datetime
import asyncio
from typing import Any
from modules import utils
from modules import achieve
from settings import omikuji_words
from settings import init_user_states
from settings.flags import achievements

words = omikuji_words
today = str(datetime.date.today())
init_omikuji_dict = init_user_states.INITIAL_STATES['omikuji']
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
    user_dict = initialize_omikuji_dict(user_dict)
    omikuji_dict: dict = user_dict['omikuji']

    if omikuji_dict['date'] != today:
        print('=========== おみくじを実行 ============')
        # おみくじ結果の名称リストを取得（大吉～凶）
        omikuji_results = list(words.OMIKUJI_RESULTS.keys())
        # 設定したサイコロの重みをもとにおみくじ結果を算出
        results = random.choices(omikuji_results, k=1, weights=omikuji_weights)
        result = results[0]
        omikuji_dict['date'] = today
        omikuji_dict['count'] += 1
        omikuji_dict['daikichi_count'] += 1 if result == '大吉' else 0
        omikuji_dict['kyo_count'] += 1 if result == '凶' else 0
        omikuji_mes = random.choice(words.OMIKUJI_RESULTS[result])
        head_message = random.choice(words.HEADER_MES)
        await utils.send_reply(message, head_message)
        async with message.channel.typing():
            result_message = result + '！ \n' + omikuji_mes
            await asyncio.sleep(3)
            print('結果：' + result)
            print(result_message)
            omikuji_dict['result'] = result_message
            await utils.send_reply(message, result_message)
            user_dict = {**user_dict, **{'omikuji': omikuji_dict}}
    else:
        print('========= おみくじを実行不可 ==========')
        limit_mes = random.choice(words.LIMIT_MES)
        warning_mes = random.choice(words.WARNING_MES)
        repeat_intro_mes = random.choice(words.REPEAT_INTRO_MES)
        last_result = omikuji_dict.get('result', 'エラーです')
        bot_message = limit_mes + '\n' + warning_mes + \
            '\n' + repeat_intro_mes + last_result
        await utils.send_reply(message, bot_message)
        print(bot_message)
        omikuji_dict['attention_count'] += 1
        user_dict = {**user_dict, **{'omikuji': omikuji_dict}}
    user_dict = await check_achievement(message, user_dict)
    return user_dict


async def check_achievement(message: Any, user_dict: dict) -> dict:
    flags_dict = user_dict.get('flags', {})
    flag = flags_dict.get('achieve', 0)
    omikuji_dict = user_dict.get('omikuji')
    # おみくじ回数称号 --------------------------------------------------------------------------
    if omikuji_dict['count'] >= 1:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_COUNT_1'])
    if omikuji_dict['count'] >= 10:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_COUNT_10'])
    if omikuji_dict['count'] >= 20:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_COUNT_20'])
    if omikuji_dict['count'] >= 30:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_COUNT_30'])
    if omikuji_dict['count'] >= 40:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_COUNT_40'])
    if omikuji_dict['count'] >= 50:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_COUNT_50'])
    if omikuji_dict['count'] >= 100:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_COUNT_100'])
    if omikuji_dict['count'] >= 200:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_COUNT_200'])
    if omikuji_dict['count'] >= 300:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_COUNT_300'])
    # 注意回数称号 -----------------------------------------------------------------------------
    if omikuji_dict['attention_count'] >= 1:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_ATTENTION_COUNT_1'])
    if omikuji_dict['attention_count'] >= 10:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_ATTENTION_COUNT_10'])
    if omikuji_dict['attention_count'] >= 20:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_ATTENTION_COUNT_20'])
    if omikuji_dict['attention_count'] >= 30:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_ATTENTION_COUNT_30'])
    if omikuji_dict['attention_count'] >= 40:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_ATTENTION_COUNT_40'])
    if omikuji_dict['attention_count'] >= 50:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_ATTENTION_COUNT_50'])
    if omikuji_dict['attention_count'] >= 100:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_ATTENTION_COUNT_100'])
    # 大吉回数称号 -----------------------------------------------------------------------------
    if omikuji_dict['daikichi_count'] >= 1:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_DAIKICHI_COUNT_1'])
    if omikuji_dict['daikichi_count'] >= 10:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_DAIKICHI_COUNT_10'])
    if omikuji_dict['daikichi_count'] >= 20:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_DAIKICHI_COUNT_20'])
    if omikuji_dict['daikichi_count'] >= 30:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_DAIKICHI_COUNT_30'])
    if omikuji_dict['daikichi_count'] >= 40:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_DAIKICHI_COUNT_40'])
    if omikuji_dict['daikichi_count'] >= 50:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_DAIKICHI_COUNT_50'])
    # 凶回数称号 -------------------------------------------------------------------------------
    if omikuji_dict['kyo_count'] >= 1:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_KYO_COUNT_1'])
    if omikuji_dict['kyo_count'] >= 10:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_KYO_COUNT_10'])
    if omikuji_dict['kyo_count'] >= 20:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_KYO_COUNT_20'])
    if omikuji_dict['kyo_count'] >= 30:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_KYO_COUNT_30'])
    if omikuji_dict['kyo_count'] >= 40:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_KYO_COUNT_40'])
    if omikuji_dict['kyo_count'] >= 50:
        flag = await give_achievement(flag, message, achievements['OMIKUJI_KYO_COUNT_50'])
    # ------------------------------------------------------------------------------------------
    flags_dict = {**flags_dict, **{'achieve': flag}}
    user_dict = {**user_dict, **{'flags': flags_dict}}
    return user_dict


async def give_achievement(flag: int, message: Any, target_achievement: dict) -> int:
    if flag & target_achievement['bit']:
        pass
    else:
        flag |= await achieve.give(message.author, message, target_achievement)
    return flag


def initialize_omikuji_dict(user_dict: dict) -> dict:
    omikuji_dict = user_dict.get('omikuji', {})
    omikuji_dict = {
        'date': omikuji_dict.get('date', init_omikuji_dict['date']),
        'result': omikuji_dict.get('result', init_omikuji_dict['result']),
        'count': omikuji_dict.get('count', init_omikuji_dict['count']),
        'daikichi_count': omikuji_dict.get('daikichi_count', init_omikuji_dict['daikichi_count']),
        'kyo_count': omikuji_dict.get('kyo_count', init_omikuji_dict['kyo_count']),
        'attention_count': omikuji_dict.get('attention_count', init_omikuji_dict['attention_count'])
    }
    user_dict = {**user_dict, **{'omikuji': omikuji_dict}}
    return user_dict
