import sys
import json

def loadobj(Users, Queues):
    MACHINES = [i for (i, user) in enumerate(Users)]
    TASKS = [i for (i, task) in enumerate(Queues)]

    find_user = lambda name: next([x for x in Users if x['name'] == x])
    find_task = lambda name: next([x for x in Queues if x['name'] == x])

    # only add valid machine/task pairs
    MACHINES_TASKS = [(m, t) for m in MACHINES for t in TASKS]
    INVALID_PAIRS = [(m, t) for m in MACHINES for t in TASKS if Users[m][Queues[t]['name'].lower()] != 'x']
    NUM_MACHINES = len(MACHINES)
    NUM_TASKS = len(TASKS)

    CAPACITIES = [8-float(user['ncw']) for user in Users]

    # n.b. only one task can be assigned per user
    RANK = [float(task['priority']) for task in Queues]
    BENEFITS = [max(RANK)-x+1 for x in RANK] # reverse

    EFFICIENCIES = [[1./float(task['utilization']) if user[task['name'].lower()] == 'x' else 0 for task in Queues] for user in Users]
    MIN_VOL = [float(task['minvolume']) for task in Queues]
    MAX_VOL = [float(task['maxvolume']) for task in Queues]

    MAX_PER_MACHINE = [float(task['maxassign']) for task in Queues]

    return {'NUM_MACHINES': NUM_MACHINES,
        'NUM_TASKS': NUM_TASKS,
        'MACHINES': MACHINES,
        'TASKS': TASKS,
        'MACHINES_TASKS': MACHINES_TASKS,
        'INVALID_PAIRS': INVALID_PAIRS,
        'BENEFITS': BENEFITS,
        'EFFICIENCIES': EFFICIENCIES,
        'MIN_VOLUMES': MIN_VOL,
        'MAX_VOLUMES': MAX_VOL,
        'MAX_PER_MACHINE': MAX_PER_MACHINE,
        'CAPACITIES': CAPACITIES,
        'Users': Users,
        'Queues': Queues}

def jsonload(infile):
    with open(infile) as f:
        return json.loads(f.read())

def obj2json(obj, outfile):
    jsonobj = json.dumps(obj, sort_keys=True,
        indent=4, separators=(',', ': '))
    with open(outfile, 'w') as f:
        f.write(jsonobj)

if __name__ == '__main__':
    print jsonload(sys.argv[1])
