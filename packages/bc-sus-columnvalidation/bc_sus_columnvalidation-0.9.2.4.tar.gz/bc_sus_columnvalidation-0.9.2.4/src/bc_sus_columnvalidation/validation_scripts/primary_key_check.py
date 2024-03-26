import pandas as pd


def primary_key_check(column_df):
   
   
    duplicates = column_df.duplicated(keep=False)
    if not duplicates.any():
        return True
    duplicate_values = column_df[duplicates]
    duplicate_value_indices = duplicate_values.index.tolist()
    duplicate_value_indices = [x + 2 for x in duplicate_value_indices]
    return {
        "No of rows failed": len(duplicate_values),
        "rows_which_failed": duplicate_value_indices,
    }
