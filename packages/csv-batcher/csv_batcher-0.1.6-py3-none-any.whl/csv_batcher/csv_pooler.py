from enum import StrEnum, auto
from multiprocessing import Pool
from typing import Callable

import pandas as pd

from csv_batcher.csv_splitter import CSVSplitter
from csv_batcher.utils.logger import logging

class CallbackWith(StrEnum):
    """
    CallbackWith Enum, used to control what is passed to callback function
    """
    # Pass the chunked CSV filename:
    CSV_FILENAME = auto()

    # Pass a Dataframe created from the chunked CSV file:
    DATAFRAME = auto()

    # First creates a DataFrame, then calls `apply()` with the callback
    #   function. This causes the callback function to be called with
    #   each row as a `pd.Series` object:
    DATAFRAME_ROW = auto()
class CSVPooler:
    def __init__(
        self,
        csv_filename: str,
        process_fn: Callable,
        callback_with: CallbackWith = CallbackWith.CSV_FILENAME,
        pool_size: int = 5,
        chunk_lines: int = 10000,
    ):
        """
        Construct `Pooler` with given `csv_filename`, `process_fn`, `as_dataframe`, `pool_size', 'chunk_size'

        Args:
            csv_filename (str): Name of CSV file
            process_fn (Callable): A function that accepts a single argument
                By default, this is the path to a chunked CSV file
                If `as_dataframe` is True, then the argument sent is a dataframe of the chunked CSV
            callback_with (CallbackWith): Controls what is sent to callback function.
                @see CallbackWith enumeration for details
                Defaults to CallbackWith.CSV_FILENAME.
            as_dataframe_rows (bool): When True, a dataframe is created as with as_dataframe.
                that is sent to `process_fn` instead.  Defaults to False.
            pool_size (int, optional): Number of workers to uses. Defaults to 8.
            chunk_lines (int, optional): Target row count for each chunked CSV. Last chunk may
                have fewer rows.  Defaults to 10000.
        """
        self.csv_filename = csv_filename
        self.process_fn = process_fn
        self.callback_with = callback_with
        self.pool_size = pool_size
        self.chunk_lines = chunk_lines

    def process(self):
        """
        Processes `self.csv_filename` by using `CSVSplitter` to split it
            into multiple temporary files defined by `self.chunk_lines`.
        Use `multiprocessing.Pool` to use multiple process workers to process
        the group of CSVs.
        """
        processed_count = 0
        csv_splitter = CSVSplitter(self.csv_filename, self.chunk_lines)
        try:
            csv_file_cnt = len(csv_splitter.csv_files())
            logging.info(f"Pooling against {csv_file_cnt} files")
            with Pool(self.pool_size) as p:
                for result, count in p.imap(self._process_csv, csv_splitter.csv_files()):
                    yield(result)
                    processed_count += count
        finally:
            csv_splitter.cleanup()

        logging.info(f"Processed {processed_count} rows from {csv_file_cnt} CSV Files")

    def _process_csv(self, csv_chunk_filename):
        if self.callback_with == CallbackWith.CSV_FILENAME:
            result = self.process_fn(csv_chunk_filename)
            with open(csv_chunk_filename) as f:
                # Get total lines and subtract for header:
                count = sum(1 for line in f) - 1
        elif self.callback_with == CallbackWith.DATAFRAME:
            df = pd.read_csv(csv_chunk_filename, skipinitialspace=True, index_col=None)
            count = df.shape[0]
            result = self.process_fn(df)
        elif self.callback_with == CallbackWith.DATAFRAME_ROW:
            df = pd.read_csv(csv_chunk_filename, skipinitialspace=True, index_col=None)
            count = df.shape[0]
            result = df.apply(self.process_fn, axis=1)

        return result, count
