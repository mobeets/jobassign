import model.datio
from model.solve import solve_bnd

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
    return model.datio.loadobj(users, jobs)

def assign_convert(obj, assignVars):
    """
    assigns = [{u'SING': 0, u'RING': 3, u'SLEEP': 9, u'name': u'Frodo', u'WALK': 5}, ...]
    """
    users = [item['name'] for item in obj['Users']]
    jobs = [item['name'] for item in obj['Queues']]
    assigns = []
    simple_assigns = []
    for i, row in enumerate(assignVars):
        assign = {}
        assign['name'] = users[i]
        for j, val in enumerate(row):
            assign[jobs[j]] = val
        assigns.append(assign)
        simple_assigns.append([users[i]] + row)
    return assigns, simple_assigns

def jsgrid_solve(content):
    is_success = True
    obj = jsgrid_load(content["users"], content["jobs"])
    obj, assignVars = solve_bnd(obj)

    full_assigns, assigns = assign_convert(obj, assignVars)
    comments = []
    return is_success, assigns, full_assigns, comments

def jsgrid_validate(content):
    is_valid = True
    comments = []
    return is_valid, comments
