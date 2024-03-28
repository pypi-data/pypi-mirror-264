from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Optional, Any

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pyreadstat import pyreadstat as prs

if TYPE_CHECKING:
    import pyreadstat


class SavToParquet:
    def __init__(
        self,
        file: str,
        folder_out: str,
        chunksize: Optional[int] = None,
        verbose: bool = False,
    ) -> None:
        self.file = file
        self.folder_out = folder_out
        self.verbose = verbose
        self.chunksize = 5_000_000 if not chunksize else chunksize

    @property
    def path_out(self) -> str:
        return str(Path(self.file)).replace(".sav", ".parquet")

    @property
    def chunks(self) -> Iterator[tuple["pyreadstat.metadata_container", pd.DataFrame]]:
        return prs.read_file_in_chunks(
            prs.read_sav, self.file, chunksize=self.chunksize
        )

    def get_meta(self) -> Iterator:
        return prs.read_sav(self.file, row_limit=10)

    def write_meta_to_json(self) -> None:
        json_path = self.path_out.replace(".parquet", "_meta.json")

        meta_dict = {}
        for attr in dir(self.meta):
            if not attr.startswith("__"):
                meta_dict[attr] = getattr(self.meta, attr)

        with open(json_path, "w") as file:
            json.dump(meta_dict, file)

    def write_meta_to_pickle(self) -> None:
        pickle_path = self.path_out.replace(".parquet", "_meta.pickle")

        with open(pickle_path, "wb") as file:
            pickle.dump(self.meta, file)

    def write_to_parquet(self) -> None:
        meta_df, self.meta = self.get_meta()
        schema = table = pa.Table.from_pandas(meta_df).schema

        print("Writing table")
        with pq.ParquetWriter(self.path_out, schema) as writer:
            for idx, (df, _) in enumerate(self.chunks):
                if self.verbose:
                    print(f"Writing chunk: {idx: >4}")

                table = pa.Table.from_pandas(df)
                writer.write_table(table)

        print("Writing metadata")
        self.write_meta_to_json()
        self.write_meta_to_pickle()
        print("Done")


def read_parquet_in_chunks(
    path: str, columns: Optional[list[str]] = None
) -> Iterator[pd.DataFrame]:
    parquet_file = pq.ParquetFile(path)
    for table in parquet_file.iter_batches(columns=columns):
        df = table.to_pandas()
        yield df


def read_metadata_container(path: str) -> dict[str, Any]:
    with open(path, "rb") as file:
        return pickle.load(file)


def read_meta_from_json(path: str) -> dict[str, Any]:
    with open(path) as file:
        return json.load(file)
