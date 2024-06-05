import os
import time
import pandas as pd
from pandas import DataFrame
from src.chroma import ingest
from src.settings import DATA_DIR

print("[ INFO ] Loading data...")
data: DataFrame = pd.read_csv(os.path.join(DATA_DIR, "sub_chunk_kb_acl-100k.csv"))# type: ignore
data = data.drop(columns=["author"])
print("[ INFO ] Data loaded.")
num_row = 100
# [NOTE]: We are only ingesting the first 30 rows of the dataset for demonstration purposes.
print("[ INFO ] Ingesting data...")
t0 = time.time()
ingest(data=data.head(num_row), doc_col="text", id_col=None, meta_col=["title", "url"])  # type: ignore
t1 = time.time()
print("[ INFO ] Data ingested.")
ingestion_time = t1-t0
print(f"[ INFO ] Ingestion time for {num_row} rows: {ingestion_time}")