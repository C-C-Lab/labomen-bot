import discord
import pickle

from packages import settings


# コマンド有無を確認
def command_check(word):
    command_words = settings.COMMANDS.values()
    for command in command_words:
        if command in word:
            return True
    else:
        return False


# 起動確認用バージョン情報
def version_check(mode):
    print(settings.READY_MESSAGE)
    print(discord.__title__ + " ライブラリのバージョン：" + discord.__version__)
    print(discord.__copyright__)
    print('現在のモード: ' + mode)


# メッセージ受信情報
def message_info(message, dt_now):
    print('時刻：' + str(dt_now))
    print('チャンネル名：' + str(message.channel))
    print('チャンネルID: ' + str(message.channel.id))
    print('ユーザー名:' + get_user_name(message.author))
    print('メッセージ受信：' + message.content)


# 送信者名取得
def get_user_name(user, ):
    return user.name + '#' + user.discriminator


# pickleへdumpするdef pkl_dump(file, content):
def pkl_dump(file, content):
    with open('./pickles/' + file + '.pkl', 'wb') as pkl:
        pickle.dump(content, pkl)


# pickleからloadする
def pkl_load(file):
    with open('./pickles/' + file + '.pkl', 'rb') as pkl:
        return pickle.load(pkl)
