import os
import sys
from subprocess import check_call, check_output
import shlex
from threading import Thread
import numpy as np
import pandas as pd

'''
step three: To plot lifetime of top 100 pc over entire run of workload
input: folder path containing edge_life.log, if too big split it 'split -l 10000 edge_life.log'
       " python3 /mnt/A/tools/lineplot_life.py . " 
'''

sim_cycles = 599552053#int(input("simualtion cycles?"))
topk_csv = "../chain/test.csv"#str(input("top_k edge freq (test.csv)?"))

#####################################
pc_list = []
timeline = []
dist = []

path = sys.argv[1]
files = os.listdir(path)
files = [f for f in files if os.path.isfile(path+'/'+f)]
fileObj = []
for i in range(len(files)):
    f = open(files[i], 'r')
    fileObj.append(f)

no_process = len(files)
#######################################


def func_main(f, pc_list, timeline, dist):
    for line in f:
        line = line.lstrip().rstrip()
        split = line.split(',')

        pc_list.append(split[0])
        
        if len(split)<=2:
            continue

        split = split[1:len(split) - 1] # ignore pc (at [0]) and new line at the end

        cycles = [int(i) for i in split]

        # print(str(split[0]) + "," + " start: {}, end: {}".format(cycles[0], cycles[len(cycles) - 1]))
        
        diff = abs(cycles[len(cycles) - 1] - cycles[0])
        dist.append( (float)(diff/sim_cycles) *100 )

        timeline.append(cycles)

all_t = []
for i in range(no_process):
    t = Thread(target=func_main, args=(fileObj[i], pc_list, timeline, dist))
    t.start()
    all_t.append(t)

for t in all_t:
    t.join()

import seaborn as sns
import matplotlib.pyplot as plt
import math

topdf = pd.read_csv(topk_csv, sep=' ')
topdf.columns = ['a','b','c']

topdf['a'] = topdf['a'].apply(int, base=16)
topdf['b'] = topdf['b'].apply(int, base=16)

topdf['a'] = topdf['a'].apply(str)
topdf['b'] = topdf['b'].apply(str)

topdf['pc'] = topdf['a'] +'_'+ topdf['b']

# sns.set(rc={'figure.figsize':(13,5)})

newdf = pd.DataFrame({'pc':pc_list, 'tc':dist})
newdf['index'] = newdf.index

res = pd.DataFrame.merge(topdf, newdf, on='pc')

res = res.drop(res[res['a'] == res['b']].index)

print("top 10")
byc = res.sort_values('c', ascending=False)
print(byc.head(10))

print("low 10")
byc = res.sort_values('c', ascending=True)
print(byc.head(10))


# print("top 10")
# bytc = res.sort_values('tc', ascending=False)
# print(bytc.head(10))

# print("low 10")
# bytc = res.sort_values('tc', ascending=True)
# print(bytc.head(10))

byc = res.sort_values('c', ascending=False).head(100)
ax = byc.plot(x='index', y='c', kind='bar', legend=False, rot=30, width=0.4)
# ax.bar_label(res['pc'], label_type='edge')
plt.show()



