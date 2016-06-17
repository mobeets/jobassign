import sys
import json

def txtload(infile):
    """
    First line is # machines (M), # tasks (T)
    Next M lines are T cost values
    Next M lines are T resource_use values
    Last line is capacity of each machine
    """

    # parse data file
    data = open(infile)

    line = data.readline().split()
    NUM_MACHINES = int(line[0])
    NUM_TASKS = int(line[1])
    MACHINES = range(NUM_MACHINES)
    TASKS = range(NUM_TASKS)
    MACHINES_TASKS = [(m, t) for m in MACHINES for t in TASKS]

    COSTS = []
    for m in MACHINES:
        line = data.readline().split()
        assert len(line) == NUM_TASKS
        COSTS.append([int(f) for f in line])

    RESOURCE_USE = []
    for m in MACHINES:
        line = data.readline().split()
        assert len(line) == NUM_TASKS
        RESOURCE_USE.append([int(f) for f in line])

    line = data.readline().split()
    assert len(line) == NUM_MACHINES
    CAPACITIES = [int(f) for f in line]

    return {'NUM_MACHINES': NUM_MACHINES,
        'NUM_TASKS': NUM_TASKS,
        'MACHINES': MACHINES,
        'TASKS': TASKS,
        'MACHINES_TASKS': MACHINES_TASKS,
        'COSTS': COSTS,
        'RESOURCE_USE': RESOURCE_USE,
        'CAPACITIES': CAPACITIES}

def jsonload(infile):
    with open(infile) as f:
        return json.loads(f.read())

def txt2json(infile, outfile):
    obj = txtload(infile)
    jsonobj = json.dumps(obj, sort_keys=True,
        indent=4, separators=(',', ': '))
    with open(outfile, 'w') as f:
        f.write(jsonobj)
    
if __name__ == '__main__':
    print jsonload(sys.argv[1])
