import os
from typing import Dict, List, Set

from graphlib import TopologicalSorter

from goshawk.domain.model import SQLModel

from ..settings import Settings

app_settings = Settings()


def get_database_paths() -> List[str]:
    return [f.path for f in os.scandir(app_settings.MODELS_PATH) if f.is_dir()]


def get_schema_paths(database_path: str) -> List[str]:
    return [f.path for f in os.scandir(database_path) if f.is_dir()]


def get_files(schema_path: str) -> List[str]:
    return [f.path for f in os.scandir(schema_path) if f.path.endswith(".sql")]


def read_files() -> List[SQLModel]:
    models = []
    for database in get_database_paths():
        for schema in get_schema_paths(database):
            for sqlfile in get_files(schema):
                model = SQLModel(database, schema, sqlfile, sqlfile)
                models.append(model)
    return models


def build_dag(models: List[SQLModel]) -> TopologicalSorter:
    ts: TopologicalSorter = TopologicalSorter()
    for m in models:
        for s in m.schemas:
            if s.startswith("REPORTING."):
                ts.add(m._schema, s)
    return ts


def build_schema_dag(models: List[SQLModel]) -> Dict[str, Set[str]]:
    schemas: Dict[str, Set[str]] = {}
    for m in models:
        if m._schema not in schemas:
            schemas[m._schema] = set()

        for t in m.parent_tables:
            tschema = f"{t.split('.')[0]}.{t.split('.')[1]}"
            if tschema != m._schema:
                schemas[m._schema].add(tschema)         
    return schemas
