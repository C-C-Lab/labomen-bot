"""じゃんけん関連の定数をまとめたモジュールです。
    """

from modules import utils
txt = utils.get_text

# じゃんけん開始時のメッセージ
JANKEN_START_MES = txt('janken/start')

# bot勝利メッセージ
JANKEN_WIN_MES = txt('janken/win')

# bot敗北メッセージ
JANKEN_LOSE_MES = txt('janken/lose')

# あいこメッセージ
JANKEN_FAVOUR_MES = txt('janken/aiko')

# じゃんけん中に他のキーワードを言った場合の反応
JANKEN_IGNORE_MES = txt('janken/ignore')
