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

        
if __name__ == '__main__':
    result = open('D:\\Documents\\python_work\\PSP_Code\\workpackage\\results\\tasknum\\sj160.txt','w')
    path = r"D:\\Documents\\python_work\\PSP_Code\\workpackage\\org_wpcode\\sj160"
    files = os.listdir(path)
    for i in range(0, len(files)):
        ad = path +'\\' + files[i]
        print(files[i])
        result.write("{}".format(files[i])+'\n')
        org_code = np.loadtxt(ad)
        for i in org_code:
            wp_code = i.reshape(2,-1)
            task_num = com_tasknuminwp(wp_code)
            meantasknum, stdtasknum = compute_ave_std(task_num)
            result.write(str(task_num)+'_'+str(meantasknum)+'_'+str(stdtasknum)+'\n')