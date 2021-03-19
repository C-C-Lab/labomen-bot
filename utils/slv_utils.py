import shelve

from settings import init_user_states
from utils import util


init_states = init_user_states.initial_user_state


def slv_save(file_name, user, key, content):
    """shelveに情報を記録します。

    Args:
        file_name (str): shelveファイル名
        user (user): discord.pyのユーザーモデル
        key (str): key
        content (any): 記録内容
    """
    user_id = str(user.id)
    user_name = util.get_user_name(user)
    print('---------------------------------------')
    try:
        s = shelve.open('./shelves/' + file_name + '.shelve')
        s_dict = dict(s)
        s.close()
        print(file_name + 'に記録')
        if user_id in s_dict:
            update('user_data', user_id, key, content)
            print(user_name + 'の' + key + 'を変更 -> ' + str(content))
        else:
            s[user_id] = {key: content}
            print(user_name + 'の項目を作成')
            print(key + ' -> ' + str(content))
    except OSError as e:
        print('-----OSError-----')
        util.error_print(e)
    except LookupError as e:
        print('-----LookupError-----')
        util.error_print(e)
    except Exception as e:
        print('-----Error-----')
        util.error_print(e)


def slv_load(file_name, user, key):
    """shelveから情報を取得します。

    Args:
        file_name (str): shelveファイル名
        user (user): discord.pyのユーザーモデル
        key (str): key

    Returns:
        any: value
    """
    user_id = str(user.id)
    user_name = util.get_user_name(user)
    print('---------------------------------------')
    try:
        s = shelve.open('./shelves/' + file_name + '.shelve')
        print(file_name + 'を参照')
        data = s[user_id]
        s.close()
        print(user_name + ':' + key + ' -> ' + str(data[key]))
        return data[key]
    except OSError as e:
        print('-----OSError-----')
        util.error_print(e)
    except KeyError:
        print('key情報なし')
    except Exception as e:
        print('-----Error-----')
        util.error_print(e)


def slv_init(user):
    """user_data.slvに不足している項目があれば初期値を記録します。

    Args:
        user (user): discord.pyのユーザーモデル
    """
    user_id = str(user.id)
    user_name = util.get_user_name(user)
    s = shelve.open('./shelves/user_data.shelve')
    if user_id in s:
        data = s[user_id]
        difference = init_states.keys() - data.keys()
        s.close()
        if difference != set():
            print(user_name + 'のデータに不足項目あり')
            print(difference)
            print('不足項目に初期値を入力')
            slv_save_init(user_id, difference)
    else:
        print(user_name + 'の一致データなし')
        print(user_name + 'の項目を作成')
        s[user_id] = init_states
        now = util.get_now()
        update(s, user_id, 'created_at', now)
        s.close()


def slv_save_init(user_id, k):
    """user_data.shelveに初期値を記録します。

    Args:
        s (str): s
        user_id (str): discordのユーザーID
        k (set): 記録したいkeyリスト
    """
    for key in k:
        s = shelve.open('./shelves/user_data.shelve')
        value = init_states[key]
        s.close()
        update('user_data', user_id, key, value)


def update(s_name, s_key, key, value):
    """shelve内のデータを上書きします。

    Args:
        s (DbfilenameShelf): shelveデータ
        s_key (str or int): shelveのキー
        key (str): 上書き項目のkey
        value (str or int): 上書き内容
    """
    s = shelve.open('./shelves/' + s_name + '.shelve')
    data = s[s_key]
    data[key] = value
    s[s_key] = data
    s.close()
    save_update_time(s_key)


def save_update_time(user_id):
    s = shelve.open('./shelves/user_data.shelve')
    now = util.get_now()
    update_time = s[user_id]
    update_time['updated_at'] = now
    s[user_id] = update_time
    s.close()


def initialize_mode():
    """shelve内ユーザーのmode情報を初期化します。
    """
    s = shelve.open('./shelves/user_data.shelve')
    user_dict = dict(s)
    s.close()
    for s_key in user_dict:
        current_mode = user_dict[s_key]['mode']
        if current_mode != 'normal':
            update('user_data', s_key, 'mode', 'normal')
            user_name = user_dict[s_key]['name']
            print(user_name + ': mode -> normal')
        else:
            None
