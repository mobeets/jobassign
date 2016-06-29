from datio import obj2json
from spreadsheet import GoogleSpreadsheet

# KEYFILE = 'notes/keys.json'
KEYFILE = None
def get_spreadsheet(name, keyfile=KEYFILE):
    gs = GoogleSpreadsheet(keyfile)
    return gs.fetchWorksheets(name)

def jsgrid_load(users, jobs):
    """
    # OLD
    Users = [{'mem': 'x', 'p2p': None, 'name': 'Bilbo', 'srt': 'x', 'ncw': '0'}, ...]
    # NEW
    users =  [{u'name': u'Frodo', u'working': u'yes', u'WALK': u'no', u'SLEEP': u'yes', u'SING': u'no', u'RING': u'yes'}, ...]

    # OLD
    Queues = [{'queue': 'MEM', 'minvolume': '100', 'maxvolume': '500', 'maxassign': '30'}, ...]
    # NEW
    jobs = [{u'priority': 1, u'max_assign': 5, u'name': u'RING', u'min_volume': 5, u'max_volume': 20}, ...]
    
    # NEW
    # assigns = [{u'SING': 0, u'RING': 3, u'SLEEP': 9, u'name': u'Frodo', u'WALK': 5}, {u'SING': 0, u'RING': 2, u'SLEEP': 9, u'name': u'Sam', u'WALK': 5}, {u'SING': 3, u'RING': 1, u'SLEEP': 3, u'name': u'Gollum', u'WALK': 2}, {u'SING': 3, u'RING': 0, u'SLEEP': 1, u'name': u'Gandalf', u'WALK': 3}, {u'SING': 3, u'RING': 0, u'SLEEP': 1, u'name': u'Sauron', u'WALK': 3}]
    """
    def job_convert(job):
        for key in job:
            job[key.replace('_', '').lower()] = job.pop(key)
        return job
    def user_convert(user):
        new_user = user.copy()
        for key, val in user.iteritems():
            key = key.lower()
            if val == 'yes':
                new_user[key] = 'x'
            elif val == 'no':
                new_user[key] = None
            else:
                new_user[key] = val
        if 'ncw' not in new_user:
            new_user['ncw'] = 0.0
        return new_user
    users = [user_convert(user) for user in users]
    jobs = [job_convert(job) for job in jobs]
    return generic_load(users, jobs)

def google_load(sheetname='fbjobapp'):
    sheets = get_spreadsheet(sheetname)
    Users = sheets['Users']
    # [{'mem': 'x', 'p2p': None, 'name': 'Bilbo', 'srt': 'x', 'ncw': '0'}, ...]
    Queues = sheets['Queues']
    # [{'queue': 'MEM', 'volume': '1000', 'minimum': '100', 'maximum': '500', 'utilization': '30'}, ...]
    return generic_load(Users, Queues)

def generic_load(Users, Queues):
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

if __name__ == '__main__':
    obj = google_load()
    print obj
    obj2json(obj, 'data/example_spdsht.json')
