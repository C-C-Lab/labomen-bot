"""
スプレッドシートの設定に関わるメソッドをまとめたモジュールです。
"""
import os
from dotenv import load_dotenv
import dotenv


# .envをロード
dotenv_path = dotenv.find_dotenv()
load_dotenv(dotenv_path, verbose=True)


def get_secret_dir():
    path = os.environ.get('SECRETS_DIRECTORY') or './secrets'
    os.makedirs(path, exist_ok=True)
    return path


# GOOGLE_JSON_KEY を置いとくディレクトリ
JSON_KEY_DIRECTORY = get_secret_dir()

# .envからの読み込み項目設定
GOOGLE_JSON_KEY = '{0}/{1}.json'.format(JSON_KEY_DIRECTORY, os.environ.get('GOOGLE_JSON_KEY')) or 'key.json'
