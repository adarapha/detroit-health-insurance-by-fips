import pandas as pd 
import pdb

def clean_df():
    """
    cleaning original dataset:
        - dropping unused columns
        - ensuring no strings
        - indexing by zip
    """
    df = pd.read_csv("data/insurance_by_zip.csv")
    df = df.drop(["ObjectId"], axis=1)
    df = df[pd.to_numeric(df['Geography'], errors='coerce').notnull()]
    df['Estimated_Percent_Insured'] = df['Estimated_Percent_Insured'].astype(int)
    df['Geography'] = df['Geography'].astype(int)
    df["ZIP"] = df["Geography"]
    df = df.drop(['Geography'], axis=1)
    df = df.set_index('ZIP')
    return df

def zip_list():
    """
    create and standardize list of detroit zipcodes
    """
    df = pd.read_csv("data/insurance_by_zip.csv")
    df = df.drop(["ObjectId", 'Estimated_Percent_Insured'], axis=1)
    df = df[pd.to_numeric(df['Geography'], errors='coerce').notnull()]
    zips = df['Geography'].tolist()
    zips = [int(i) for i in zips]
    return zips

det_zips = zip_list()

def clean_lookup():
    """
    cleaning original dataset:
        - dropping unused columns, values
        - making sure everything is int
        - indexing by zip
        - dropping non-detroit zips
        - deduping
    """
    df = pd.read_csv("data/lookup.csv")
    df = df.drop(["COUNTYNAME", "STATE", "CLASSFP"], axis=1)
    df['ZIP'] = df['ZIP'].astype(int)
    df['STCOUNTYFP'] = df['STCOUNTYFP'].astype(int)
    df = df.drop_duplicates(subset=['ZIP'])
    df = df[df['ZIP'].isin(det_zips)]
    df = df.set_index('ZIP')
    df = df.sort_index()
    return df

def merge():
    """
    join both dataframes
    convert fips back to str
    """
    dff = clean_df()
    df_lookup = clean_lookup()
    df_total = dff.merge(df_lookup, on="ZIP", how='left')
    df_total["STCOUNTYFP"] = df_total["STCOUNTYFP"].astype(str)
    return df_total
