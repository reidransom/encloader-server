import os

import bottle
bottle.debug(True)

CWD = os.path.dirname(__file__)

@bottle.route('/hello')
def hello():
	return "Hello World!"

@bottle.route('/static/:filename')
def send_static(filename):
	return bottle.static_file(filename, root=os.path.join(CWD, 'static'))

bottle.run(host='0.0.0.0', port=8080, reloader=True)
