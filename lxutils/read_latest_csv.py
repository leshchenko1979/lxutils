import os, glob, pandas as pd
from lxutils import *

def read_latest_csv(dir=".", mask='*.csv'):
    list_of_files=glob.glob(
        f"{dir}\\{mask}")
    latest_file=max(list_of_files, key=os.path.getctime)
    log(f'Latest file found - {latest_file}')

    return pd.read_csv(latest_file).drop_duplicates()
