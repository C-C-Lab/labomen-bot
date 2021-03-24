achievements = {
    'JANKEN_WIN_1': {'bit': 0b1 << 10, 'name': '初めての勝利',
                     'description': '誰にでも初めてはある！ここからがキミのスタートだ！', 'requirement': 'じゃんけんで1回勝利する。'},
    'JANKEN_WIN_10': {'bit': 0b1 << 11, 'name': '戦いの味',
                      'description': '戦いとは本能。この運命は、まだ始まったばかりなのだ。', 'requirement': 'じゃんけんで10回勝利する。'},
    'JANKEN_WIN_50': {'bit': 0b1 << 12, 'name': '大きな手',
                      'description': '成長はその姿形にさえ影響を及ぼすものだ。', 'requirement': 'じゃんけんで50回勝利する。'},
    'JANKEN_WIN_100': {'bit': 0b1 << 13, 'name': '選ばれし存在',
                       'description': 'そろそろじゃんけんのプロを名乗っても良い。', 'requirement': 'じゃんけんで100回勝利する。'},
    'JANKEN_WIN_200': {'bit': 0b1 << 14, 'name': '英傑の手',
                       'description': 'あいつが持つのは伝説の拳。じゃん拳だ！', 'requirement': 'じゃんけんで200回勝利する。'},
    'JANKEN_WIN_500': {'bit': 0b1 << 15, 'name': 'バーサーカー',
                       'description': '誰かやつを止めてくれ！', 'requirement': 'じゃんけんで500回勝利する。'},
    'JANKEN_WIN_1000': {'bit': 0b1 << 16, 'name': 'ゴッドハンド',
                        'description': '君に叶うやつはもういない。そう、運すらもね。', 'requirement': 'じゃんけんで1000回勝利する。'},
    'JANKEN_LOSE_1': {'bit': 0b1 << 17, 'name': '初めての敗北',
                      'description': '誰でも初めは初心者だ！ここから強くなればいい！', 'requirement': 'じゃんけんで1回敗北する。'},
    'JANKEN_LOSE_10': {'bit': 0b1 << 18, 'name': '床の味',
                       'description': '戦いは常に、死と隣り合わせなのだ。', 'requirement': 'じゃんけんで10回敗北する。'},
    'JANKEN_LOSE_100': {'bit': 0b1 << 19, 'name': '逆にすごい',
                        'description': 'そろそろ本気を出してもいいのでは？', 'requirement': 'じゃんけんで100回敗北する。'},
    'JANKEN_LOSE_1000': {'bit': 0b1 << 20, 'name': 'Oh My God.',
                         'description': 'じゃんけんの神よ。かの者を導き給え。', 'requirement': 'じゃんけんで1000回敗北する。'},
    'JANKEN_FAVOUR_1': {'bit': 0b1 << 17, 'name': '仲良し',
                        'description': '気の合う仲間は大切だ。', 'requirement': 'じゃんけんで1回あいこになる。'},
    'JANKEN_FAVOUR_10': {'bit': 0b1 << 18, 'name': '僕たち親友',
                         'description': '親睦を深めることが互いの成長に繋がる。', 'requirement': 'じゃんけんで10回あいこになる。'},
    'JANKEN_FAVOUR_100': {'bit': 0b1 << 19, 'name': 'もはや恋人',
                          'description': 'カップル誕生！ひゅーひゅー！', 'requirement': 'じゃんけんで100回あいこになる。'},
    'JANKEN_FAVOUR_1000': {'bit': 0b1 << 20, 'name': 'もう結婚しろ',
                           'description': '心が通じ合っているとしか思えない。', 'requirement': 'じゃんけんで1000回あいこになる。'},
    'WIN_5_STRAIGHT': {'bit': 0b1 << 21, 'name': 'ビクトリーロード',
                       'description': '運とは紛れもなく実力である。', 'requirement': 'じゃんけんで5連勝する。'},
    'WIN_10_STRAIGHT': {'bit': 0b1 << 22, 'name': '覇道',
                        'description': 'あなたは超能力者かもしれない。', 'requirement': 'じゃんけんで10連勝する。'},
    'LOSE_5_STRAIGHT': {'bit': 0b1 << 23, 'name': 'アンラッキー',
                        'description': 'とんでもなく不運。', 'requirement': 'じゃんけんで5連敗する。'},
    'LOSE_10_STRAIGHT': {'bit': 0b1 << 24, 'name': '不幸の呪い',
                         'description': 'かける言葉が見つからない。', 'requirement': 'じゃんけんで10連敗する。'},
    'FAVOUR_5_STRAIGHT': {'bit': 0b1 << 25, 'name': '以心伝心',
                          'description': 'テニスのラリーより難しいぞ。', 'requirement': 'じゃんけんで5連続あいこになる。'},
    'FAVOUR_10_STRAIGHT': {'bit': 0b1 << 26, 'name': 'ドッペルゲンガー',
                           'description': '前世はAIだったのかもしれない。', 'requirement': 'じゃんけんで10連続あいこになる。'},
    'OMIKUJI_COUNT_1': {'bit': 0b1 << 27, 'name': '初めてのおみくじ', 'description': 'おみくじって楽しいね！', 'requirement': 'おみくじを1回引く'},
    'OMIKUJI_COUNT_10': {'bit': 0b1 << 28, 'name': 'おみくじ大好き', 'description': 'おみくじってクセになるね！', 'requirement': 'おみくじを10回引く'},
    'OMIKUJI_COUNT_20': {'bit': 0b1 << 29, 'name': 'おみくじ常連', 'description': 'おみくじを引かずにはいられないね！', 'requirement': 'おみくじを20回引く'},
    'OMIKUJI_COUNT_30': {'bit': 0b1 << 30, 'name': 'おみくじの人', 'description': 'おみくじといえば私だよね！', 'requirement': 'おみくじを30回引く'},
    'OMIKUJI_COUNT_40': {'bit': 0b1 << 31, 'name': 'おみくじヒーロー', 'description': '世界をおみくじで救ってみせる！', 'requirement': 'おみくじを40回引く'},
    'OMIKUJI_COUNT_50': {'bit': 0b1 << 32, 'name': 'おみくじマイスター', 'description': '俺たちが、おみくじだ！', 'requirement': 'おみくじを50回引く'},
    'OMIKUJI_COUNT_100': {'bit': 0b1 << 33, 'name': 'おみくじマスター', 'description': '誰もの憧れのおみくじマスターだ！', 'requirement': 'おみくじを100回引く'},
    'OMIKUJI_COUNT_200': {'bit': 0b1 << 34, 'name': 'ザ・おみくじ', 'description': '君はおみくじそのものさ！', 'requirement': 'おみくじを200回引く'},
    'OMIKUJI_COUNT_300': {'bit': 0b1 << 35, 'name': 'ゴッドオブおみくじ', 'description': 'そして僕は…新世界の神になる！', 'requirement': 'おみくじを300回引く'},
    'OMIKUJI_DAIKICHI_COUNT_1': {'bit': 0b1 << 36, 'name': 'ビギナーズラック', 'description': '運、いいほうなんだね', 'requirement': 'おみくじで大吉を1回引く'},
    'OMIKUJI_DAIKICHI_COUNT_10': {'bit': 0b1 << 37, 'name': 'ラッキーパンチ', 'description': '強運の持ち主。なんでもどうにかなっちゃうね！', 'requirement': 'おみくじで大吉を10回引く'},
    'OMIKUJI_DAIKICHI_COUNT_20': {'bit': 0b1 << 38, 'name': 'プロの素質', 'description': 'タレントにも社長にもなれる豪運だ！', 'requirement': 'おみくじで大吉を20回引く'},
    'OMIKUJI_DAIKICHI_COUNT_30': {'bit': 0b1 << 39, 'name': 'ラッキーマン', 'description': 'ラッキークッキーもんじゃ焼き！', 'requirement': 'おみくじで大吉を30回引く'},
    'OMIKUJI_DAIKICHI_COUNT_40': {'bit': 0b1 << 40, 'name': '幸福の体現者', 'description': 'もはや歩いてるだけで幸運が訪れる', 'requirement': 'おみくじで大吉を40回引く'},
    'OMIKUJI_DAIKICHI_COUNT_50': {'bit': 0b1 << 41, 'name': '青い鳥', 'description': 'あなたを見た人は幸せになるレベル', 'requirement': 'おみくじで大吉を50回引く'},
    'OMIKUJI_KYO_COUNT_1': {'bit': 0b1 << 42, 'name': 'そんな日もあるさ', 'description': '仕方ない！明日からがんばろう！', 'requirement': 'おみくじで凶を1回引く'},
    'OMIKUJI_KYO_COUNT_10': {'bit': 0b1 << 43, 'name': 'ガーターボール', 'description': 'あー！なるほど！ノーコンだね！', 'requirement': 'おみくじで凶を10回引く'},
    'OMIKUJI_KYO_COUNT_20': {'bit': 0b1 << 44, 'name': '悲しき運命', 'description': '少し心配になってきたよ', 'requirement': 'おみくじで凶を20回引く'},
    'OMIKUJI_KYO_COUNT_30': {'bit': 0b1 << 45, 'name': '憂鬱の魔人', 'description': '負の力もパワーに変える！', 'requirement': 'おみくじで凶を30回引く'},
    'OMIKUJI_KYO_COUNT_40': {'bit': 0b1 << 46, 'name': 'アンデッド・アンラック', 'description': 'もはや不運すぎて不死', 'requirement': 'おみくじで凶を40回引く'},
    'OMIKUJI_KYO_COUNT_50': {'bit': 0b1 << 47, 'name': 'オーマイ・ゴッド', 'description': 'これはこれで神だよ！！', 'requirement': 'おみくじで凶を50回引く'},
}
