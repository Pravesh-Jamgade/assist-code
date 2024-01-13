import os
import sys
from subprocess import check_call, check_output
import shlex
from threading import Thread
import numpy as np
import pandas as pd

'''
step two: from edges select top 100 of them
input: edge_freq.log
'''
fileName = sys.argv[1]
f = open(fileName, 'r')
entries = []

# for line in f:
#     line_split = line.split(',')
#     first_split = line_split[0].split('_')
#     second_split = line_split[1].lstrip().rstrip()
#     entries.append([first_split[0], first_split[1], second_split])

# df = pd.DataFrame(entries, columns=['a','b','c'])
# df = df.sort_values(by=['c'], ascending=False)
# print(df['c'].max())

for line in f:
    line_split = line.split(',')
    first_split = line_split[0].split('_')
    second_split = line_split[1].lstrip().rstrip()
    entries.append([first_split[0], first_split[1], int(second_split)])

df = pd.DataFrame(entries, columns = ['a','b','c'])
print(df)
# df['a'] = df['a'].apply(int, base=16)
# df['b'] = df['b'].apply(int, base=16)
df = df.sort_values(by=['c'], ascending=False)

print(df.head(200).to_csv("test.csv", index=False, sep=" "))



