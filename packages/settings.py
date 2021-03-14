import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# .envからの読み込み項目設定
ACCESS_TOKEN = os.environ.get("DISCORD_ACCESS_TOKEN")
CHANNEL_IDS = os.environ.get("DISCORD_CHANNEL_IDS").split(',')

# ここからtransitionsの設定
# 状態の定義
STATES = ['NORMAL', 'JANKEN', 'TIMEOUT']

# 状態変化の定義
TRAMSITIONS = [
    {'trigger': 'to_NORMAL', 'source': '*', 'dest': 'NORMAL'},
    {'trigger': 'to_JANKEN', 'source': '*', 'dest': 'JANKEN'},
    {'trigger': 'to_TIMEOUT', 'source': '*', 'dest': 'TIMEOUT'},
]

# BOTのメッセージなどの設定
READY_MESSAGE = "接続し、準備ができました"

COMMANDS = {
    'NORMAL': 'にあちゃん',
    'JANKEN': 'じゃんけん'
}

RANDOM_CONTENTS = [
    "にゃーん",
    "わん！",
    "コケッコッコー",
    "お嬢",
    "みら姉"
]
