# csv-batcher
<p>
  <img src="https://raw.githubusercontent.com/tangledpath/csv-batcher/master/csv_batcher.png" align="left" width="512" height="256"/>
</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>
<p>&nbsp</p>

## [Vertical scaling]([url](https://en.wikipedia.org/wiki/Scalability#Vertical_or_scale_up))
A lightweight, python-based, multiprocess CSV batcher suitable for
use with dataframes or other tools that deal with large CSV files (or those that require timely processing).

## Installation
pip install csv-batcher

## GitHub
https://github.com/tangledpath/csv-batcher

## Documentation
https://tangledpath.github.io/csv-batcher/csv_batcher.html

## Further excercises
* Possibly implement pooling with celery (for use in django apps, etc.), which can bring about [horizontal scaling]([url](https://en.wikipedia.org/wiki/Scalability#Horizontal_or_scale_out)).

## Usage
Arguments sent to callback function can be controlled by
creating pooler with `callback_with` and the CallbackWith enum
values:

### As dataframe row
```python
from csv_batcher.csv_pooler import CSVPooler, CallbackWith

# Callback function passed to pooler; accepts a dataframe row
#   as a pandas Series (via apply)
def process_dataframe_row(row):
    return row.iloc[0]

pooler = CSVPooler(
    "5mSalesRecords.csv",
    process_dataframe_row,
    callback_with=CallbackWith.DATAFRAME_ROW,
    pool_size=16
)
for processed_batch in pooler.process():
    print(processed_batch)
```

### As dataframe
```python
from csv_batcher.csv_pooler import CSVPooler, CallbackWith

# Used from process_datafrom's apply:
def process_dataframe_row(row):
    return row.iloc[0]

# Callback function passed to pooler; accepts a dataframe:
def process_dataframe(df):
    foo = df.apply(process_dataframe_row, axis=1)
    # Or do something more complicated....
    return len(df)

pooler = CSVPooler(
    "5mSalesRecords.csv",
    process_dataframe,
    callback_with=CallbackWith.DATAFRAME,
    pool_size=16
)
for processed_batch in pooler.process():
    print(processed_batch)
```

### As CSV filename
```python
import pandas as pd
from csv_batcher.csv_pooler import CSVPooler, CallbackWith

# Used from process_csv_filename's apply:
def process_dataframe_row(row):
    return row.iloc[0]

def process_csv_filename(csv_chunk_filename):
    # print("processing ", csv_chunk_filename)
    df = pd.read_csv(csv_chunk_filename, skipinitialspace=True, index_col=None)
    foo = df.apply(process_dataframe_row, axis=1)
    return len(df)

pooler = CSVPooler(
    "5mSalesRecords.csv",
    process_csv_filename,
    callback_with=CallbackWith.CSV_FILENAME,
    chunk_lines=10000,
    pool_size=16
)
for processed_batch in pooler.process():
    print(processed_batch)
```
## Development
### Linting
```bash
ruff check . # Find linting errors
ruff check . --fix # Auto-fix linting errors (where possible)
```

### Documentation
```
# Shows in browser
poetry run pdoc csv_batcher
# Generates to ./docs
poetry run pdoc csv_batcher -o ./docs
# OR (recommended)
bin/build.sh
```

### Testing
```bash
clear; pytest
```

### Publishing
```bash
poetry publish --build -u __token__ -p $PYPI_TOKEN`
# OR (recommended)
bin/publish.sh
```
