import os
import sys
from subprocess import check_call, check_output
import shlex
from threading import Thread
import numpy as np
import pandas as pd


path = sys.argv[1]
df = pd.read_csv(path, sep=',')

'''COL HEX string TO INT'''
def hexstr2int():
    df['broken']=df['broken'].apply(str)
    df.broken = df.broken.apply(lambda x: int(x, 16))
    df.to_csv("broken_anda.log", index=False)

def merge_broken_edgfreq():
    root = "/mnt/A/Champsim2/test2"
    brk = root +'/broken_anda.log'
    edg = root +'/chain/test.csv'
    df1 = pd.read_csv(brk, sep=',')
    df2 = pd.read_csv(edg, sep=' ')
    res = pd.DataFrame.merge(df1, df2, on=['a','b'])
    res['d'] = res['a'] == res['b']
    res.to_csv("broken_freq.log")

merge_broken_edgfreq()