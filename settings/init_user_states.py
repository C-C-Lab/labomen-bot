"""
INITIAL_USER_STATES dict:
    shelveにユーザー情報を保存するための変数
    'name': ユーザー名(name_discriminator)
    'mode': 現在のモード
    'last_act_at': 最終コマンド実行日時
    'updated_at': 最終更新日時
    'created_at': 作成日時
    'deleted_at': 削除日時
"""
INITIAL_STATES = {
    'data': {
        'name': '',
        'mode': 'normal',
        'last_act_at': '',
        'updated_at': '',
        'created_at': '',
        'deleted_at': ''
    },
    'omikuji': {
        'date': '',
        'result': ''
    },
    'janken': {
        'last_message_id': '',
        'start_mes_id': ''
    },
    'flags': {
        'achieve': 0
    }
}
