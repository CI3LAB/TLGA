# TLGA
Data and codes for "Two-list genetic algorithm for optimizing work package schemes to minimize project costs"

Optimizing work package schemes is challenging under uncertain task duration. This paper develops a two-list genetic algorithm (TLGA) to optimize work package schemes with minimal project costs under deterministic and stochastic task durations. First, this paper defines the deterministic and stochastic work package scheme problem. Second, the TLGA, comprising a task and a work packaging list, is developed to generate the deterministic work package scheme and issue work package policies through stochastic distribution simulations. 

# The description of all files
1. whole_project_for_computewp.rcp: Case project data.
2. ga_main.py: The main function for TLGA
3. dwp_det_inact.py: The necessary functions for TLGA, including Loading data, Feasibility test, Initial population generation, and Identify inactive tasks.
4. com_fitness.py: Fitness (cost) calculation
5. com_tasknum.py：Calculate the number of tasks for decoding.

# Preparations
1. Python
2. Python libraries: numpy, copy, time, os.

# Other notes
1. For detailed principles and explanations of TLGA, please refer to “Zhang, Y., Li, X., Teng, Y., Bai, S., & Chen, Z. (2024). Two-list genetic algorithm for optimizing work package schemes to minimize project costs. Automation in Construction, 165, 105595.”
2. To reference and use this code, please cite “Zhang, Y., Li, X., Teng, Y., Bai, S., & Chen, Z. (2024). Two-list genetic algorithm for optimizing work package schemes to minimize project costs. Automation in Construction, 165, 105595.”
3. For reference and use of the initial model for the work package sizing problem, please cite “Li, C. L., & Hall, N. G. (2019). Work package sizing and project performance. Operations Research, 67(1), 123-142.”.
4. If you have any other questions about data and codes, please email “ya-ning.zhang@connect.polyu.hk”.
