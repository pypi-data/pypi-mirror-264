import pandas as pd
import datetime


def datatype_check_date(column_df):
    def datecheck(field):
        date_format = "%d/%m/%Y"

        try:
            dateObject = datetime.datetime.strptime(field, date_format)
            return True

        except ValueError:
            return False

    # we convert the entries to str to do the checks
    column_df = column_df.astype(str)
    non_missing_df = column_df[
        (column_df != "") & (column_df != "nan")
    ]  # null values become 'nan' in the previous step so we account for that

    wrong_date_mask = ~non_missing_df.apply(datecheck)
    # get a list as o/p with the datatype check result(True or false); invert it;
    #  filter the column with that mask and get the failed row indices alone

    wrong_date_rows = non_missing_df[wrong_date_mask]

    if wrong_date_rows.empty:
        return True
    wrong_date_row_numbers = wrong_date_rows.index.tolist()
    wrong_date_row_numbers = [x + 2 for x in wrong_date_row_numbers]
    return {
        "No of rows failed": len(wrong_date_row_numbers),
        "rows_which_failed": wrong_date_row_numbers,
    }
