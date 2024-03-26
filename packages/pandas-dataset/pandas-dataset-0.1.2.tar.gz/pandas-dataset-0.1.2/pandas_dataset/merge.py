""""Merge module for dataset objects"""
from typing import Dict, Tuple
import pandas as pd
from .column_types import ColumnType

def merge_datasets(dataset1: "Dataset", dataset2: "Dataset", *args, must_be_disjoint: bool, **kwargs
                  ) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Dict[str, ColumnType]]]:
    """Merges two datasets together. Calls underlying pd.merge only on needed data groups"""
    new_data: Dict[str, pd.DataFrame] = {}
    new_column_types: Dict[str, Dict[str, ColumnType]] = {}
    tbs_together = set(dataset1.tables).union(dataset2.tables)
    for tb in tbs_together:
        if tb not in dataset1.tables:
            new_data[tb] = dataset2[tb]
            new_column_types[tb] = dataset2.column_types[tb]
            continue

        if tb not in dataset2.tables:
            new_data[tb] = dataset1[tb]
            new_column_types[tb] = dataset1.column_types[tb]
            continue

        tb1: pd.DataFrame = dataset1[tb]
        tb2: pd.DataFrame = dataset2[tb]
        if tb2.index.name != tb1.index.name:
            raise KeyError(f"Index name mismatch: '{tb1.index.name}' vs '{tb2.index.name}'")

        common_cols = dataset1[tb].columns.intersection(tb2.columns)
        if len(common_cols) > 0 and must_be_disjoint:
            raise ValueError(f"Got common cols: {common_cols}, but must_be_disjoin is set to True.")

        tb2 = tb2.drop(columns=common_cols)
        new_data[tb] = pd.merge(tb1, tb2, on=dataset1.primary_keys[tb], *args, **kwargs)
        new_column_types[tb] = {**dataset1.column_types[tb], **dataset2.column_types[tb]}
    return new_data, new_column_types
