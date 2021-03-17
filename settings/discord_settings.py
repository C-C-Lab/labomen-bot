import os
from dotenv import load_dotenv
import dotenv
"""
discord_settings.py ディスコードの設定に関わるメソッドをまとめたモジュールです。
"""

# .envをロード
dotenv_path = dotenv.find_dotenv()
load_dotenv(dotenv_path, verbose=True)

# .envからの読み込み項目設定
ACCESS_TOKEN = os.environ.get('DISCORD_ACCESS_TOKEN')
CHANNEL_IDS = os.environ.get('DISCORD_CHANNEL_IDS').split(',')

# 接続時のコンソール用メッセージ
READY_MESSAGE = '接続し、準備ができました'
