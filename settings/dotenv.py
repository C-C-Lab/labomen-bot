"""
.envの設定に関わるメソッドをまとめたモジュールです。
"""

from dotenv import load_dotenv
from modules import utils
import dotenv
import os


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

try:
    GUILDS_IDS_TO_GET_URL = os.environ.get('GUILDS_IDS_TO_GET_URL').split(',')
except Exception as e:
    utils.print_error(e)
    print('GUILDS_IDS_TO_GET_URLの取得に失敗')
