import os
from dotenv import load_dotenv
import dotenv

from modules import utils
"""
discord_settings.py ディスコードの設定に関わるメソッドをまとめたモジュールです。
"""

# .envをロード
dotenv_path = dotenv.find_dotenv()
load_dotenv(dotenv_path, verbose=True)

# .envからの読み込み項目設定
try:
    ACCESS_TOKEN = os.environ.get('DISCORD_ACCESS_TOKEN')
except Exception as e:
    utils.print_error(e)
    print('ACCESS_TOKENの取得に失敗')

try:
    CHANNEL_IDS = os.environ.get('DISCORD_CHANNEL_IDS').split(',')
except Exception as e:
    utils.print_error(e)
    print('CHANNEL_IDSの取得に失敗')

# 接続時のコンソール用メッセージ
READY_MESSAGE = '接続し、準備ができました'
