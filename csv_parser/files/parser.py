import pandas as pd
from django.conf import settings
from .db_functions import get_all_files, get_file_by_id, get_filename_by_id


def read_csv(file):
    return pd.read_csv(file, encoding_errors='ignore')


def get_column_names_and_rows(file):
    df = read_csv(file)
    list_of_column_names = list(df.columns)
    rows_index = len(df.index)
    return list_of_column_names, rows_index


def get_files_info():
    all_files = get_all_files()

    data_files = []

    for obj in all_files:

        column_names, rows_index = get_column_names_and_rows(obj.file)
        data_files.append({
            "name": obj.file_name,
            "columns": column_names,
            "columns_count": len(column_names),
            "rows_count": rows_index,
            "file_id": obj.id,
        })

    return data_files


def df_to_html(df, pk):
    frame = df.to_html()
    with open('csv_parser/templates/files/frames.html', 'w') as f:
        f.write(f"<a href='/files/{pk}/download'>Скачать</a></br>" + frame)
    return


def df_to_csv(df, pk):
    file_name = get_filename_by_id(pk)
    return df.to_csv(f'{settings.MEDIA_ROOT}/downloadedfiles/{file_name}')


def filter_data(
        pk: int,
        columns_to_show: list[str],
        columns_to_sort: list[str],
        is_ascending: bool,
        is_index: bool,
        is_head: bool,
        num_of_rows: int
):

    file_object = get_file_by_id(pk)
    file_object_df = read_csv(file_object.file)
    filtered_data = sort_and_filter(file_object_df,
                                    columns_to_show,
                                    columns_to_sort,
                                    is_ascending,
                                    is_index,
                                    is_head,
                                    num_of_rows)
    return filtered_data


def sort_and_filter(
        df,
        cols_to_show=None,
        cols_to_sort=None,
        is_ascending=False,
        is_index=False,
        is_head=None,
        num_of_rows=None
):

    if cols_to_sort:
        modified_df = df.sort_values(by=cols_to_sort,
                                     ascending=is_ascending)
        filtered_df = sort_and_filter(modified_df,
                                      cols_to_show,
                                      None,
                                      is_ascending,
                                      is_index,
                                      is_head,
                                      num_of_rows)
        return filtered_df

    if cols_to_show:
        modified_df = df[cols_to_show]
        filtered_df = sort_and_filter(modified_df,
                                      is_ascending=is_ascending,
                                      is_index=is_index,
                                      is_head=is_head,
                                      num_of_rows=num_of_rows)
        return filtered_df

    if is_index:
        modified_df = df.sort_index(ascending=is_ascending)
        filtered_df = sort_and_filter(modified_df,
                                      is_head=is_head,
                                      num_of_rows=num_of_rows)
        return filtered_df

    match is_head:
        case 'True':
            return df.head(abs(num_of_rows))
        case 'False':
            return df.tail(abs(num_of_rows))
        case _:
            pass

    return df
