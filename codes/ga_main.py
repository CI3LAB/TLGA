import numpy as np
import copy
import os
import time
from dwp_det_inact import SSGS,  feasible_test, list_generation, div_inact, get_index_from_array
from com_fitness import Comcost

class GA():
    def __init__(self, addr, init_pop_size, pop_size, MaxGens, mutation_rate):
        self.addr = addr
        self.init_pop_size = init_pop_size
        self.pop_size = pop_size
        self.MaxGens = MaxGens
        self.mutation_rate = mutation_rate


    def get_info(self):
        ssgs = SSGS(addr=self.addr)
        taskdur = ssgs.loaddata()[1]
        tasknum = ssgs.loaddata()[4]
        workload = ssgs.loaddata()[3]
        taskpre = ssgs.compre()
        cpm = ssgs.com_cpm()
        inact = ssgs.loaddata()[5]
        heur_numactwp = ssgs.loaddata()[6]
        return tasknum, taskpre, taskdur, cpm, workload, inact, heur_numactwp


    def get_init_pop(self):
        tasknum = self.get_info()[0]
        taskpre = self.get_info()[1]
        inact = self.get_info()[5]
        heur_numactwp = self.get_info()[6]
        init_pop = list_generation(tasknum, taskpre, inact, heur_numactwp)
        while np.size(init_pop) < self.init_pop_size * tasknum * 2:
            individual = list_generation(tasknum, taskpre, inact, heur_numactwp)
            init_pop = np.vstack((init_pop,individual))
        init_pop = init_pop.reshape(self.init_pop_size, 2, tasknum)
        return init_pop.astype(int)
        
    def random_select(self,pop):
        random_pop = np.random.permutation(pop)
        random_selected_pop = random_pop[0:self.pop_size,:,:]
        return random_selected_pop.astype(int)

    def get_fitness(self,pop):
        i_pre = self.get_info()[1]
        i_taskdur = self.get_info()[2]
        i_cpm = self.get_info()[3]
        i_workload = self.get_info()[4]
        pop_fitness = []
        for i in pop:
            com_fitness = Comcost(wp_code=i,pre=i_pre,taskdur=i_taskdur, workload=i_workload, cpm=i_cpm)
            individual_fitness = com_fitness.com_cost()
            pop_fitness.append(individual_fitness)
        return np.array(pop_fitness)

    def ranking_select(self,pop):
        tasknum = self.get_info()[0]
        pop_fitness = self.get_fitness(pop)
        select_index = np.argsort(pop_fitness)
        ranking_selected_pop = pop[select_index[0]]
        for i in select_index[1:self.pop_size]:
            ranking_selected_pop = np.vstack((ranking_selected_pop,pop[i]))
        ranking_selected_pop = ranking_selected_pop.reshape(self.pop_size,2,tasknum)
        return ranking_selected_pop
        
    def crossover(self,pop_m,pop_f):
        tasknum = self.get_info()[0]
        inact = self.get_info()[5]
        i = 0
        crossover_pop = np.zeros((2,tasknum)) 
        while i < self.pop_size:
            m = pop_m[i]
            f = pop_f[i]

            q = np.random.randint(0,len(m[0]))
            t_d_m = m[0,0:q+1]
            t_d_f = np.setdiff1d(f[0],t_d_m,assume_unique=True)
            t_d = np.append(t_d_m,t_d_f)
            temp_index = get_index_from_array(t_d,inact)

            for j in range(1,len(m[1])-1):
                if m[1][j] + m[1][j+1] == 2:
                    m[1][j] = 0
            
            m_aftercross_modelist = div_inact(temp_index,m[1])

            
            d = np.vstack((t_d,m_aftercross_modelist))
            crossover_pop = np.vstack((crossover_pop,d))

            t_s_f = f[0,0:q+1]
            t_s_m = np.setdiff1d(m[0],t_s_f,assume_unique=True)
            t_s = np.append(t_s_f,t_s_m)
            temp_index = get_index_from_array(t_s,inact)

            for k in range(1,len(f[1])-1):
                if m[1][k] + m[1][k+1] == 2:
                    m[1][k] = 0

            f_aftercross_modelist = div_inact(temp_index,f[1])


            s = np.vstack((t_s,f_aftercross_modelist))
            crossover_pop = np.vstack((crossover_pop,s))
            i += 1
        crossover_pop = crossover_pop.reshape(self.pop_size*2+1,2,tasknum).astype(int)
        return crossover_pop[1:]
            
    def mutation(self,pop,pre):
        tasknum = self.get_info()[0]
        inact = self.get_info()[5]
        mutation_pop = np.zeros((2,tasknum))
        for indi in pop:
            taskmodelist = indi
            mutation_rate = self.mutation_rate
            m_tasklist = copy.copy(taskmodelist[0])
            m_modelist = copy.copy(taskmodelist[1])
            for i in m_tasklist[1:-1]:
                if np.random.rand() < mutation_rate:
                    index = np.where(m_tasklist==i)[0][0]
                    m_tasklist[index], m_tasklist[index+1] = m_tasklist[index+1], m_tasklist[index]
            if feasible_test(m_tasklist,pre):
                temp_index = get_index_from_array(m_tasklist,inact)
                
                for j in range(1,len(m_modelist)-1):
                    if m_modelist[j] + m_modelist[j+1] == 2:
                        m_modelist[j] = 0

                m_modelist = div_inact(temp_index,m_modelist)
                taskmodelist_end = np.vstack((m_tasklist,m_modelist))
            else:
                taskmodelist_end = taskmodelist
            mutation_pop = np.vstack((mutation_pop,taskmodelist_end))
        mutation_pop = mutation_pop.reshape(self.pop_size*2+1,2,tasknum).astype(int)
        return mutation_pop[1:]

    def ga_evolution(self):
        tasknum = self.get_info()[0]
        pre = self.get_info()[1]
        initpop = self.get_init_pop()
        mother = self.ranking_select(initpop)
        father = self.random_select(initpop)
        result = []
        s_time = time.process_time()
        while(self.MaxGens):
            print(self.MaxGens)
            self.MaxGens -= 1
            son_1 = self.crossover(mother,father)
            son_2 = self.crossover(mother,father)
            
            son_1 = self.mutation(son_1,pre)
            son_2 = self.mutation(son_2,pre)
            
            mother = self.ranking_select(son_1)
            father = self.ranking_select(son_2)

            best_fitnees = min(self.get_fitness(mother)[0], self.get_fitness(father)[0])
            result.append(best_fitnees)
            if len(result) > 100:
                if all(i == result[-100] for i in result[-100:-1]):
                    break
                    
            print(best_fitnees)
              
        final_pop = np.vstack((mother,father)).reshape(self.pop_size*2,2,tasknum)
        final_pop = self.ranking_select(final_pop)
        best_fitness_end = self.get_fitness(final_pop)[0]
        best_inid_end = final_pop[0]
        f_time = time.process_time()
        return best_fitness_end, best_inid_end, f_time-s_time


    