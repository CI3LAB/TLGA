import pandas as pd
import numpy as np
import os 

def com_wp(wp_code):
    w_divide_index = np.where(wp_code[1]==1)[0]
    work_package = []
    for i in range(len(w_divide_index)-1):
        single_wp = wp_code[0][w_divide_index[i]:w_divide_index[i+1]]
        work_package.append(tuple(single_wp))
    return(work_package)

def com_tasknuminwp(wp_code):
    wp = com_wp(wp_code)
    wp_tasknum = []
    if len(wp[0]) == 1:
        for i in wp:
            wp_tasknum.append(len(i))
        for j in range(int((len(wp_code[0])-2)/10)-1):
            try:
                wp_tasknum.remove(1)
            except:
                return wp_tasknum
    else:
        for i in wp:
            wp_tasknum.append(len(i))
        for j in range(int((len(wp_code[0])-2)/10)-2):
            try:
                wp_tasknum.remove(1)
            except:
                return wp_tasknum

    return wp_tasknum

def compute_ave_std(lst):
    mean = np.average(np.array(lst))
    std = np.std(np.array(lst),ddof=1)
    return mean, std

        
