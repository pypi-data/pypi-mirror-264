from __future__ import annotations  # Should be able to remove in py 3.10

from enum import Enum

from sqlglot import exp, parse_one


class SourceTable:
    def __init__(self, fqn: str, table_exp: exp.Table):
        parts = fqn.split(".")
        db = parts[0]
        schema = db + "." + parts[1]

        if len(table_exp.parts) == 3:
            assert isinstance(table_exp.parts[0], exp.Identifier)  # this pleases mypy
            assert isinstance(table_exp.parts[1], exp.Identifier)
            self.table_catalog = (
                table_exp.parts[0].name if table_exp.parts[0].quoted else table_exp.parts[0].name.upper()
            )
            self.table_schema = (
                self.table_catalog + "." + table_exp.parts[1].name
                if table_exp.parts[1].quoted
                else self.table_catalog + "." + table_exp.parts[1].name.upper()
            )
        if len(table_exp.parts) == 2:
            assert isinstance(table_exp.parts[0], exp.Identifier)
            self.table_schema = (
                db + "." + table_exp.parts[0].name
                if table_exp.parts[0].quoted
                else db + "." + table_exp.parts[0].name.upper()
            )
            self.table_catalog = db
        if len(table_exp.parts) == 1:
            self.table_schema = schema
            self.table_catalog = db
        self.table_name = table_exp.name if table_exp.this.quoted else table_exp.name.upper()
        self.fqn = f"{self.table_schema}.{self.table_name}"


class ModelTypes(str, Enum):
    view = "view"
    table = "table"


class SQLEx(Exception):
    pass


def fqn_schema(fqn: str) -> str:
    if len(fqn.split(".")) != 3 and 1 == 2:
        raise SQLEx()
    return f"{fqn.split('.')[0]}.{fqn.split('.')[1]}"


class SQLModel:
    def __init__(self, database: str, schema: str, name: str, filepath: str, schema_entry: str = "None"):
        self._filepath = filepath
        self._database = filepath.split("/")[-3].upper()
        self._schema = self._database + "." + filepath.split("/")[-2].upper()
        self._name = filepath.split("/")[-1].upper().removesuffix(".SQL")
        self.fqn = f"{self._schema}.{self._name}"
        with open(filepath) as f:
            self._raw_sql = f.read()
        self._parsed_sql = parse_one(self._raw_sql, dialect="snowflake")
        self._ctes = [ex.alias_or_name.upper() for ex in self._parsed_sql.find_all(exp.CTE)]

        self._table_references = [
            t
            for t in self._parsed_sql.find_all(exp.Table)
            if (t.name.upper() not in self._ctes) and (t.this.key != "anonymous")
        ]
        self.parent_tables = {}
        for t in self._table_references:
            source_table = SourceTable(self.fqn, t)
            self.parent_tables[source_table.fqn] = source_table

        self.schemas = {f"{fqn_schema(t)}" for t in self.parent_tables if fqn_schema(t) != self._schema}
