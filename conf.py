import os
CURDIR = os.path.dirname(os.path.abspath(__file__))
ROOTDIR = os.path.abspath(os.path.join(CURDIR, '..'))

settings = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', '5000')),
        'server.environment': 'development',
    },
}

root_settings = {
    '/': {
        'tools.staticdir.root': ROOTDIR,
    }
}
