#!/usr/bin/env python
"""
This is the simpler, pulp-only solution
    because installing dippy is a pain.
"""

import sys
from pulp import *
from datio import jsonload
from spdsht.load import google_load

def solve_pulp(obj):
    """
    can add dummy machine that adds large cost or something,
        to cover tasks that can't be worked
    """

    COSTS = obj['COSTS']
    MACHINES_TASKS = obj['MACHINES_TASKS']
    MACHINES = obj['MACHINES']
    RESOURCE_USE = obj['RESOURCE_USE']
    TASKS = obj['TASKS']
    CAPACITIES = obj['CAPACITIES']

    assignVars = []
    for m in MACHINES:
        v = []
        for t in TASKS:
            v.append(LpVariable("M%dT%d" % (m, t), cat=LpBinary))
        assignVars.append(v)

    prob = LpProblem("GAP", LpMinimize)

    # objective
    prob += lpSum(assignVars[m][t] * COSTS[m][t] for m, t in MACHINES_TASKS), "min"

    # machine capacity (knapsacks, relaxation)
    for m in MACHINES:
        prob += lpSum(assignVars[m][t] * RESOURCE_USE[m][t] for t in TASKS) <= CAPACITIES[m]

    # assignment
    for t in TASKS:
        prob += lpSum(assignVars[m][t] for m in MACHINES) == 1

    prob.solve()

    for m in MACHINES:
        print 
        print "Machine %d assigned tasks" %m,
        for t in TASKS:
            v = assignVars[m][t].varValue
            if v:
                print "%d" %t,

def solve_bnd(obj, create_dummy=True):
    """
    can add dummy machine that adds large cost or something,
        to cover tasks that can't be worked
    """

    COSTS = obj['COSTS']
    CAPACITIES = obj['CAPACITIES']
    MACHINES_TASKS = obj['MACHINES_TASKS']
    
    TASKS = obj['TASKS']
    MACHINES = obj['MACHINES']
    EFFICIENCIES = obj['EFFICIENCIES'] # 1/UTILIZATION
    MAX_VOL = obj['MAX_VOLUMES']
    MIN_VOL = obj['MIN_VOLUMES']

    # create dummy object to catch extra tasks, at a large cost
    if create_dummy:
        MACHINES.append('Dummy')
        EFFICIENCIES.append([1e-2]*len(EFFICIENCIES[-1]))
        CAPACITIES.append(1e8)
        COSTS.append([10000]*len(COSTS[-1]))
        for t in TASKS:
            MACHINES_TASKS.append(('Dummy', t))

    assignVars = []
    for m in MACHINES:
        v = []
        for t in TASKS:
            # name, lower bound, upper bound, type
            v.append(LpVariable("M{0}T{1}".format(m, t), 0, None, cat=LpContinuous))
        assignVars.append(v)

    prob = LpProblem("GAP", LpMinimize)

    # objective
    prob += lpSum(assignVars[m][t] * COSTS[m][t] for m, t in MACHINES_TASKS), "min"

    # machine capacity (knapsacks, relaxation)
    for m in MACHINES:
        prob += lpSum(assignVars[m][t] * EFFICIENCIES[m][t] for t in TASKS) <= CAPACITIES[m]

    # assignment
    for t in TASKS:
        prob += lpSum(assignVars[m][t] for m in MACHINES) <= MAX_VOL[t]
        prob += lpSum(assignVars[m][t] for m in MACHINES) >= MIN_VOL[t]

    prob.solve()

    for m in MACHINES:
        print 
        print "Machine {0} assigned tasks".format(m),
        for t in TASKS:
            v = assignVars[m][t].varValue
            if v:
                print t

def main(infile):
    objs = jsonload(infile)
    print objs
    solve_pulp(objs)

def main2(infile):
    objs = google_load(infile)
    print objs
    solve_bnd(objs)

if __name__ == '__main__':
    main(sys.argv[1])
