import model.datio
from model.spreadsheet import GoogleSpreadsheet
from model.solve import solve_bnd

# KEYFILE = 'notes/keys.json'
KEYFILE = None
def fetch_spreadsheet(name, keyfile=KEYFILE):
    gs = GoogleSpreadsheet(keyfile)
    return gs.fetchWorksheets(name)

def load_spreadsheet(sheetname='fbjobapp'):
    sheets = fetch_spreadsheet(sheetname)
    Users = sheets['Users']
    # [{'mem': 'x', 'p2p': None, 'name': 'Bilbo', 'srt': 'x', 'ncw': '0'}, ...]
    Queues = sheets['Queues']
    # [{'queue': 'MEM', 'volume': '1000', 'minimum': '100', 'maximum': '500', 'utilization': '30'}, ...]
    return model.datio.loadobj(Users, Queues)

def print_results(obj):
    out = ''
    for m in obj['MACHINES']:
        out += '<br>' 
        out += "User {0} assigned tasks:<br>".format(obj['Users'][m]['name'])
        for t in obj['TASKS']:
            v = assignVars[m][t]
            if v:
                out += '({0}, {1})<br>'.format(obj['Queues'][t]['name'], v)
    return out

def google_solve():
    obj = load_spreadsheet()
    obj, assignVars = solve_bnd(obj)
    return print_results(obj)

if __name__ == '__main__':
    obj = load_spreadsheet()
    print obj
    model.datio.obj2json(obj, 'data/example_spdsht.json')
