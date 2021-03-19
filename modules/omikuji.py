import random
import datetime

from modules import utils
from settings import omikuji_words
from modules import slv


async def play_omikuji(message):
    """おみくじを実行します。
    結果に応じてメッセージを送信します。

    Args:
        message (any): discord.pyのmessageモデル
    """
    user = message.author
    user_id = str(user.id)
    user_slv = utils.get_user_slv_path(user_id)
    today = datetime.date.today()
    last_omikuji_date = slv.get_value(user_slv, 'data', 'omikuji_date')

    if last_omikuji_date != today:
        print('=========== おみくじを実行 ============')
        results = list(omikuji_words.OMIKUJI_RESULTS.keys())
        # サイコロの重み設定 大吉・中吉・小吉・吉・凶
        w = [20, 30, 40, 30, 10]
        omikuji_result_list = random.choices(results, k=1, weights=w)
        omikuji_result = omikuji_result_list[0]
        omikuji_mes = random.choice(omikuji_words.OMIKUJI_RESULTS[omikuji_result])
        head_mes = random.choice(omikuji_words.HEADER_MES)
        result_mes = create_result_message(head_mes, omikuji_result, omikuji_mes)
        print('結果：' + omikuji_result)
        print(result_mes[0])
        await utils.send_reply(message, result_mes[0])
        # slvへ日付と結果を記録
        update_omikuji_slv(user, result_mes[1])
    else:
        print('========= おみくじを実行不可 ==========')
        limit_mes = random.choice(omikuji_words.LIMIT_MES)
        last_omikuji_result = slv.get_value(user_slv, 'data', 'omikuji_result')
        bot_message = limit_mes + '\n' + '一応今日の結果をもう一度お知らせしておくね！' + '\n' + 'あなたの今日の運勢は、' + last_omikuji_result
        await utils.send_reply(message, bot_message)
        print(bot_message)


def create_result_message(head_mes, omikuji_result, omikuji_mes):
    """おみくじの結果に応じたメッセージを生成します。

    Args:
        head_mes (str): 接頭メッセージ
        omikuji_result (str): おみくじ結果
        omikuji_mes (str): 本体メッセージ

    Returns:
        list : おみくじ結果メッセージ2種類 (接頭あり、接頭なし)
    """
    result_message = head_mes + ' ' + omikuji_result + '！！ \n' + omikuji_mes
    no_header = omikuji_result + '！ \n' + omikuji_mes
    return [str(result_message), str(no_header)]


def update_omikuji_slv(user, result):
    """おみくじの日付をslvに保存します。

    Args:
        message (any): discord.pyのuserモデル
        result (str): 省略版の結果メッセージ
    """
    user_id = str(user.id)
    today = datetime.date.today()
    slv.update_user_value(user_id, 'omikuji_date', today)
    slv.update_user_value(user_id, 'omikuji_result', result)
