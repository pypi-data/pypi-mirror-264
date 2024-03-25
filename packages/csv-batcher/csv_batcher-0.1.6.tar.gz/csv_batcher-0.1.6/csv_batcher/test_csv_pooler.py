from csv_batcher.utils.time import time_and_log
from csv_batcher.csv_pooler import CSVPooler, CallbackWith
import pandas as pd

def __process_dataframe_row(row):
    return row.iloc[0]

def __process_csv_filename(csv_chunk_filename):
    # print("processing ", csv_chunk_filename)
    df = pd.read_csv(csv_chunk_filename, skipinitialspace=True, index_col=None)
    return df.apply(__process_dataframe_row, axis=1)

def __process_as_dataframe(df):
    return df.apply(__process_dataframe_row, axis=1)

def test_big_file_as_csv():
    with time_and_log("test_big_file_as_csv"):
        pooler = CSVPooler("5mSalesRecords.csv", __process_csv_filename)
        for processed_batch in pooler.process():
            assert isinstance(processed_batch, pd.Series)

def test_big_file_as_dataframe():
    with time_and_log("test_big_file_as_dataframe"):
        pooler = CSVPooler("5mSalesRecords.csv", __process_as_dataframe, callback_with=CallbackWith.DATAFRAME)
        for processed_batch in pooler.process():
            assert isinstance(processed_batch, pd.Series)

def test_big_file_as_dataframe_rows():
    with time_and_log("test_big_file_as_dataframe_rows"):
        pooler = CSVPooler("5mSalesRecords.csv", __process_dataframe_row, callback_with=CallbackWith.DATAFRAME_ROW)
        for processed_batch in pooler.process():
            assert isinstance(processed_batch, pd.Series)

def test_no_pooler():
    with time_and_log("test_no_pooler"):
        __process_csv_filename("5mSalesRecords.csv")


if __name__ == '__main__':
    test_big_file_as_csv()
    test_big_file_as_dataframe()
    test_big_file_as_dataframe_rows()
    # test_migrator_idempotency()

