from bottle import debug
debug(True)

import os
from ftplib import FTP
import re
import subprocess

try:
    import json # Python 2.6+
except ImportError:
    import simplejson as json

#from bottle import route, template, request, static_file, run, PasteServer
import bottle
bottle.TEMPLATE_PATH.append(os.path.dirname(__file__))

from settings import *
import models

def is_safe(s):
    if re.match("^[\w\.-]+$", s):
        return True
    return False
def get_temp_path(base_name):
    return os.path.join(ENCODE_DIR, base_name)
def get_preset(name, presets):
    try:
        return presets[name]
    except KeyError:
        return "preset not defined"
def get_encoding_preset(name):
    return get_preset(name, ENCODING_PRESETS)
def get_destination_preset(name):
    return get_preset(name, DESTINATION_PRESETS)
def P(s):
    return '<p>' + s + '</p>'

@bottle.route('/')
def index():
    return bottle.template('index', encoding_presets=ENCODING_PRESETS,
        destination_presets=DESTINATION_PRESETS,
        e=bottle.request.GET.get('e', ''),
        d=bottle.request.GET.get('d', ''),
        p=bottle.request.GET.get('p', ''),
        v=bottle.request.GET.get('v', ''),
        j=None)

@bottle.route('/joblook')
def joblook():
    return bottle.template('index', encoding_presets=ENCODING_PRESETS,
        destination_presets=DESTINATION_PRESETS,
        e="web_post_full",
        d="b2",
        p="somepath.mp4",
        v="somepath.html",
        j=5)

@bottle.route('/job/status/:id')
def job_status(id):
    db = models.DBConnection()
    (s, p) = models.Job.get_status(db, id)
    db.close()
    return {'status': s, 'percent': p}

@bottle.route('/job', method='post')
def job():
    
    file_data = bottle.request.files.get('file_data')
    
    if not file_data.filename:
        return "Error"
        
    db = models.DBConnection()
    job = models.Job(db, bottle.request.forms.get('encoding_preset'), 
        bottle.request.forms.get('destination_preset'),
        bottle.request.forms.get('destination_path'),
        os.path.basename(file_data.filename))
    job.save()

    def file_buffer(f, chunk_size=10000):
        while True:
            chunk = f.read(chunk_size)
            if not chunk: break
            yield chunk
    f = open(job.get_input_path(), 'wb', 10000)
    for chunk in file_buffer(file_data.file):
        f.write(chunk)
    f.close()
    
    pid = subprocess.Popen([ENCLOADC, '-j', str(job.id)], cwd=CWD).pid
    
    db.close()

    return bottle.template('index', encoding_presets=ENCODING_PRESETS,
        destination_presets=DESTINATION_PRESETS,
        e=job.encoding_preset,
        d=job.destination_preset,
        p=job.destination_path,
        v=bottle.request.forms.get('view', ''),
        j=job.id)

@bottle.route('/static/:path#.+#')
def send_static(path):
    return bottle.static_file(path, root=os.path.join(CWD, 'static'))

#run(host='0.0.0.0', port=8000, reloader=True)
bottle.run(host='0.0.0.0', port=8000, reloader=True, server=bottle.PasteServer)
