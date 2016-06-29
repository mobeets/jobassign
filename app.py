import json
import os.path
import cherrypy

import conf
from model.gglio import google_solve
from model.appio import jsgrid_solve, jsgrid_validate

class Root(object):
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        with open('static/demo.html') as f:
            return f.read()

    @cherrypy.expose
    def google_test(self):
        return google_solve()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def validate(self):
        result = {"operation": "request", "result": "success"}
        content = cherrypy.request.json
        result["is_valid"], result["comments"] = jsgrid_validate(content)
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def optimize(self):
        result = {"operation": "request", "result": "success"}
        content = cherrypy.request.json
        result["is_success"], result["assigns"], result["comments"] = \
            jsgrid_solve(content)
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
