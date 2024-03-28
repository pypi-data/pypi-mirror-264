import re
from io import BytesIO
from typing import Union

import chardet
import duckdb
import pandas as pd
from duckdb.typing import BOOLEAN, VARCHAR
from pydantic import BaseModel


class DataSeries(BaseModel):
    fields: list[str]
    data: list[tuple]


class DuckDBEngine:
    # https://duckdb.org/docs/sql/data_types/overview.html#general-purpose-data-types
    # https://duckdb.org/docs/api/python/conversion.html
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        self.conn = conn
        self.conn.create_function(
            "can_cast",
            self.can_cast,
            [VARCHAR, VARCHAR],
            BOOLEAN,
        )

    def execute(self, query):
        return self.conn.execute(query)

    @staticmethod
    def can_cast(value: str, dtype: str) -> bool:
        """
        Check if a value can be cast to a given data type.
        """

        # If value is None, it can be cast to any data type
        if value is None:
            return True

        # Normalize value and data type
        value_ = value.strip()
        dtype_ = dtype.lower()

        # Handle each data type casting
        if dtype_ in ("varchar", "text", "nvarchar", "clob"):
            return True

        elif dtype_ == "boolean":
            if value_ in ("true", "false", "1", "0"):
                return True
            else:
                return False

        elif dtype_ == "date":
            if (
                # YYYY-MM-DD
                re.match(r"\d{4}-\d{2}-\d{2}", value_)
                or
                # MM-DD-YYYY
                re.match(r"\d{2}-\d{2}-\d{4}", value_)
                or
                # MM/DD/YYYY
                re.match(r"\d{2}/\d{2}/\d{4}", value_)
            ):
                return True
            else:
                return False

        elif dtype_ in ("int", "integer", "bigint", "hugeint"):
            try:
                int(value_)
                return int(value_) == float(value_)
            except ValueError:
                return False

        elif dtype_ in ("float", "double", "decimal"):
            try:
                float(value_)
                return True
            except ValueError:
                return False

        else:
            raise ValueError(f"Unknown data type: {dtype}")

    def load_file(self, file_path: str, table: str, **options) -> None:
        file_format = file_path.split(".")[-1]
        if file_format == "csv":
            with open(file_path, "rb") as f:
                data = f.read()
                encoding = chardet.detect(data).get("encoding")
                df = pd.read_csv(BytesIO(data), dtype=str, encoding=encoding, **options)

                self.conn.execute(
                    f"""create or replace table {table} AS
                       select
                            row_number() over () as row_id,
                            * 
                       from df
                    """
                )

        elif file_format in ("xlsx", "xls"):
            open_options = {
                "HEADERS": "FORCE",
                "FIELD_TYPES": "STRING",
                **options,
            }
            open_options_str = ", ".join(
                [f"'{k}={v}'" for k, v in open_options.items()]
            )
            self.conn.execute(
                f"""create or replace table {table} AS
                select row_number() over () as row_id, *
                from st_read(?, open_options=[{open_options_str}])""",
                [file_path],
            )

        else:
            raise ValueError(f"Unknown file format: {file_format}")

    def fetchall(
        self,
        query: str,
        format="dataseries",
    ) -> Union[pd.DataFrame, DataSeries]:
        if format == "dataframe":
            return self.conn.execute(query).fetchdf()

        elif format == "dataseries":
            df = self.conn.execute(query).fetchdf()
            fields = df.columns.tolist()
            data = df.apply(lambda row: tuple(row), axis=1).tolist()
            return DataSeries(fields=fields, data=data)

        else:
            raise ValueError(f"Unknown format: {format}")

    def create_table_from_query(
        self, query: str, table: str, temp: bool = False
    ) -> str:
        self.conn.execute(f"DROP TABLE IF EXISTS {table}")
        self.conn.execute(
            f"CREATE {'TEMPORARY ' if temp else ''}TABLE {table} AS {query}"
        )
        return table

    def create_table_from_df(self, df: pd.DataFrame, table: str) -> None:
        self.conn.from_df(df).create(table)

    def get_schema(self, table) -> dict[str, str]:
        df = self.conn.execute(f"PRAGMA table_info('{table}')").fetchdf()
        schema = {}
        for _, col in df.iterrows():
            schema[col["name"]] = col["type"]
        return schema
