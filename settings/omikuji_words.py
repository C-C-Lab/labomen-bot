"""おみくじ関連の定数をまとめたモジュールです。
    """
# 結果の送る接頭メッセージ
HEADER_MES = [
    'おみくじするよ！あなたの運勢は…！',
    'おみくじを引くんだね！それじゃ…いくよぉ…(ガラガラ)…',
    'おみくじだね！わかった！あなたの運勢はね…',
    'おみくじだー！いくよー！結果はー…！'
]

# おみくじを2回引こうとした時のメッセージ
LIMIT_MES = [
    'だめだめ！おみくじは一日1回まで！日付が変わったらまた来なよ～♪',
    'おみくじは、1日1回なんだー！ごめんね！またあした！',
    'よくばりさんだなぁ！おみくじは1日1回までだよ！',
    'おみくじは1日1回！また明日をお楽しみに★',
    'あれれ？キミはもう今日はおみくじが終わってるみたいだよ？',
]


# 大吉のときのメッセージ
DAIKICHI_MES = [
    '実ります！恋！思い！幸せな将来はキミのもの！',
    '人や物が集まるかも！？商売繁盛！儲かりまっか！？',
    '即断即決！行動力！バランス感覚が運とお金の流れを呼び込むよ！',
    '英雄殿！！あなたなら今はなんでもできましょう！！',
    'ガチャを回すなら今だ！！全てがうまくいく！保証はしないけどね★'
]

# 中吉のときのメッセージ
CHUKICHI_MES = [
    '憂鬱な気分になっても、大丈夫！なるようになるさ！れりびー！',
    '新しい出会いがくるかも！。健康管理も大切にね！',
    '道を切り拓く力の満ちる時。周囲の意見をよく聞き、力強く前に進みましょう',
    'そこそこの運。そこそこの日。そこそこの食事。実は普通って幸せなコトなんだよ？',
    '今でも十分な運勢だけど、よかったらブロッコリーを食べよう！そしたらうまくいくさ♪',
    'ガチャを回してもいいくらいの運気だよ！'
]

# 小吉のときのメッセージ
SYOKICHI_MES = [
    '心を平和にして親類・縁者と交われば、竜詩戦争も集結するでしょう！！へぶんずわーど！！',
    '下り坂で車を押して進むように、何事もうまくいく日！',
    '今一つ納得のいかない結果のときは、一歩下がって平穏を守るときです！',
    '運がチャージされたね！ガチャを回すなら、いまだ！'
]

# 吉のときのメッセージ
KICHI_MES = [
    '変化の時きたれり！どう身を処するか、いま一度確かめましょう！',
    '明るい光！超える力！何かが芽生える！新しい事を始めよう！',
    '小さき者の面倒を見よう！全体運にバフがかかるよ！全体バフだ！',
    'それなりにいいものがでるよ！ガチャを回すなら、いまだ！'
]

# 凶のときのメッセージ
KYO_MES = [
    '勝てる時期を見極めるべし',
    '落ち着いた交際が続くことなし。思いやりの心で接するべし。',
    '悔いが残らないように！全力で行こう！いつか必ず実を結ぶときがくるよ！',
    '今日は凶だね♪なんちって！え！？ごめん！落ち込まないで！？きっといいことあるから！',
    '今キミは運を溜めている！そう！ガチャを回すなら、いまだ！'
]


# おみくじ種別
OMIKUJI_RESULTS = {
    '大吉': DAIKICHI_MES,
    '中吉': CHUKICHI_MES,
    '小吉': SYOKICHI_MES,
    '吉': KICHI_MES,
    '凶': KYO_MES
}
