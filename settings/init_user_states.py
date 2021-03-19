"""
initial_user_state dict:
    shelveにユーザー情報を保存するための変数
    'name': ユーザー名(name_discriminator)
    'mode': 現在のモード
    'updated_at': 最終更新
"""

initial_user_state = {
    'name': '',
    'mode': 'normal',
    'last_act_at': '',
    'updated_at': '',
    'created_at': '',
    'deleted_at': ''
}
