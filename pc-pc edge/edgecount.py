import os
import sys
from subprocess import check_call, check_output
import shlex
from threading import Thread
import numpy as np
import pandas as pd


'''
(edgecount)
step one: get all edges from map<intptr, vector<vector<intptr>>>
map from pc to corresponding vector of bag_of_pc
input: pc_chain.log  from champsim simulation
'''

path = sys.argv[1]
f = open(path+'/pc_chain.log', 'r')
out = open(path+'/edge_freq.log', 'w')

freq = {}
for line in f:
    arr = line.split(',')
    arr = arr[0:len(arr)-1]
    if len(arr) <=1:
        continue

    src = arr[0]

    for node in arr[1:]:
        edge = src + '_' + node
        if edge in freq.keys():
            freq[edge]=freq[edge]+1
        else:
            freq[edge]=1


for k,v in freq.items():
    out.write(str(k) + ',' + str(v) + '\n')

import heapq

k_keys_sorted = heapq.nlargest(10, freq, key=freq.get)
print(k_keys_sorted)