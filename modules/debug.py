"""
デバッグコマンドに関するメソッドをまとめたモジュールです。
"""
import datetime
import pprint
from typing import Any
from modules import utils
from settings import init_user_states

"""デバッグコマンドを判定するための接頭文字"""
prefix = '!'


def command_check(user_dict: dict, message: Any = None) -> dict:
    """デバッグコマンドを実行して結果を返します

    Args:
        user_dict (dict): user_slvから取り出したdict
        message (Any, optional): discord.pyのmessageモデル

    Returns:
        dict: デバッグの結果を辞書形式で返します
    """

    now = utils.get_now()
    command = None
    content = None

    if message.content[0] == prefix:

        command = message.content.replace(prefix, '')

        # SLV閲覧
        if command == 'slv':
            p_dict = pprint.pformat(user_dict)
            content = '*```xl\n{}```*'.format(p_dict)
        # おみくじリセット
        elif command == 'omikuji':
            content = 'おみくじの日付をリセットしました'
            omikuji_dict = user_dict.get('omikuji', {})
            omikuji_dict = {**omikuji_dict, **{'date': ''}}
            user_dict = {**user_dict, **{'omikuji': omikuji_dict}}
        # slvリセット
        elif command == 'init_slv':
            content = 'ユーザー情報をリセットしました'
            user_dict = init_user_states.INITIAL_STATES
            user_dict['data']['created_at'] = now
            user_dict['data']['last_act_at'] = now
        # datetimeの日付を確認
        elif command == 'date':
            today = datetime.date.today()
            content = str(today)
        # チャンネルの情報を確認
        elif command == 'ch':
            content = '*```xl\nチャンネル名：{0}\nチャンネルID：{1}```*'.format(str(message.channel.name), str(message.channel.id))
    return {'user_dict': user_dict, 'content': content, 'command': command}
