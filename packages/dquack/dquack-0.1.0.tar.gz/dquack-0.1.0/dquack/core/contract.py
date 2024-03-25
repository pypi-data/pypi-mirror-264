from typing import Optional, Union

from pydantic import BaseModel, Field


class Constraint(BaseModel):
    type_: str = Field(alias="type")
    name: Optional[str] = None
    expression: Optional[Union[str, list]] = None
    config: dict = {}


class Column(BaseModel):
    name: str
    description: Optional[str] = None
    data_type: str
    constraints: list[Constraint] = []
    configs: dict = {}


class Table(BaseModel):
    name: str
    columns: list[Column]
    configs: dict = {}
