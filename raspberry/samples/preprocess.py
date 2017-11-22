import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from pprint import pprint
import csv
from param import *

def load_csv(file):
    data = []
    with open('./'+file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            data.append( [float(i) for i in row[0].split(",")])
    return data

def calc_difference(data, diff_index=[1,2,3]):
    new_data = []
    # diff_index = [1,2,3]

    for i in range(0,len(data)):
        if i == 0 or (data[i][0] - data[i-1][0] >15):
            new_data.append(data[i].copy())
            for j in diff_index:
                new_data[i][j] = 0

        else:
            new_data.append(data[i].copy())
            for j in diff_index:
                new_data[i][j] = data[i][j] - data[i-1][j]
    
    return new_data

# 버튼 여러번 눌린 데이터 삭제
def remove_error_data(data):
    count = 0
    remove_range = []
    before = -1
    i=0

    while i < len(data):
        if data[i][-1] == 1:
            if before == -1:
                before = i
            else:
                diff = data[i][0] - data[before][0]
                if diff <= 200 or diff<0 :
                    remove_range.append((before, i))
                before = i

        i+=1

    for rng in remove_range:
        for idx in range(rng[0], rng[1]+1):
            data[idx][2] = -987

    new_data = []
    for d in data:
        if d[2] != -987:
            new_data.append(d)

    return new_data


# In[5]:


def spread_accident_tag(data, before_gap = 15, after_gap = 30):
    i = 0
    while i < len(data):
        if data[i][-1] == 1:
            j = i-1
            while j >= 0:
                gap = data[i][0] - data[j][0]
                if gap > before_gap:
                    break

                data[j][-1] = 1.0
                j -= 1

            j = i+1
            while j<len(data):
                gap = data[j][0] - data[i][0]
                if gap > after_gap:
                    break
                data[j][-1] = 1.0
                j+=1

            i=j

        i += 1


    return data


def split_xy(data, n_step):
    x_data_orgin = [ row[1:4]+row[5:10] for row in data]
    y_data_orgin = [ row[-1] for row in data]
    x_data = []
    y_data = []

    for i in range(len(y_data_orgin)-n_step+1):    
    #     total = sum(y_data_orgin[i:i+n_step]) 
    #     print(total)
        if y_data_orgin[i+n_step-1] > 0.5:
            for i in range(5):
                x_data.append(x_data_orgin[i:i+n_step])
                y_data.append([0,1])
        else :
            x_data.append(x_data_orgin[i:i+n_step])
            y_data.append([1,0])
    return x_data, y_data

def preprocess(file_name):
    org_data = load_csv(file_name)
    dif_data = calc_difference(org_data)
    rmv_error_data = remove_error_data(dif_data)
    spreaded_data = spread_accident_tag(rmv_error_data)
    x_data, y_data = split_xy(spreaded_data, n_step)
    return x_data, y_data




