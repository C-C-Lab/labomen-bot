import shelve

from settings import init_user_states
from utils import util


init_states = init_user_states.initial_user_state


def slv_save(file_name, user, key, content):
    """shelveに情報を記録します。

    Args:
        file_name (str): shelveファイル名
        user (str): ユーザー名
        key (str): key
        content (any): 記録内容
    """
    print('---------------------------------------')
    try:
        s = shelve.open('./shelves/' + file_name + '.shelve')
        print(file_name + 'に記録')
        if user in s:
            data = s[user]
            data[key] = content
            s[user] = data
            print(user + 'の' + key + 'を変更 -> ' + str(content))
        else:
            s[user] = {key: content}
            print(user + 'の項目を作成')
            print(key + ' -> ' + str(content))
        s.close()
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
        user (str): ユーザー名
        key (str): key

    Returns:
        any: value
    """
    print('---------------------------------------')
    try:
        s = shelve.open('./shelves/' + file_name + '.shelve')
        print(file_name + 'を参照')
        data = s[user]
        s.close()
        print(user + ':' + key + ' -> ' + str(data[key]))
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
        user (str): ユーザー名
    """
    s = shelve.open('./shelves/user_data.shelve')
    if user in s:
        data = s[user]
        difference = init_states.keys() - data.keys()
        s.close()
        if difference != set():
            print('ユーザーデータに不足項目あり')
            print(difference)
            print('不足項目に初期値を入力')
            slv_save_init(user, difference)
    else:
        print('ユーザーデータなし')
        print(user + 'の項目を作成')
        s[user] = init_states
        s.close()


def slv_save_init(user, k):
    """user_data.shelveに初期値を記録します。

    Args:
        s (str): s
        user (str): user
        k (set): 記録したいkeyリスト
    """
    for key in k:
        s = shelve.open('./shelves/user_data.shelve')
        value = init_states[key]
        data = s[user]
        data[key] = value
        s[user] = data
        s.close()
