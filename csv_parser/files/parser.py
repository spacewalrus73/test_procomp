import pandas as pd
from csv_parser.files.models import Files


def save(file) -> None:
    """
    Save file to db
    """
    Files.objects.create(
        file_name=file.name,
        file=file
    )


def read_csv(file):
    return pd.read_csv(file, encoding_errors='ignore')


def get_column_names_and_rows(file):
    df = read_csv(file)
    list_of_column_names = list(df.columns)
    rows_index = len(df.index)
    return list_of_column_names, rows_index


def get_files_info():
    all_files = Files.objects.all()

    data_files = []

    for obj in all_files:

        column_names, rows_index = get_column_names_and_rows(obj.file)
        data_files.append({
            "name": obj.file_name,
            "columns": column_names,
            "columns_count": len(column_names),
            "rows_count": rows_index,
        })

    return data_files


def df_to_html(pk: int = None, df=None):
    if pk:
        file_object = Files.objects.get(id=pk)
        file_object_df = read_csv(file_object.file)
        return file_object_df.to_html()
    else:
        return df.to_html()


def filter_data(pk: int, columns_list: list[str]):
    file_object = Files.objects.get(id=pk)
    file_object_df = read_csv(file_object.file)
    filtered_columns_df = file_object_df[columns_list]
    return filtered_columns_df

