"""
GoogleSpreadSheet の値操作関連
"""
import gspread
from gspread.models import Worksheet, Spreadsheet, Cell
from oauth2client.service_account import ServiceAccountCredentials
from typing import Union
from settings import gs_settings


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(gs_settings.GOOGLE_JSON_KEY, scope)
client = gspread.authorize(credentials)


def init_response(action: str) -> dict:
    """レスポンスの初期値を返す

    Args:
        action (str): 実行するアクションの名称

    Returns:
        dict: レスポンス初期値
    """
    return {'action:': action, 'result': 'Initial result', 'message': 'Initial message', 'data': None}


def get_book(book_identifier: str) -> dict:
    """Googleスプレッドシートを取得する

    Args:
        book_identifier (str): シートの`URL`または`キー`

    Returns:
        dict: 取得結果 `data`は`gspread`で定義されている`Spreadsheet`モデル
        e.g. {'action:': create_sheet, 'result': 'Success', 'message': 'Created a sheet: {sheet title}', 'data': Spreadsheet}
    """
    action = 'get_book'
    response = init_response(action)
    if 'http' in book_identifier:
        workbook = client.open_by_url(book_identifier)
    else:
        workbook = client.open_by_key(book_identifier)
    if workbook:
        response = {'action:': action, 'result': 'Success', 'message': 'Got the book.', 'data': workbook}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The book does not exist.', 'data': None}
    return response


def get_sheets(workbook: Spreadsheet) -> dict:
    """Googleスプレッドシート内にあるシートのリストを取得する

    Args:
        workbook (Spreadsheet): `gspread`で定義されている`Spreadsheet`モデル

    Returns:
        dict: 取得結果 `data`は`gspread`で定義されている`Worksheet`モデルのリスト
        e.g. {'action:': create_sheet, 'result': 'Success', 'message': 'Created a sheet: {sheet title}', 'data': list}
    """
    action = 'get_sheet_titles'
    response = init_response(action)
    sheets = workbook.worksheets()
    if sheets:
        response = {'action:': action, 'result': 'Success', 'message': 'Got the sheets.', 'data': sheets}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'Any sheet does not exist.', 'data': None}
    return response


def get_sheet_titles(workbook: Spreadsheet) -> dict:
    """Googleスプレッドシート内にあるシートのタイトルリストを取得する

    Args:
        workbook (Spreadsheet): `gspread`で定義されている`Spreadsheet`モデル

    Returns:
        dict: 取得結果 `data`には取得した`str`のリスト
        e.g. {'action:': create_sheet, 'result': 'Success', 'message': 'Created a sheet: {sheet title}', 'data': sheet_titles}
    """
    action = 'get_sheet_titles'
    response = init_response(action)
    sheets = get_sheets(workbook)['data']
    if sheets:
        sheet_titles = [sheet.title for sheet in sheets]
        response = {'action:': action, 'result': 'Success', 'message': 'Got sheet titles.', 'data': sheet_titles}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def create_sheet(workbook: Spreadsheet, title: str, size: list) -> dict:
    """新しいシートを作成する

    Args:
        workbook (Spreadsheet): `gspread`で定義されている`Spreadsheet`モデル
        title (str): 作成するシートのタイトル
        size (list): 作成するシートのサイズ[row, col]
        e.g. [10, 20]
    Returns:
        dict: 作成結果 `data`は`gspread`で定義されている`Worksheet`モデル
        e.g. {'action:': create_sheet, 'result': 'Success', 'message': 'Created a sheet: {sheet title}', 'data': sheet}
    """
    action = 'create_sheet'
    response = init_response(action)
    sheet_titles = get_sheet_titles(workbook)
    if title not in sheet_titles and len(size) == 2:
        workbook.add_worksheet(title=title, rows=size[0], cols=size[1])
        new_sheet = get_sheet(workbook, title)
        response = {'action:': action, 'result': 'Success', 'message': 'Created a sheet: {}'.format(title), 'data': new_sheet}
    elif title in sheet_titles:
        sheet = get_sheet(workbook, title)
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet already exists.', 'data': sheet}
    elif len(size) != 2:
        response = {'action:': action, 'result': 'Failure', 'message': 'The size specification is wrong.', 'data': None}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'Undefined error', 'data': None}
    return response


def delete_sheet(workbook: Spreadsheet, sheet: Union[Worksheet, None]) -> dict:
    """シートを削除する

    Args:
        workbook (Spreadsheet): `gspread`で定義されている`Spreadsheet`モデル
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル

    Returns:
        dict: 削除結果
        e.g. {'action:': action, 'result': 'Success', 'message': 'Deleted a sheet: {sheet title}, 'data': workbook}
    """
    action = 'delete_sheet'
    response = init_response(action)
    if sheet:
        workbook.del_worksheet(sheet)
        response = {'action:': action, 'result': 'Success', 'message': 'Deleted a sheet: {}'.format(sheet.title), 'data': workbook}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': workbook}
    return response


def get_sheet(workbook: Spreadsheet, sheet_identifier: Union[str, int]) -> dict:
    """シートをWorksheetとして取得する。

    Args:
        workbook (Spreadsheet): `gspread`で定義されている`Spreadsheet`モデル
        sheet_identifier (Union[str, int]): シート識別子 `str`の場合はシートの名前で、`int`の場合は何番目のシートかを指定して取得する
        e.g. 'シート1' or 0

    Returns:
        dict: 取得結果　`data`は`gspread`で定義されている`Worksheet`モデル
        e.g. {'action:': action, 'result': 'Success', 'message': 'Got a sheet.', 'data': Worksheet}
    """
    action = 'get_sheet'
    response = init_response(action)
    try:
        if type(sheet_identifier) == str:
            sheet = workbook.worksheet(sheet_identifier)
            response = {'action:': action, 'result': 'Success', 'message': 'Got a sheet.', 'data': sheet}
        elif type(sheet_identifier) == int:
            sheet = workbook.get_worksheet(sheet_identifier)
            response = {'action:': action, 'result': 'Success', 'message': 'Got a sheet.', 'data': sheet}
        else:
            {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    except Exception:
        {'action:': action, 'result': 'Failure', 'message': 'Unknown error.', 'data': None}
    return response


def get_records(sheet: Union[Worksheet, None], head: int = 1) -> dict:
    """シートの内容を辞書形式のリストとして取得する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        head (int): どの行番号をキーとするかを指定 初期値は`1`

    Returns:
        dict: 取得結果　dataは辞書形式のリスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Got sheet records.', 'data': list}
    """
    action = 'get_records'
    response = init_response(action)
    if sheet:
        records = sheet.get_all_records(empty2zero=False, head=head, default_blank='')
        response = {'action:': action, 'result': 'Success', 'message': 'Got sheet records.', 'data': records}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def update_sheet_title(workbook: Spreadsheet, sheet: Union[Worksheet, None], title) -> dict:
    """シートのタイトルを変更する

    Args:
        workbook (Spreadsheet): `gspread`で定義されている`Spreadsheet`モデル
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        title ([type]): 新しくつけるタイトル

    Returns:
        dict: 更新結果
        e.g. {'action:': action, 'result': 'Success', 'message': 'Updated sheet title {old_title} to {new_title}', 'data': Worksheet}
    """
    action = 'update_sheet_title'
    response = init_response(action)
    sheet_titles = get_sheet_titles(workbook)
    if title not in sheet_titles:
        if sheet:
            old_title = sheet.title
            if old_title != title:
                sheet.update_title(title)
                new_title = sheet.title
                response = {'action:': action, 'result': 'Success', 'message': 'Updated sheet title {} to {}'.format(old_title, new_title), 'data': sheet}
            else:
                response = {'action:': action, 'result': 'Failure', 'message': 'Same title as before.', 'data': sheet}
        else:
            response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet already exists.', 'data': sheet}
    return response


def get_cell(sheet: Union[Worksheet, None], coordinate: Union[list, str]) -> dict:
    """スプレッドシートの単一のセルを取得する

    Args:
        sheet (Worksheet, optional): `gspread`で定義されている`Worksheet`モデル
        coordinate (Union[list, str]): 取得対象セルの座標指定 ラベルでも座標[row, col]でも指定可能
        e.g. `'A1'` or `[1,1]`

    Returns:
        Union[str, None]: `gspread`で定義されている`Cell`モデル
    """
    action = 'get_cell'
    response = init_response(action)
    if sheet:
        if type(coordinate) == str:
            try:
                cell = sheet.acell(coordinate)
                response = {'action:': action, 'result': 'Success', 'message': 'Got a cell', 'data': cell}
            except Exception:
                response = {'action:': action, 'result': 'Failure', 'message': 'The coordinates are incorrect.', 'data': None}
        elif type(coordinate) == list and len(coordinate) == 2:
            try:
                cell = sheet.cell(coordinate[0], coordinate[1])
                response = {'action:': action, 'result': 'Success', 'message': 'Got a cell', 'data': cell}
            except Exception:
                response = {'action:': action, 'result': 'Failure', 'message': 'The coordinates are incorrect.', 'data': None}
        else:
            response = {'action:': action, 'result': 'Failure', 'message': 'Incorrect coordinate type', 'data': None}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def update_specific_cell(sheet: Union[Worksheet, None], coordinate: Union[list, str], value: Union[str, int]) -> dict:
    """セルの位置を指定してスプレッドシートのセルの内容を更新する

    Args:
        sheet (Worksheet, optional): `gspread`で定義されている`Worksheet`モデル
        coordinate (Union[list, str]): 取得対象セルの座標 ラベルでも座標でも指定可能
        e.g. 'A1' or [1,1]
        value (Union[str, int]): 新しくセルに入れる値

    Returns:
        Union[dict, None]: 更新結果 `data`には更新後の`Cell`モデル
        e.g. {'action:': action, 'result': 'Success', 'message': 'Updated value {old_value} to {new_value}', 'data': Cell}
    """
    action = 'update_specific_cell'
    response = init_response(action)
    value = str(value)
    if sheet:
        cell = get_cell(sheet, coordinate)['data']
        old_value = cell.value
        if old_value != value:
            if type(coordinate) == str:
                sheet.update_acell(coordinate, value)
                cell = get_cell(sheet, coordinate)['data']
                new_value = cell.value
                response = {'action:': action, 'result': 'Success', 'message': 'Updated value {} to {}'.format(old_value, new_value), 'data': cell}
            elif type(coordinate) == list and len(coordinate) == 2:
                sheet.update_cell(coordinate[0], coordinate[1], value)
                cell = get_cell(sheet, coordinate)['data']
                new_value = cell.value
                response = {'action:': action, 'result': 'Success', 'message': 'Updated value {} to {}'.format(old_value, new_value), 'data': cell}
            else:
                response = {'action:': action, 'result': 'Failure', 'message': 'Wrong argument.', 'data': cell}
        else:
            response = {'action:': action, 'result': 'Failure', 'message': 'Same value as before.', 'data': cell}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def update_cell(sheet: Union[Worksheet, None], cell: Union[Cell, None], value: Union[str, int]) -> dict:
    """セルを更新する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        cell (Union[Cell, None]): `gspread`で定義されている`cell`モデル
        value (Union[str, int]): 新しくセルに代入する値

    Returns:
        dict: 更新結果 `data`には更新後の`Cell`モデル
        e.g. {'action:': action, 'result': 'Success', 'message': 'Updated value {old_value} to {new_value}', 'data': Cell}
    """
    action = 'update_cell'
    response = init_response(action)
    value = str(value)
    if sheet:
        if cell:
            if cell.value != value:
                old_value = cell.value
                response = update_specific_cell(sheet, [cell.row, cell.col], value)
                new_cell = response['data']
                new_value = new_cell.value
                response = {'action:': action, 'result': 'Success', 'message': 'Updated value {} to {}'.format(old_value, new_value), 'data': new_cell}
            else:
                response = {'action:': action, 'result': 'Failure', 'message': 'Same value as before.', 'data': cell}
        else:
            response = {'action:': action, 'result': 'Failure', 'message': 'The cell does not exist.', 'data': None}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def get_range_values(sheet: Union[Worksheet, None], range: str) -> dict:
    """シートの範囲を指定して値のリストを取得する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        range (str): 範囲 e.g. 'A1:B10'

    Returns:
        dict: 取得結果 `data`キーの`values`は 値のリスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Got the cells.', 'data': cells}
    """
    action = 'get_range_values'
    response = init_response(action)
    if sheet:
        values = sheet.range(range)
        response = {'action:': action, 'result': 'Success', 'message': 'Got the values.', 'data': values}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def get_row_cells(sheet: Union[Worksheet, None], row: int, ignore: int = 0) -> dict:
    """行番号を指定してセルのリストを取得する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        row (int): 行番号
        ignore (int): 無視する行数

    Returns:
        dict: 取得結果 `data`キーの`cell`は `gspread`で定義されている`Cell`モデルのリスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Got the cells.', 'data': cells}
    """
    action = 'get_row_cells'
    response = init_response(action)
    row_count = sheet.row_count
    cells = []
    if sheet:
        for i in range(row_count - ignore):
            cell = get_cell(sheet, [row, i + 1 + ignore])['data']
            cells.append(cell)
        response = {'action:': action, 'result': 'Success', 'message': 'Got the cells.', 'data': cells}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def get_col_cells(sheet: Union[Worksheet, None], col: int, ignore: int = 0) -> dict:
    """列番号を指定してセルのリストを取得する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        col (int): 列番号
        ignore (int): 無視する列数

    Returns:
        dict: 取得結果 `data`キーの`cell`は `gspread`で定義されている`Cell`モデルのリスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Got the cells.', 'data': cells}
    """
    action = 'get_col_cells'
    response = init_response(action)
    col_count = sheet.col_count
    if sheet:
        cells = []
        for i in range(col_count - ignore):
            cell = get_cell(sheet, [i + 1 + ignore, col])['data']
            cells.append(cell)
        response = {'action:': action, 'result': 'Success', 'message': 'Got the cells.', 'data': cells}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def get_cells_values(cells: list) -> dict:
    """セルのリストからセルの値のリストを取得する

    Args:
        cells (list): `gspread`で定義されている`Cell`モデル

    Returns:
        dict: 取得結果 `data`キーのvaluesは、値のリスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Got the values.', 'data': values}
    """
    action = 'get_cells_values'
    response = init_response(action)
    values = []
    if cells:
        for cell in cells:
            if cell:
                values.append(cell.value)
            else:
                values.append(None)
        response = {'action:': action, 'result': 'Success', 'message': 'Got the values.', 'data': values}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The cells does not exist.', 'data': None}
    return response


def get_row_values(sheet: Union[Worksheet, None], row: int) -> dict:
    """行番号から値のリストを取得する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        row (int): 行番号

    Returns:
        dict: 取得結果 `data`キーのvaluesは、値のリスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Got the values.', 'data': values}
    """
    action = 'get_row_values'
    response = init_response(action)
    if sheet:
        values = sheet.row_values(row)
        response = {'action:': action, 'result': 'Success', 'message': 'Got the values.', 'data': values}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def get_col_values(sheet: Union[Worksheet, None], col: int) -> dict:
    """列番号から値のリストを取得する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        row (int): 列番号

    Returns:
        dict: 取得結果 `data`キーのvaluesは、値のリスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Got the values.', 'data': values}
    """
    action = 'get_col_values'
    response = init_response(action)
    if sheet:
        values = sheet.col_values(col)
        response = {'action:': action, 'result': 'Success', 'message': 'Got the values.', 'data': values}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def get_sheet_values(sheet: Union[Worksheet, None]) -> dict:
    """シートから全ての値の多次元リストを取得する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル

    Returns:
        dict: 取得結果 `data`キーのvaluesは、値の多次元リスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Got the values.', 'data': values}
    """
    action = 'get_sheet_values'
    response = init_response(action)
    if sheet:
        values = sheet.get_all_values()
        response = {'action:': action, 'result': 'Success', 'message': 'Got the values.', 'data': values}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def get_cells(sheet: Union[Worksheet, None], string: str) -> dict:
    """シート内から特定の値のセルを取得する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        string (str): 検索文字列

    Returns:
        dict: 検索結果 `data`キーの`cell`は `gspread`で定義されている`Cell`モデル
        e.g. {'action:': action, 'result': 'Success', 'message': 'A cell found', 'data': cell}
    """
    action = 'get_cells'
    response = init_response(action)
    if sheet:
        try:
            cell = sheet.find(string)
            response = {'action:': action, 'result': 'Success', 'message': 'Cells found.', 'data': cell}
        except Exception:
            response = {'action:': action, 'result': 'Failure', 'message': 'Data not found', 'data': None}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def get_all_cells(sheet: Union[Worksheet, None], value: Union[str, int]) -> dict:
    """シート内のセルを全てリストとして取得する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        string (str): 検索文字列

    Returns:
        dict: 検索結果 `data`キーの`cells`は `gspread`で定義されている`Cell`モデルのリスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Cells found.', 'data': cells}
    """
    action = 'get_all_cells'
    response = init_response(action)
    value = str(value)
    if sheet:
        try:
            cells = sheet.findall(value)
            response = {'action:': action, 'result': 'Success', 'message': 'Cells found.', 'data': cells}
        except Exception:
            response = {'action:': action, 'result': 'Failure', 'message': 'Data not found', 'data': None}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def update_all_cells(sheet: Union[Worksheet, None], cells_list: Union[list, None], value: Union[str, int]) -> dict:
    """リスト内のセルを全て更新する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        cells_list (Union[list, None]): `gspread`で定義されている`Cell`モデルの`list`
        value (Union[str, int]): セルに代入する値

    Returns:
        Returns:
        dict: 更新結果 `data`キーの`cells`は更新後の `gspread`で定義されている`Cell`モデルのリスト
        e.g. {'action:': action, 'result': 'Success', 'message': 'Cells found.', 'data': cells}
    """
    action = 'update_all_cells'
    response = init_response(action)
    value = str(value)
    new_cells_list = []
    if sheet:
        if cells_list:
            for cell in cells_list:
                if cell.value != value:
                    response = update_cell(sheet, cell, value)
                    new_cells_list.append(response['data'])
                else:
                    pass
            update_count = len(new_cells_list)
            if update_count > 0:
                response = {'action:': action, 'result': 'Success', 'message': '{} cells updated'.format(update_count), 'data': new_cells_list}
            else:
                response = {'action:': action, 'result': 'Failure', 'message': 'No cells updated', 'data': new_cells_list}
        else:
            response = {'action:': action, 'result': 'Failure', 'message': 'The cells does not exist.', 'data': new_cells_list}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': new_cells_list}
    return response


def create_col(sheet: Union[Worksheet, None], count: int) -> dict:
    """指定した数の列を増やす

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        count (int): 追加する列数

    Returns:
        dict: 更新結果 `data`キーの`cells`は更新後の `gspread`で定義されている`Cell`モデルのリスト
        e.g. {'action:': action, 'result': 'Success', 'message': '{count} cols added', 'data': cells}
    """
    action = 'create_col'
    response = init_response(action)
    if sheet:
        sheet.add_cols(count)
        added_cells = get_col_cells(sheet, sheet.col_count)
        response = {'action:': action, 'result': 'Success', 'message': '{} cols added.'.format(count), 'data': added_cells}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def create_row(sheet: Union[Worksheet, None], count: int) -> dict:
    """指定した数の行を増やす

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        count (int): 追加する行数

    Returns:
        dict: 更新結果 `data`キーの`cells`は更新後の `gspread`で定義されている`Cell`モデルのリスト
        e.g. {'action:': action, 'result': 'Success', 'message': '{count} rows added', 'data': cells}
    """
    action = 'create_row'
    response = init_response(action)
    if sheet:
        sheet.add_rows(count)
        added_cells = get_row_cells(sheet, sheet.row_count)
        response = {'action:': action, 'result': 'Success', 'message': '{} rows added.'.format(count), 'data': added_cells}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response


def delete_row(sheet: Union[Worksheet, None], row_number: int) -> dict:
    """指定した番号の列を削除する

    Args:
        sheet (Union[Worksheet, None]): `gspread`で定義されている`Worksheet`モデル
        count (int): 削除する行番号

    Returns:
        dict: 更新結果 `data`キーの`WorkSheet`は `gspread`で定義されている`WorkSheet`モデル
        e.g. {'action:': action, 'result': 'Success', 'message': '{count} rows added', 'data': WorkSheet}
    """
    action = 'delete_row'
    response = init_response(action)
    if sheet:
        sheet.delete_row(row_number)
        response = {'action:': action, 'result': 'Success', 'message': 'Column deleted.', 'data': sheet}
    else:
        response = {'action:': action, 'result': 'Failure', 'message': 'The sheet does not exist.', 'data': None}
    return response
