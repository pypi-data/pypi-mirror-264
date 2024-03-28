import re
import uuid
from enum import Enum
from typing import Optional, Union

import pandas as pd
from pydantic import BaseModel

from dquack.constant import DEFAULT_INDEX_COLUMN_NAME
from dquack.core.contract import Column, Constraint, Table
from dquack.core.engine import DataSeries, DuckDBEngine


class ConstraintStatus(Enum):
    SUCCESS = 0
    FAILURE = 1
    WARNING = 2
    ERROR = 3


class ColumnConstraintResult(BaseModel):
    column_name: str
    constraint_name: str
    constraint_id: str
    constraint_details: Optional[str] = None
    failed_records: DataSeries

    @property
    def status(self) -> ConstraintStatus:
        if self.failed_records.data:
            status = ConstraintStatus.FAILURE
        else:
            status = ConstraintStatus.SUCCESS

        return status


class ConstraintResult(BaseModel):
    table_name: str
    columns: list[ColumnConstraintResult]

    @property
    def status(self):
        return ConstraintStatus(
            max([column.status.value for column in self.columns])
        ).name.lower()


class ConstraintExecutor:
    def __init__(self, table: Table, engine: DuckDBEngine):
        self.table = table
        self.engine = engine

    @property
    def table_configs(self):
        return self.table.configs or {}

    @property
    def extra_columns(self):
        return self.table_configs.get("extra_columns", [])

    def execute(self) -> ConstraintResult:
        result = ConstraintResult(
            table_name=self.table.name,
            columns=[],
        )

        for column in self.table.columns:
            # Execute data type constraint check
            dtype_result = self.data_type(column.name, column.data_type, column.configs)

            # Only execute other constraints if data type constraint passes
            if dtype_result.status == ConstraintStatus.SUCCESS:
                for constraint in column.constraints:
                    run_result = getattr(self, constraint.type_)(
                        column.name,
                        constraint,
                    )
                    result.columns.append(run_result)
            else:
                result.columns.append(dtype_result)

        return result

    def random_string(self, length: int = 4):
        return str(uuid.uuid4())[:length]

    def get_detailed_result(
        self, result: ConstraintResult
    ) -> Union[pd.DataFrame, None]:
        if result.status == "failure":
            print(f"Table {result.table_name} has failed constraints")
            schema = {
                DEFAULT_INDEX_COLUMN_NAME: "int",
                **{col: "string" for col in self.extra_columns},
                "column_name": "string",
                "constraint_name": "string",
                "column_value": "string",
                "constraint_details": "string",
            }
            failed_records_df = pd.DataFrame(columns=schema.keys()).astype(schema)  # type: ignore

            for column in result.columns:
                if column.status == ConstraintStatus.FAILURE:
                    df = pd.DataFrame(
                        data=column.failed_records.data,
                        columns=column.failed_records.fields,
                    )
                    df["constraint_name"] = column.constraint_name
                    df["column_name"] = column.column_name
                    df["constraint_details"] = column.constraint_details
                    failed_records_df = pd.concat(
                        [failed_records_df, df],
                        axis=0,
                        ignore_index=True,
                        join="inner",
                    )
            return failed_records_df.sort_values(by=DEFAULT_INDEX_COLUMN_NAME)
        else:
            print(f"Table {result.table_name} has passed all constraints")

    def get_overview_result(
        self, result: ConstraintResult
    ) -> Union[pd.DataFrame, None]:
        if result.status == "failure":
            print(f"Table {result.table_name} has failed constraints")
            schema = {
                DEFAULT_INDEX_COLUMN_NAME: "int",
                **{col: "string" for col in self.extra_columns},
            }
            failed_records_df = pd.DataFrame(columns=schema.keys()).astype(schema)  # type: ignore

            for column in result.columns:
                if column.status == ConstraintStatus.FAILURE:
                    df = pd.DataFrame(
                        data=column.failed_records.data,
                        columns=column.failed_records.fields,
                    )
                    failed_records_df = pd.merge(
                        failed_records_df,
                        df,
                        on=list(schema.keys()),
                        how="outer",
                    )
            return failed_records_df
        else:
            print(f"Table {result.table_name} has passed all constraints")

    def missing_columns(self, table_name: str, columns: list[str]):
        pass

    def data_type(self, column_name: str, dtype: str, configs: dict):
        constraint_name = "data_type"
        constraint_id = f"{column_name}_{constraint_name}"
        constraint_details = f"Expected dtype: {dtype}"

        if not configs.get("is_derived_column", False):
            query = f"""
            select
                row_id,
                {', '.join(self.extra_columns)},
                {column_name} as 'column_value'
            from {self.table.name}
            where can_cast({column_name}, '{dtype}') = FALSE
            """

            failed_records: DataSeries = self.engine.fetchall(query)  # type: ignore
            return ColumnConstraintResult(
                column_name=column_name,
                constraint_name=constraint_name,
                constraint_id=constraint_id,
                constraint_details=constraint_details,
                failed_records=failed_records,
            )
        else:
            return ColumnConstraintResult(
                column_name=column_name,
                constraint_name=constraint_name,
                constraint_id=constraint_id,
                constraint_details=constraint_details,
                failed_records=DataSeries(fields=[], data=[]),
            )

    def not_null(
        self,
        columm_name: str,
        constraint: Constraint,
    ):
        constraint_name = constraint.type_
        constraint_id = f"{columm_name}_{constraint_name}"
        constraint_details = "Must not be null"
        query = f"""
        select 
            row_id,
            {', '.join(self.extra_columns)},
            {columm_name} as 'column_value'
        from {self.table.name}
        where {columm_name} is null or trim({columm_name}) = ''
        """

        failed_records: DataSeries = self.engine.fetchall(query)  # type: ignore
        return ColumnConstraintResult(
            column_name=columm_name,
            constraint_name=constraint_name,
            constraint_id=constraint_id,
            constraint_details=constraint.name or constraint_details,
            failed_records=failed_records,
        )

    def unique(
        self,
        column_name: str,
        constraint: Constraint,
    ):
        constraint_name = constraint.type_
        constraint_id = f"{column_name}_{constraint_name}"
        constraint_details = "Must be unique"
        query = f"""
        with duplicate_records as (
            select {column_name}, count(*) as cnt
            from {self.table.name}
            group by {column_name}
            having count(*) > 1
        )
        select 
            row_id,
            {', '.join(self.extra_columns)},
            {column_name} as 'column_value'
        from {self.table.name}
        where {column_name} in (select {column_name} from duplicate_records)
        """

        failed_records: DataSeries = self.engine.fetchall(query)  # type: ignore
        return ColumnConstraintResult(
            column_name=column_name,
            constraint_name=constraint_name,
            constraint_id=constraint_id,
            constraint_details=constraint.name or constraint_details,
            failed_records=failed_records,
        )

    def foreign_key(
        self,
        column_name: str,
        constraint: Constraint,
    ):
        # Ensure that the expression is not empty
        if not constraint.expression:
            raise ValueError("Expression cannot be empty")

        constraint_name = constraint.type_
        constraint_id = f"{column_name}_{constraint_name}_{self.random_string()}"
        constraint_details = f"Value not found in {constraint.expression}"

        ref_table, ref_column = constraint.expression.split(".")

        query = f"""
        select 
            row_id,
            {', '.join(self.extra_columns)},
            {column_name} as 'column_value'
        from {self.table.name}
        where not {column_name} in (
            select distinct {ref_column}
            from {ref_table}
            where {ref_column} is not null
        )
        """

        failed_records: DataSeries = self.engine.fetchall(query)  # type: ignore
        return ColumnConstraintResult(
            column_name=column_name,
            constraint_name=constraint_name,
            constraint_id=constraint_id,
            constraint_details=constraint.name or constraint_details,
            failed_records=failed_records,
        )

    def check(
        self,
        column_name: str,
        constraint: Constraint,
    ):
        # Ensure that the expression is not empty
        if not constraint.expression:
            raise ValueError("Expression cannot be empty")

        constraint_name = constraint.type_
        constraint_id = f"{column_name}_{constraint_name}_{self.random_string()}"
        constraint_details = f"Failed expression: {constraint.expression}"

        query = f"""
        select 
            row_id,
            {', '.join(self.extra_columns)},
            {column_name} as 'column_value'
        from {self.table.name}
        where not ({constraint.expression})
        """

        failed_records: DataSeries = self.engine.fetchall(query)  # type: ignore
        return ColumnConstraintResult(
            column_name=column_name,
            constraint_name=constraint_name,
            constraint_id=constraint_id,
            constraint_details=constraint.name or constraint_details,
            failed_records=failed_records,
        )

    def accept_values(
        self,
        column_name: str,
        constraint: Constraint,
    ):
        if not isinstance(constraint.expression, list):
            raise ValueError("Expression must be a list!")

        match_type = "exact"
        is_case_sensitive = False
        if isinstance(constraint.config, dict):
            match_type = constraint.config.get("match_type", match_type)
            is_case_sensitive = constraint.config.get(
                "is_case_sensitive", is_case_sensitive
            )

        constraint_name = constraint.type_
        constraint_id = f"{column_name}_{constraint_name}_{self.random_string()}"
        constraint_details = "Not found in accepted values"

        if match_type == "exact":
            list_values = ", ".join([f"'{val}'" for val in constraint.expression])
            query = f"""
            select 
                row_id,
                {', '.join(self.extra_columns)},
                {column_name} as 'column_value'
            from {self.table.name}
            where not {column_name} in ({list_values})
            """

        elif match_type == "regex":
            match_flag = "c" if is_case_sensitive else "i"
            condition = " or ".join(
                [
                    f"regexp_matches({column_name}, '{val}', '{match_flag}')"
                    for val in constraint.expression
                ]
            )
            query = f"""
            select 
                row_id,
                {', '.join(self.extra_columns)},
                {column_name} as 'column_value'
            from {self.table.name}
            where not ({condition})
            """
        else:
            raise ValueError(f"Unknown match type: {constraint.config['match_type']}")


        failed_records: DataSeries = self.engine.fetchall(query)  # type: ignore

        return ColumnConstraintResult(
            column_name=column_name,
            constraint_name=constraint_name,
            constraint_id=constraint_id,
            constraint_details=constraint.name or constraint_details,
            failed_records=failed_records,
        )
