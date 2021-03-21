"""じゃんけん関連の定数をまとめたモジュールです。
    """

from modules import utils
txt = utils.get_text

# じゃんけん開始時のメッセージ
START_MES = txt('janken/start')

# bot勝利メッセージ
WIN_MES = txt('janken/win')

# bot敗北メッセージ
LOSE_MES = txt('janken/lose')

# あいこメッセージ
FAVOUR_MES = txt('janken/aiko')

# じゃんけん中に他のキーワードを言った場合の反応
IGNORE_MES = txt('janken/ignore')
