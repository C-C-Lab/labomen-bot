"""
slv関連のメソッドをまとめたモジュールです。
"""
import glob
import shelve
from typing import Any
from typing import Union

import discord

from settings import init_user_states
from modules import utils


def get_user_slv_path(user_id: Union[str, int]) -> str:
    """userのslvパスを取得します。

    Args:
        user_id (str or int): user_id

    Returns:
        str: ファイルパス
    """
    str_id = str(user_id)
    user_slv_path = './shelves/users/' + str_id + '.slv'
    return user_slv_path


def get_dict(file_name: str) -> dict:
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


def get_value(file_name: str, index_key: str, dict_key: Union[str, int]) -> Any:
    """shelveからvalueを取得します。

    Args:
        file_name (str): shelveファイルの名前を相対パスで指定
        index_key (str): shelveのindex_key
        dict_key (str or int): shelveのdict_key

    Returns:
        any: value
    """
    slv_dict = get_dict(file_name)
    _dict = slv_dict.get(index_key, {})
    value = _dict.get(dict_key)
    return value


def merge_dict(_dict: dict, file_name: str):
    """shelveファイルにdictをマージします。

    Args:
        _dict (dict): マージするdict
        file_name (str): shelveファイルの名前を相対パスで指定
    """
    slv = shelve.open(file_name)
    slv.update(_dict)
    slv.close()


def update_value(file_name: str, index_key: str, dict_key: Union[str, int] = None, value: Any = None):
    """shelve内のデータを上書きします。

    Args:
        file_name (str): shelveファイルの名前を相対パスで指定
        index_key (str): shelveのindex_key
        dict_key (str or int): shelveのdict_key
        value (str or int): 上書き内容
    """
    slv_dict = get_dict(file_name)
    now = utils.get_now()
    _dict = slv_dict.get(index_key, {})
    _dict['updated_at'] = now
    if dict_key and value:
        _dict[dict_key] = value
    slv_dict[index_key] = _dict
    merge_dict(slv_dict, file_name)


def update_user_value(user_id: Union[str, int], dict_key: Union[str, int] = None, value: Any = None):
    """shelve内のデータを上書きします。

    Args:
        user_id (str or int): discordのuser_id
        dict_key (str or int): shelveのdict_key
        value (Any): 上書き内容
    """
    file_name = get_user_slv_path(user_id)
    slv_dict = get_dict(file_name)
    now = utils.get_now()
    _dict = slv_dict.get('data', {})
    _dict['updated_at'] = now
    if dict_key and value:
        _dict[dict_key] = value
    slv_dict['data'] = _dict
    merge_dict(slv_dict, file_name)


def initialize_user(user: discord.User):
    """usersディレクトリ内にユーザーデータがなければ初期値を記録します。

    Args:
        user (user): discord.pyのuserモデル
    """
    user_id = str(user.id)
    slv_list = glob.glob('./shelves/users/*.slv')
    replace_list = [s.replace('./shelves/users/', '') for s in slv_list]
    id_list = [s.replace('.slv', '') for s in replace_list]
    if user_id not in id_list:
        user_slv = get_user_slv_path(user_id)
        slv_dict = get_dict(user_slv)
        user_name = utils.get_user_name(user)
        print(user_name + 'の一致データなし')
        print(user_name + 'の項目を作成')
        slv_dict = init_user_states.INITIAL_STATES
        now = utils.get_now()
        slv_dict['data']['created_at'] = now
        slv_dict['data']['last_act_at'] = now
        merge_dict(slv_dict, user_slv)
