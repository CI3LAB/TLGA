import numpy as np

class Comcost():

    def __init__(self, wp_code, pre, taskdur, workload, cpm):
        self.wp_code = wp_code
        self.pre = pre
        self.taskdur = taskdur
        self.workload = workload
        self.cpm = cpm

    def com_wp_num(self):
        if self.wp_code[1][1] == 1:             
            p = np.sum(self.wp_code[1]) - 2
        else:
            p = np.sum(self.wp_code[1]) - 1
        return p

    def com_wp(self):
        w_divide_index = np.where(self.wp_code[1]==1)[0]
        work_package = []
        for i in range(len(w_divide_index)-1):
            single_wp = self.wp_code[0][w_divide_index[i]:w_divide_index[i+1]]
            work_package.append(tuple(single_wp))
        return(work_package)

    def com_wp_workload(self):
        w_divide_index = np.where(self.wp_code[1]==1)[0]
        rearrange_workload = []
        for j in self.wp_code[0]:
            rearrange_workload.append(self.workload[j])
        rearrange_workload = np.array(rearrange_workload)

        wp_taskdur = []
        for k in range(len(w_divide_index)-1):
            single_wp = rearrange_workload[w_divide_index[k]:w_divide_index[k+1]]
            wp_taskdur.append(single_wp)


        wp_workload = []
        for l in wp_taskdur:
            wp_workload.append(np.sum(l))
        return(wp_workload)

    def com_wp_duration(self):
        work_package = self.com_wp()
        wp_duration = []
        for q in work_package:
            q = np.insert(q,0,0)                        
            temp_pre = [()]
            for i in q[1:]:
                if len(set(self.pre[i]) & set(q)) != 0:                          
                    temp_pre.append(tuple(set(self.pre[i]) & set(q)))      
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
                local_eft[index] = local_est[index] + self.taskdur[j]
                index += 1

            single_wp_duration = np.max(local_eft)
            wp_duration.append(single_wp_duration)
        return wp_duration

    def com_wpcw(self):
        work_package = self.com_wp()
        wp_duration = self.com_wp_duration()
        wp_pre = [()]
        for i in work_package[1:]:
            all_predecessors = set()
            for j in i:
                all_predecessors = all_predecessors | set(self.pre[j])
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

    def com_cost(self):
        p = self.com_wp_num()
        wp_workload = self.com_wp_workload()
        wp_eft = self.com_wpcw()
        true_d = np.max(wp_eft)
        # print(p)
        # print(wp_workload)
        # print(wp_eft)
        cost = 50 * p + np.sum(2 * 3 * np.power(wp_workload,0.8) + np.power(wp_workload,1.2)) + 50 * np.sum(wp_workload * (1 - np.power(2.71, -0.00025*wp_eft )))
        if true_d > self.cpm * 1.1:
            cost = cost * (2 - self.cpm * 1.1 / true_d)
        return cost

