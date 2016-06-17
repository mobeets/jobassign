
Problem: Generalized Assignment Problem

Inputs:
* N bins with capacity C_1, ..., C_N
* K jobs with maximum volumes V_1, ..., V_K, and minimum volumes W_1, ..., W_K
* K job priorities P_1, ..., P_K (s.t. sum_j P_j == 1)

Outputs:
* w_ij is volume of job j assigned to bin i

Objective:
* fulfill as many jobs as possible: maximize sum_ij P_j * w_ij

Constraints:
* don't overfill bins: for each bin i, sum_j w_ij <= C_i
* assign the right number of jobs (not too few, not too many): for each job j, W_j <= sum_i w_ij <= V_j

(Future) Extension: Allow each bin to have different efficiencies at covering a given job.

------

Example: John has 7 hours, Bob has 2 hours, Sue has 5 hours. We need to mop 30 hours and sweep 17 hours. Mopping has priority 0.8 and sweeping has priority 0.2.

Inputs:
* C_1 = 7, C_2 = 2, C_3 = 5
* V_1 = 30, V_2 = 17
* P_1 = 0.8, P_2 = 0.2

Problem: We are always dealing with infeasible solutions; i.e., there will always be more task volumes than bin capacity. Resultingly, the above approach will always fill itself up with high priority items first, when in reality we desire to diverse solutions--i.e., we want to lower queue lengths for lower priority jobs as well.

Solution #1: Have priorities decay with increasing volume--so break up volumes into new units where each bundle has a lower priority. I.e., V_1=10 with P_1=0.9 might be broken up into (V_1a=5, P_1a=0.6), and (V_1b=5, P_1b=0.3) or somehting like that.

Solution #2: Have priorities be relative ratios, so for jobs j,k constrain so that sum_i P_j w_ij <= sum_i P_k w_ik

Solution #3: If optimization runs quickly enough, add sliders to each job type to bound the total number that need to be satisfied. The user could start at the top of the priority queue and lower the volumes until there's a diverse enough set of tasks covered.

Also maybe add in a minimum-value slider for each volume.


Resources:

http://pythonhosted.org/PuLP/CaseStudies/a_blending_problem.html
http://coral.ie.lehigh.edu/~ted/teaching/ie418/
https://projects.coin-or.org/Dip

## Install instructions

https://projects.coin-or.org/Dip

