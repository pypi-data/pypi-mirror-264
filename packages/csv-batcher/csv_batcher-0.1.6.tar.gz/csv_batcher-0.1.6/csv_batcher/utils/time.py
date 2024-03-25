from contextlib import contextmanager
from timeit import default_timer as timer
import sys

from .logger import logging

@contextmanager
def time_and_log(name: str, silent: bool = False):
  """Time and log block (using `with` statement)"""

  if not silent:
    caption = name if name else 'operation'
    logging.info(f"[{caption}] Starting...")
    sys.stdout.flush()
  started_at = timer()
  yield()
  elapsed = timer() - started_at
  if not silent:
    logging.info(f"[{caption}] Processed in {elapsed:.2f}s.")
    sys.stdout.flush()
  return elapsed
