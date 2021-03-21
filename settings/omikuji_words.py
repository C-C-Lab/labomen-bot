"""おみくじ関連の定数をまとめたモジュールです。
    """

from modules import utils
txt = utils.get_text

# おみくじ開始時に送るメッセージ
HEADER_MES = txt('omikuji/start')

# おみくじを2回引こうとした時のメッセージ
LIMIT_MES = txt('omikuji/limit')

# 制限回数以上におみくじを引いた時、注意をお知らせする前置き
WARNING_MES = txt('omikuji/warning')

# 制限回数以上におみくじを引いた時、運勢を告げる直前に入るメッセージ
REPEAT_INTRO_MES = txt('omikuji/repeat_intro')

# 大吉のときのメッセージ
DAIKICHI_MES = txt('omikuji/daikichi')

# 中吉のときのメッセージ
CHUKICHI_MES = txt('omikuji/chukichi')

# 小吉のときのメッセージ
SYOKICHI_MES = txt('omikuji/syokichi')

# 吉のときのメッセージ
KICHI_MES = txt('omikuji/kichi')

# 凶のときのメッセージ
KYO_MES = txt('omikuji/kyo')


# おみくじ種別
OMIKUJI_RESULTS = {
    '大吉': DAIKICHI_MES,
    '中吉': CHUKICHI_MES,
    '小吉': SYOKICHI_MES,
    '吉': KICHI_MES,
    '凶': KYO_MES
}
