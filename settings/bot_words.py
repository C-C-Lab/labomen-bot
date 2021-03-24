"""bot_words.py botの基本的な発言やコマンドをまとめたモジュールです。
    """

from modules import utils
txt = utils.get_text

# botが反応するコマンド一覧
BOT_COMMANDS = {
    'NORMAL': 'らびちゃん',
    'JANKEN': 'じゃんけん',
    'OMIKUJI': 'おみくじ',
    'HELP': r'へるぷ|教えて|おしえて',
}

# ランダムに返すメッセージ
RANDOM_CONTENTS = txt('default')


# メンションされた際のヒントメッセージ
HINT_MESSAGE = 'もし私ができることを知りたいのなら「ヘルプ」とか「教えて」って話しかけてもらえれば教えてあげられるわ'
