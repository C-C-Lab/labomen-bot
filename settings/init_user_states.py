"""
initial_user_state dict:
    shelveにユーザー情報を保存するための変数
    'name': ユーザー名(name_discriminator)
    'mode': 現在のモード
    'last_act_at': 最終コマンド実行
    'updated_at': 最終更新日時
    'created_at': 作成日時
    'deleted_at': 削除日時
"""

initial_user_state = {
    'name': '',
    'mode': 'normal',
    'last_act_at': '',
    'updated_at': '',
    'created_at': '',
    'deleted_at': ''
}
