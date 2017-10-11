import numpy as np
import pandas as pd
import sklearn as skl
import sys
import itertools as it
import math
from copy import copy
import datetime
import os
import random
from urllib.request import urlretrieve
import json
from pandas.io.json import json_normalize

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from ipywidgets import interact

plt.style.use("fivethirtyeight")
plt.rc("figure", figsize=(5,7))
sns.set_palette('deep')

# Stuff below controls how dataframes are displayed when you use display()
import IPython.display as ipd
digits = 3
pd.options.display.chop_threshold = 10**-(digits+1)
pd.options.display.float_format = lambda x: '{0:.{1}f}'.format(x,digits)
pd.options.display.show_dimensions = True
pd.options.display.max_rows = 30

def display(X):
    if isinstance(X, pd.Series) or (isinstance(X, np.ndarray) and X.ndim <=2):
        ipd.display(pd.DataFrame(X))
    else:
        ipd.display(X)
    return


def tile_rows(v,n):
    return np.tile(v,(n,1))

def tile_cols(v,n):
    return np.tile(v[:,np.newaxis],(1,n))

def margins(df):
    df = pd.DataFrame(df)
    col_sums = df.sum(axis=0)
    df.loc['TOTAL'] = col_sums
    row_sums = df.sum(axis=1)
    df['TOTAL'] = row_sums
    return df

def get_summary_stats(v):    
    ss = pd.DataFrame(v).describe().T
    ss['SE'] = ss['std'] / np.sqrt(ss['count'])
    return ss

def get_champions():
    #Creates a dataframe of champions
    if not os.path.isfile('champion.json'): #if the file isn't already in the directory, download it
        urlretrieve("http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json", 'champion.json')
    with open('champion.json') as json_file:
          data2 = json.loads(json_file.read())
    #these two lines just get rid of some of the JSON header info so that the Dataframe looks nice
    ls = [a for a in data2['data']]
    ls2 = [data2['data'][b] for b in ls]
    champions = pd.DataFrame.from_dict(json_normalize(ls2), orient='columns')
    return champions