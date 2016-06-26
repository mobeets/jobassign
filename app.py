import json
import os.path
import cherrypy

import conf
from spdsht.load import google_load
from solve import solve_bnd

class Root(object):
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        obj = google_load()
        obj, assignVars = solve_bnd(obj)

        out = ''
        for m in obj['MACHINES']:
            out += '<br>' 
            out += "User {0} assigned tasks:<br>".format(obj['Users'][m]['name'])
            for t in obj['TASKS']:
                v = assignVars[m][t].varValue
                if v:
                    out += '({0}, {1})<br>'.format(obj['Queues'][t]['name'], v)
        return out
        # return json.dumps(obj, sort_keys=True,
        #     indent=4, separators=(',', ': '))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def validate(self):
        result = {"operation": "request", "result": "success"}

        content = cherrypy.request.json
        assigns = content["assigns"]

        return result

def main():
    cherrypy.config.update(conf.settings)

    root_app = cherrypy.tree.mount(Root(), '/', conf.root_settings)
    root_app.merge(conf.settings)

    if hasattr(cherrypy.engine, "signal_handler"):
        cherrypy.engine.signal_handler.subscribe()
    if hasattr(cherrypy.engine, "console_control_handler"):
        cherrypy.engine.console_control_handler.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
