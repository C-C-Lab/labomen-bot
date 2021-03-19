import glob
import shelve

from settings import init_user_states
from modules import utils


def get_dict(file_name):
    """shelveファイル内容をdictとして取得します。

    Args:
        file_name (str): shelveファイルの名前を相対パスで指定

    Returns:
        dict: shelve内容
    """
    slv = shelve.open(file_name)
    slv_dict = dict(slv)
    slv.close()
    return slv_dict


def get_value(file_name, index_key, dict_key):
    """shelveからvalueを取得します。

    Args:
        file_name (str): shelveファイルの名前を相対パスで指定
        index_key (str): index_key
        dict_key (str or int): dict_key

    Returns:
        any: value
    """
    slv_dict = get_dict(file_name)
    _dict = slv_dict[index_key]
    return _dict[dict_key]


def merge_dict(_dict, file_name):
    """shelveファイルにdictをマージします。

    Args:
        _dict (dict): マージするdict
        file_name (str): shelveファイルの名前を相対パスで指定
    """
    slv = shelve.open(file_name)
    slv.update(_dict)
    slv.close()


def update_value(file_name, index_key, dict_key=None, value=None):
    """shelve内のデータを上書きします。

    Args:
        file_name (str): shelveファイルの名前を相対パスで指定
        index_key (str): shelveのindex_key
        dict_key (str or int): shelveのdict_key
        value (str or int): 上書き内容
    """
    slv_dict = get_dict(file_name)
    now = utils.get_now()
    _dict = slv_dict[index_key]
    _dict['updated_at'] = now
    if dict_key and value:
        _dict[dict_key] = value
    slv_dict[index_key] = _dict
    merge_dict(slv_dict, file_name)


def update_user_value(user_id, dict_key=None, value=None):
    """shelve内のデータを上書きします。

    Args:
        user_id (str): discordのuser_id
        dict_key (str or int): shelveのdict_key
        value (str or int): 上書き内容
    """
    file_name = './shelves/users/' + user_id + '.slv'
    slv_dict = get_dict(file_name)
    now = utils.get_now()
    _dict = slv_dict['data']
    _dict['updated_at'] = now
    if dict_key and value:
        _dict[dict_key] = value
    slv_dict['data'] = _dict
    merge_dict(slv_dict, file_name)


def initialize_user(user):
    """usersディレクトリ内にユーザーデータがなければ初期値を記録します。

    Args:
        user (user): discord.pyのユーザーモデル
    """
    user_id = str(user.id)
    slv_list = glob.glob('./shelves/users/*.slv')
    replace_list = [s.replace('./shelves/users/', '') for s in slv_list]
    id_list = [s.replace('.slv', '') for s in replace_list]
    if user_id not in id_list:
        user_slv = './shelves/users/' + user_id + '.slv'
        slv_dict = get_dict(user_slv)
        user_name = utils.get_user_name(user)
        index_key = 'data'
        print(user_name + 'の一致データなし')
        print(user_name + 'の項目を作成')
        slv_dict[index_key] = init_user_states.initial_user_state
        now = utils.get_now()
        slv_dict[index_key]['created_at'] = now
        slv_dict[index_key]['last_act_at'] = now
        merge_dict(slv_dict, user_slv)
