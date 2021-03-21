"""bot_words.py botの基本的な発言やコマンドをまとめたモジュールです。
    """

from modules import utils
txt = utils.get_text

# botが反応するコマンド一覧
BOT_COMMANDS = {
    'NORMAL': 'らびちゃん',
    'JANKEN': 'じゃんけん',
    'OMIKUJI': 'おみくじ'
}

# ランダムに返すメッセージ
RANDOM_CONTENTS = txt('default')
