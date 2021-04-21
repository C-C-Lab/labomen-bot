"""
デバッグコマンドに関するメソッドをまとめたモジュールです。
"""
import datetime
import pprint
from typing import Any
from modules import utils
from settings import init_user_states

"""デバッグコマンドを判定するための接頭文字"""
debug_prefix = '!'

command_dict = {
    'debug_command_list': {'command': 'debug_help', 'description': 'デバッグコマンドのリストを確認します'},
    'check_slv': {'command': 'slv', 'description': '発言ユーザーのSLVを確認します'},
    'reset_omikuji': {'command': 'omikuji', 'description': '発言ユーザーのおみくじ日付をリセットします'},
    'initialize_slv': {'command': 'init_slv', 'description': '発言ユーザーのSLVを初期化します'},
    'check_datetime': {'command': 'date', 'description': 'BOTが動いているサーバー時間を確認します'},
    'check_channel_info': {'command': 'ch', 'description': '発言されたチャンネルの情報を確認します'},
    'check_text_channels': {'command': 'text_ch', 'description': 'サーバー内のテキストチャンネル情報を確認します'},
    'check_voice_channels': {'command': 'voice_ch', 'description': 'サーバー内のボイスチャンネル情報を確認します'}
}


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

    if message.content[0] == debug_prefix:

        command = message.content.replace(debug_prefix, '')

        # デバッグコマンド閲覧
        if command == command_dict['debug_command_list']['command']:
            content = '定義されているデバッグコマンドは以下の通りです\n```xl\n'
            for value in command_dict.values():
                add_content = '{0}{1}\n{2}\n'.format(debug_prefix, value['command'], value['description'])
                content = content + add_content
            content = content + '```'
        # SLV閲覧
        elif command == command_dict['check_slv']['command']:
            p_dict = pprint.pformat(user_dict)
            content = '*```xl\n{}```*'.format(p_dict)
        # おみくじリセット
        elif command == command_dict['reset_omikuji']['command']:
            content = 'おみくじの日付をリセットしました'
            omikuji_dict = user_dict.get('omikuji', {})
            omikuji_dict = {**omikuji_dict, **{'date': ''}}
            user_dict = {**user_dict, **{'omikuji': omikuji_dict}}
        # slvリセット
        elif command == command_dict['initialize_slv']['command']:
            content = 'ユーザー情報をリセットしました'
            user_dict = init_user_states.INITIAL_STATES
            user_dict['data']['created_at'] = now
            user_dict['data']['last_act_at'] = now
        # datetimeの日付を確認
        elif command == command_dict['check_datetime']['command']:
            today = datetime.date.today()
            content = str(today)
        # チャンネルの情報を確認
        elif command == command_dict['check_channel_info']['command']:
            content = '*```xl\nチャンネル名：{0}\nチャンネルID：{1}```*'.format(str(message.channel.name), str(message.channel.id))
        # サーバーのテキストチャンネルリストを確認
        elif command == command_dict['check_text_channels']['command']:
            content = 'このサーバーのテキストチャンネルは以下の通りです\n```xl\n'
            text_channels = message.guild.text_channels
            for text_ch in text_channels:
                add_content = '{0} [{1}]\n'.format(text_ch.name, str(text_ch.id))
                content = content + add_content
            content = content + '```'
        # サーバーのボイスチャンネルリストを確認
        elif command == command_dict['check_voice_channels']['command']:
            content = 'このサーバーのボイスチャンネルは以下の通りです\n```xl\n'
            voice_channels = message.guild.voice_channels
            for voice_ch in voice_channels:
                add_content = '{0} [{1}]\n'.format(voice_ch.name, str(voice_ch.id))
                content = content + add_content
            content = content + '```'

    return {'user_dict': user_dict, 'content': content, 'command': command}
