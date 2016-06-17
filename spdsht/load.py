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

    MACHINES = [user['name'] for (i, user) in enumerate(Users)]
    TASKS = [task['name'] for (i, task) in enumerate(Queues)]
    MACHINES_TASKS = [(m, t) for m in MACHINES for t in TASKS]
    NUM_MACHINES = len(MACHINES)
    NUM_TASKS = len(TASKS)

    CAPACITIES = [8-float(user['ncw']) for user in Users]

    # n.b. only one task can be assigned per user
    COSTS = [[1 for task in Queues] for user in Users]
    EFFICIENCIES = [[1./float(task['utilization']) if user[task['name'].lower()] == 'x' else 0 for task in Queues] for user in Users]
    MIN_VOL = [float(task['minimum']) if user[task['name'].lower()] == 'x' else 0 for task in Queues]
    MAX_VOL = [float(task['maximum']) if user[task['name'].lower()] == 'x' else 0 for task in Queues]

    # # min and max amounts per task
    # amts = []
    # for task in Queues:
    #     vol = float(task['volume'])
    #     mn = float(task['minimum'])
    #     mx = float(task['maximum'])
    #     utl = float(task['utilization'])
    #     min_amt = mn/utl
    #     max_amt = mx/utl
    #     amts.append((min_amt, max_amt))

    return {'NUM_MACHINES': NUM_MACHINES,
        'NUM_TASKS': NUM_TASKS,
        'MACHINES': MACHINES,
        'TASKS': TASKS,
        'MACHINES_TASKS': MACHINES_TASKS,
        'COSTS': COSTS,
        'EFFICIENCIES': EFFICIENCIES,
        'MIN_VOLUMES': MIN_VOL,
        'MAX_VOLUMES': MAX_VOL,
        'CAPACITIES': CAPACITIES}

if __name__ == '__main__':
    print google_load()
