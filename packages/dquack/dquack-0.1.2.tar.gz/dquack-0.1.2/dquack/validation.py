from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel

from dquack.cores.contract import Column, Dataset


class CheckStatus(Enum):
    SUCCESS = 0
    FAILURE = 1


class CheckResult(BaseModel):
    dataset: Dataset
    column: Column
    status: CheckStatus
    message: Optional[str] = None
    sample: Optional[str] = None


class Check:
    def __init__(self, dataset: Dataset):
        self.dataset = dataset

    def evaluate(self):  # -> CheckResult:
        pass

    def check(self):
        for column in self.dataset.columns:
            for constraint in column.constraints:
                if constraint.type_ == "unique":
                    print(f"Checking unique constraint for {column.name}")
                    # check unique constraint if not unique, raise error
                elif constraint.type_ == "not_null":
                    print(f"Checking not null constraint for {column.name}")
                    # check not null constraint
                    # if null, raise error
                elif constraint.type_ == "check":
                    print(f"Checking check constraint for {column.name}")
                    # check check constraint
                    # if not satisfied, raise error
                elif constraint.type_ == "foreign_key":
                    print(f"Checking foreign key constraint for {column.name}")
                    # check foreign key constraint
                    # if not satisfied, raise error
                elif constraint.type_ == "custom":
                    print(f"Checking custom constraint for {column.name}")
                    # check custom constraint
                    # if not satisfied, raise error
                else:
                    raise ValueError(f"Unknown constraint type: {constraint.type_}")
        return True
