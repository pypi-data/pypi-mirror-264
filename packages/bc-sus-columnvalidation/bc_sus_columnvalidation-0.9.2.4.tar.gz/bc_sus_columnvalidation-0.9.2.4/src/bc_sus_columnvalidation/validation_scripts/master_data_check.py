import pandas as pd
import logging



def master_data_check(
    master_df,
    excel_df,
    lookup_column_name,
    excel_column_name,
    primary_key_in_excel="",
    primary_key_in_master="",
):
    """Function for Master Data checks. Requires master data Dataframe which contains the lookup values and the Excel Dataframe for which validation has to be carried out.
       Regarding primary_key_in_excel & priamry_key_in_master:
            1) Generic lookup checks if the field in excel is in the master data and if not it fails. But there are cases where we need to do row wise check instead \
                of just lookup. For eg: IN CERT_CERTIFICATION_CONCAT, each farmer certification should fall within the corresponding group of values within \
                CERT_CERTIFICATION_CONCAT which requires a composite of farmer code and certification in both the excel file AND the master data check which can now be \
                compared and evaluated. 
            
                
    Args:
        master_df (pd.Dataframe): Pandas dataframe that contains the relevant master data columns and fields for lookup checks
        excel_df (pd.Dataframe): Pandas dataframe that contains the user uploaded excel file data for which validation has to be done.
        lookup_column_name (str): Master data Lookup column i.e column name in master data table e.g "FARMER_CODE" etc
        excel_column_name (str): Corresponding Column name in excel  for eg. "Farmer Code" in excel has to validated against "FARMER_CODE" in master data
        primary_key_in_excel (str, optional): name of the column in excel which is required for multi-column filtering and lookup. Defaults to "".
        primary_key_in_master (str, optional): name of the column in master data corresponding to primary_key_in_excel. Defaults to "".

    Returns:
        dict: 
    """
    logging.info("master data check is started")

    if primary_key_in_master != "":

        excel_df_copy = excel_df[
            (excel_df[excel_column_name] != "") & (excel_df[excel_column_name].notna())
        ]
        excel_df_copy = excel_df_copy.reset_index(names="Original Index")
        

        excel_df_main = excel_df_copy.rename(
            columns={primary_key_in_excel: primary_key_in_master}
        )

        merged_df = pd.merge(
            excel_df_main, master_df, on=primary_key_in_master, how="left"
        )

        non_empty_merged_df = merged_df.dropna(subset=[lookup_column_name])

        def certification_concat_check(row):

            certifications_set = set(row[lookup_column_name].lower().split(", "))
            if type(row[excel_column_name]) == str:
                return row[excel_column_name].lower() in certifications_set
            else:
                return False

        error_column_name = lookup_column_name.lower()
        non_empty_merged_df[error_column_name] = non_empty_merged_df.apply(
            certification_concat_check, axis=1
        )

        logging.info("merged_df of lookup column done")
        failed_master_data_check_rows = non_empty_merged_df[
            ~non_empty_merged_df[error_column_name]
        ]["Original Index"].tolist()

        if len(failed_master_data_check_rows) == 0:
            return True
        wrong_master_data_rows = failed_master_data_check_rows
        wrong_master_data_rows = [x + 2 for x in wrong_master_data_rows]
        return {
            "No of rows failed": len(wrong_master_data_rows),
            "rows_which_failed": wrong_master_data_rows,
        }
    elif "BC Farmer" in excel_df and lookup_column_name == "FARMER_CODE":
        # for the case where we need to check farmer code in master data only if they are BC Farmers.
        master_data_column_df = master_df[lookup_column_name]
        excel_df = excel_df[excel_df["BC Farmer"] == True]
        bc_farmer_excel_filter_df = excel_df[excel_column_name]

        def lowercase_if_string(value):
            if isinstance(value, str):
                return value.lower()
            return value

        # check for and filter for empty strings, null values in excel and master data column df
        non_empty_master_column_df = master_data_column_df[
            (master_data_column_df != "") & (master_data_column_df.notna())
        ]
        non_empty_master_column_df = non_empty_master_column_df.apply(
            lowercase_if_string
        )
        non_empty_bc_farmer_df = bc_farmer_excel_filter_df[
            (bc_farmer_excel_filter_df != "") & (bc_farmer_excel_filter_df.notna())
        ]
        non_empty_bc_farmer_df = non_empty_bc_farmer_df.apply(lowercase_if_string)

        is_in_master_data_df = non_empty_bc_farmer_df.isin(non_empty_master_column_df)

        failed_master_data_check_rows = is_in_master_data_df[
            ~is_in_master_data_df
        ].index.tolist()

        if len(failed_master_data_check_rows) == 0:
            return True
        wrong_master_data_rows = failed_master_data_check_rows
        wrong_master_data_rows = [x + 2 for x in wrong_master_data_rows]
        return {
            "No of rows failed": len(wrong_master_data_rows),
            "rows_which_failed": wrong_master_data_rows,
        }

    else:
        master_data_column_df = master_df[lookup_column_name]
        column_df = excel_df[excel_column_name]

        def lowercase_if_string(value):
            if isinstance(value, str):
                return value.lower()
            return value

        # check for and filter for empty strings, null values in excel and master data column df
        non_empty_master_column_df = master_data_column_df[
            (master_data_column_df != "") & (master_data_column_df.notna())
        ]
        non_empty_master_column_df = non_empty_master_column_df.apply(
            lowercase_if_string
        )
        non_empty_excel_df = column_df[(column_df.notna()) & (column_df != "")]
        non_empty_excel_df = non_empty_excel_df.apply(lowercase_if_string)

        is_in_master_data_df = non_empty_excel_df.isin(non_empty_master_column_df)

        failed_master_data_check_rows = is_in_master_data_df[
            ~is_in_master_data_df
        ].index.tolist()

        if len(failed_master_data_check_rows) == 0:
            return True
        wrong_master_data_rows = failed_master_data_check_rows
        wrong_master_data_rows = [x + 2 for x in wrong_master_data_rows]
        return {
            "No of rows failed": len(wrong_master_data_rows),
            "rows_which_failed": wrong_master_data_rows,
        }