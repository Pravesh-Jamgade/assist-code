import os
import sys
from subprocess import check_call, check_output
import shlex
from threading import Thread
import numpy as np
import pandas as pd

'''
first split file using: 
split -l 100000 newpc_chain.csv // split line-wise on command line
'''
edge = []

def func_main(f, edge):
    for line in f:
        spl = line.split(',')
        edge.append([spl[0].lstrip().rstrip(), spl[1].lstrip().rstrip()])

path = sys.argv[1]

files = os.listdir(path)
files = [f for f in files if os.path.isfile(path+'/'+f)]

print(files)

fileObj = []
for i in range(len(files)-1):
    f = open(files[i], 'r')
    fileObj.append(f)

no_process = len(files) - 1

all_t = []
for i in range(no_process):
    t = Thread(target=func_main, args=(fileObj[i], edge))
    t.start()
    all_t.append(t)

for t in all_t:
    t.join()


freq = {}
for e in edge:
    key = str(e[0])+'_'+str(e[1])
    if key in freq.keys():
        freq[key]=freq[key]+1
    else:
        freq[key]=1

keys = list(freq.keys())
values = list(freq.values())

keyval = {'key':keys, 'val':values}
df = pd.DataFrame.from_dict(keyval)

print(df.head(3))
print(df.shape)
df.to_csv("freq.log")

# import seaborn as sns
# import matplotlib.pyplot as plt
# sns.histplot(data=df)
# plt.show()