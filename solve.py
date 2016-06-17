#!/usr/bin/env python
"""
This is the simpler, pulp-only solution
    because installing dippy is a pain.
"""

import sys
from pulp import *
from datio import jsonload

def solve_pulp(obj):
    """
    all the vars you need are in obj, but I haven't loaded them here yet
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

def main(infile):
    objs = jsonload(infile)
    print objs
    solve_pulp(objs)

if __name__ == '__main__':
    main(sys.argv[1])
