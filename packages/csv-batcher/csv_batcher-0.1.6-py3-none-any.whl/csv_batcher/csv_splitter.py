import tempfile
from typing import Sequence
from csv_batcher.utils.logger import logging

class CSVSplitter:
    """Splits a CSV file into multiple files"""
    def __init__(self, csv_filename:str, chunk_line_cnt:int = 10000):
        """
        Construct CSVSplitter

        Args:
            csv_filename (str): path to CSV file
            chunk_line_cnt (int, optional): Target lines for each chunk. Last chunk might
            be smaller than this.  Defaults to 10000.
        """
        self.csv_filename = csv_filename
        self.chunk_line_cnt = chunk_line_cnt  # lines
        self.chunk_dir =  tempfile.TemporaryDirectory()
        self.chunk_files = []
        self._split()

    def _split(self):
        """ Does the actual splitting into multiple files defined by `self.chunk_line_cnt`. """
        self.chunk_files = []
        with open(self.csv_filename, 'r') as f:
            count = 0
            header = f.readline()
            lines = []
            for line in f:
                count += 1
                lines.append(line)
                if count % self.chunk_line_cnt == 0:
                    self._write_chunk(header, count // self.chunk_line_cnt, lines)
                    lines = []

            # write remainder
            if len(lines) > 0:
                self._write_chunk(header, (count // self.chunk_line_cnt) + 1, lines)
        logging.info(f"Split ({self.csv_filename}) into {len(self.chunk_files)}")

    def _write_chunk(self, header:str, part:int, lines:Sequence):
        chunk_filename = f"{self.chunk_dir.name}/data_part_{str(part)}.csv"
        with open(chunk_filename, 'w') as f_out:
            f_out.write(header)
            f_out.writelines(lines)
            self.chunk_files.append(chunk_filename)

    def csv_files(self):
        """ Returns `self.chunk_files` """
        return self.chunk_files

    def cleanup(self):
        """
        Remove temporary directory for chunk files; this must be called
        and should be called in a `finally` block
        """
        self.chunk_dir.cleanup()
