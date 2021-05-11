"""
デバッグコマンドに関するメソッドをまとめたモジュールです。
"""
import datetime
import os
import pprint
from typing import Any
from modules import utils
from settings import init_user_states
txt = utils.get_text

"""デバッグコマンドを判定するための接頭文字"""
debug_prefix = '!'

command_dict = {
    'check_channel_info': {'command': 'ch', 'description': '発言されたチャンネルの情報を表示'},
    'check_datetime': {'command': 'date', 'description': 'BOTが動いているサーバー時間を表示'},
    'check_slv': {'command': 'slv', 'description': '発言ユーザーのSLVを表示'},
    'check_text_channels': {'command': 'text_ch', 'description': 'サーバー内のテキストチャンネル情報を表示'},
    'check_version': {'command': 'version', 'description': '現在のバージョンを確認(GithubのコミットID)'},
    'check_voice_channels': {'command': 'voice_ch', 'description': 'サーバー内のボイスチャンネル情報を表示'},
    'debug_command_list': {'command': 'debug_help', 'description': 'デバッグコマンドのリストを表示'},
    'initialize_slv': {'command': 'init_slv', 'description': '発言ユーザーのSLVを初期化'},
    'reset_omikuji': {'command': 'omikuji', 'description': '発言ユーザーのおみくじ日付をリセット'},
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
    description = ''

    if message.content[0] == debug_prefix:

        command = message.content.replace(debug_prefix, '')
        print('======== デバッグコマンド検知 =========')

        # デバッグコマンド閲覧
        if command == command_dict['debug_command_list']['command']:
            content = '定義されているデバッグコマンドは以下の通りです\n```xl\n'
            for value in command_dict.values():
                add_content = '{0}{1}\n{2}\n'.format(debug_prefix, value['command'], value['description'])
                content = content + add_content
            content = content + '```'
            description = command_dict['debug_command_list']['description']
        # SLV閲覧
        elif command == command_dict['check_slv']['command']:
            p_dict = pprint.pformat(user_dict)
            content = '*```xl\n{}```*'.format(p_dict)
            description = command_dict['check_slv']['description']
        # おみくじリセット
        elif command == command_dict['reset_omikuji']['command']:
            content = 'おみくじの日付をリセットしました'
            omikuji_dict = user_dict.get('omikuji', {})
            omikuji_dict = {**omikuji_dict, **{'date': ''}}
            user_dict = {**user_dict, **{'omikuji': omikuji_dict}}
            description = command_dict['reset_omikuji']['description']
        # slvリセット
        elif command == command_dict['initialize_slv']['command']:
            content = 'ユーザー情報をリセットしました'
            user_dict = init_user_states.INITIAL_STATES
            user_dict['data']['created_at'] = now
            user_dict['data']['last_act_at'] = now
            description = command_dict['initialize_slv']['description']
        # datetimeの日付を確認
        elif command == command_dict['check_datetime']['command']:
            today = datetime.date.today()
            content = str(today)
            description = command_dict['check_datetime']['description']
        # チャンネルの情報を確認
        elif command == command_dict['check_channel_info']['command']:
            content = '*```xl\nチャンネル名：{0}\nチャンネルID：{1}```*'.format(str(message.channel.name), str(message.channel.id))
            description = command_dict['check_channel_info']['description']
        # サーバーのテキストチャンネルリストを確認
        elif command == command_dict['check_text_channels']['command']:
            content = 'このサーバーのテキストチャンネルは以下の通りです\n```xl\n'
            text_channels = message.guild.text_channels
            for text_ch in text_channels:
                add_content = '{0} [{1}]\n'.format(text_ch.name, str(text_ch.id))
                content = content + add_content
            content = content + '```'
            description = command_dict['check_text_channels']['description']
        # サーバーのボイスチャンネルリストを確認
        elif command == command_dict['check_voice_channels']['command']:
            content = 'このサーバーのボイスチャンネルは以下の通りです\n```xl\n'
            voice_channels = message.guild.voice_channels
            for voice_ch in voice_channels:
                add_content = '{0} [{1}]\n'.format(voice_ch.name, str(voice_ch.id))
                content = content + add_content
            content = content + '```'
            description = command_dict['check_voice_channels']['description']
        # バージョンを確認
        elif command == command_dict['check_version']['command']:
            if os.path.isfile('./.version'):
                version_file = open('.version', 'r', encoding='UTF-8')
                version = version_file.readline() or 'Version file is blank.'
                version_file.close
            else:
                version = 'Version file does not exist.'
            content = '現在のバージョン情報です\n```\n{}```'.format(version)
            description = command_dict['check_version']['description']
        else:
            description = '無効なデバッグコマンド'
    print('コマンド内容： {0}'.format(description))
    print('=======================================')
    return {'user_dict': user_dict, 'content': content, 'command': command}
