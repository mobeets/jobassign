from datio import obj2json
from spreadsheet import GoogleSpreadsheet

KEYFILE = 'notes/keys.json'
def get_spreadsheet(name, keyfile=KEYFILE):
    gs = GoogleSpreadsheet(keyfile)
    return gs.fetchWorksheets(name)

def google_load(sheetname='fbjobapp'):
    sheets = get_spreadsheet(sheetname)
    Users = sheets['Users']
    # [{'mem': 'x', 'p2p': None, 'name': 'Bilbo', 'srt': 'x', 'ncw': '0'}, ...]
    Queues = sheets['Queues']
    # [{'queue': 'MEM', 'volume': '1000', 'minimum': '100', 'maximum': '500', 'utilization': '30'}, ...]

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
    BENEFITS = [[1 for task in Queues] for user in Users]
    EFFICIENCIES = [[1./float(task['utilization']) if user[task['name'].lower()] == 'x' else 0 for task in Queues] for user in Users]
    MIN_VOL = [float(task['minimum']) for task in Queues]
    MAX_VOL = [float(task['maximum']) for task in Queues]

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
        'CAPACITIES': CAPACITIES}

if __name__ == '__main__':
    obj = google_load()
    print obj
    obj2json(obj, 'data/example_spdsht.json')
