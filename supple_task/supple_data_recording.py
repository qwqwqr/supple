import pandas as pd


# doi oa_status pdf	is_open_access pmc_id supplementary
def data_recording(request_data: list):
    dtype = {
        'doi': 'str',
        'oa_status': 'str',
        'pdf': 'str',
        'is_open_access': 'str',
        'pmc_id': 'str',
        'supplementary': 'str'

    }
    # df_main = pd.read_excel('supple_data/google_drive_2.xlsx', sheet_name='Sheet1', dtype=dtype)
    df_new = pd.read_excel('supple_data/test3.xlsx', sheet_name='Sheet2', dtype=dtype)

    df_new['pmcid'] = df_new['pmcid'].astype(str)
    df_new['doi'] = df_new['doi'].astype(str)

    cols = df_new.columns[1:]
    for row in request_data:
        df_new.loc[len(df_new), cols] = row

    df_new.to_excel('supple_data/test.xlsx', sheet_name='Sheet2', index=False)