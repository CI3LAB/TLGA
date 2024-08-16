import numpy as np
import copy
import math


class SSGS():

    def __init__(self, addr):
        self.addr = addr
        

    def loaddata(self):
        with open(self.addr) as f:
            pro_data = []
            taskdur = ()
            workload = ()
            num_successors = ()
            tasksuc = ()
            inact = ()

            for i in f.readlines():
                line = i.strip().split()
                line = list(map(int, line))
                pro_data.append(line)

            heur_numactwp = pro_data[0][0]
            tasknum = len(pro_data) - 1
            for i in pro_data[1:]:                                  
                taskdur += (i[2], )
                workload += (i[1], )
                num_successors += (i[3], )
                tasksuc += (i[4:], )
                inact += (i[0], )
            
            inact_index = np.where(np.array(inact)==1)[0]
        return tasksuc, np.array(taskdur), np.array(num_successors), np.array(workload), tasknum, inact_index, heur_numactwp


    def compre(self):
        tasknum = self.loaddata()[4]
        tasksuc = self.loaddata()[0]
        taskpre = [() for _ in range(tasknum)]
        index = 0
        for i in tasksuc:
            for j in i:
                taskpre[j-1] += (index, )
            index += 1
        return tuple(taskpre)
    
    def com_cpm(self):
        tasknum = self.loaddata()[4]
        taskpre = self.compre()
        taskdur = self.loaddata()[1]

        estart = np.zeros(tasknum)
        efinish = np.zeros(tasknum)
        for i in range(1,tasknum):
            estart[i] = np.max(efinish[taskpre[i],])
            efinish[i] = estart[i] + taskdur[i]
        return np.max(efinish)



def feasible_test(order,pre):
    flags = []
    for i in order:
        index_i = np.where(order==i)[0][0]
        if all(np.in1d(pre[i],order[0:index_i])):
            flag = 1
        else:
            flag = 0
        flags.append(flag)
    if sum(flags) == len(order):
        fea = True
    else:
        fea = False
    return fea

def div_inact(index,mode_list):

    
    for i in index[1:-1]:
        mode_list[i] = 1
        mode_list[i+1] = 1

    for j in index:
        if j-1 in index:
            mode_list[j] = 0
    mode_list[0] = 1
    mode_list[-1] = 1
    return mode_list




def wp_dvi(m, temp_index, heur_numactwp):
    mode_list = np.zeros(m, dtype=int)
    act_idnex = np.random.choice(np.arange(1,len(mode_list)), heur_numactwp, replace=False) 
    for i in act_idnex:
        mode_list[i] = 1
    
    mode_list = div_inact(temp_index, mode_list)
    return mode_list


def get_index_from_array(from_array, purpose_array):
    purpose_array = np.array(purpose_array)
    from_array = np.array(from_array)
    purpose_idx_in_from = -np.ones(purpose_array.shape).astype(int)     
    p_idx = np.in1d(purpose_array, from_array)      
    union_array = np.hstack((from_array, purpose_array[p_idx]))        
    _, union_idx, union_inv = np.unique(union_array, return_index=True, return_inverse=True)    
    purpose_idx_in_from[p_idx] = union_idx[union_inv[len(from_array):]] 
    return purpose_idx_in_from


def com_wp(wp_code):
    w_divide_index = np.where(wp_code[1]==1)[0]
    work_package = []
    for i in range(len(w_divide_index)-1):
        single_wp = wp_code[0][w_divide_index[i]:w_divide_index[i+1]]
        work_package.append(tuple(single_wp))
    return(work_package)

def com_wp_duration(work_package,pre,taskdur):
    wp_duration = []
    for q in work_package:
        q = np.insert(q,0,0)                      
        temp_pre = [()]
        for i in q[1:]:
            if len(set(pre[i]) & set(q)) != 0:                          
                temp_pre.append(tuple(set(pre[i]) & set(q)))      
            else:
                temp_pre.append((0,))                                 
                        

        local_est = np.zeros(len(temp_pre))
        local_eft = np.zeros(len(temp_pre))
        index = 1
        for j in q[1:]:
            local_temp_index = []
            for k in temp_pre[index]:
                local_temp_index.append(np.where(q==k)[0])               
    
            local_est[index] = np.max(local_eft[local_temp_index,])
            local_eft[index] = local_est[index] + taskdur[j]
            index += 1

        single_wp_duration = np.max(local_eft)
        wp_duration.append(single_wp_duration)
    return wp_duration



def com_wpcw(work_package,pre,wp_duration):
    wp_pre = [()]
    for i in work_package[1:]:
        all_predecessors = set()
        for j in i:
            all_predecessors = all_predecessors | set(pre[j])
        i_predecessors = ()
        for k in work_package[0:work_package.index(i)]:
            if set(k) & all_predecessors != set():
                i_predecessors += (work_package.index(k),)
        wp_pre.append(i_predecessors)

    wp_est = np.zeros(len(work_package))
    wp_eft = np.zeros(len(work_package))
    wp_eft[0] = wp_est[0] + wp_duration[0]
    for i in range(1,len(work_package)):
        wp_est[i] = np.max(wp_eft[wp_pre[i],])
        wp_eft[i] = wp_est[i] + wp_duration[i]

    return wp_eft

def list_generation(tasknum, p, inact_index, heur_numactwp):
    # flag = 1
    # while flag:
    init_order = np.arange(0,tasknum,1)
    task_list = np.array([0])
    while len(init_order)!= 0:
        init_order = np.setdiff1d(init_order,task_list,assume_unique=True)  
        temp_list = np.array([])                                            
        for i in init_order:
            if all(np.in1d(p[i],task_list)):
                temp_list = np.append(temp_list,i)
        if len(temp_list) > 1:                                            
            temp_list= np.random.permutation(temp_list)                    
            task_list = np.append(task_list,temp_list[0])
        else:
            task_list = np.append(task_list,temp_list)
    temp_index = get_index_from_array(task_list, inact_index)
    mode_list = wp_dvi(tasknum, temp_index, heur_numactwp)

    mm_list = np.vstack((task_list,mode_list)).astype(int)

    return mm_list



