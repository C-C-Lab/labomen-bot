import os
from os.path import join, dirname
from dotenv import load_dotenv
"""
discord_settings.py ディスコードの設定に関わるメソッドをまとめたモジュールです。
"""

# .envをロード
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(verbose=True, dotenv_path=dotenv_path)

# .envからの読み込み項目設定
ACCESS_TOKEN = os.environ.get('DISCORD_ACCESS_TOKEN')
CHANNEL_IDS = os.environ.get('DISCORD_CHANNEL_IDS').split(',')

# 接続時のコンソール用メッセージ
READY_MESSAGE = '接続し、準備ができました'
