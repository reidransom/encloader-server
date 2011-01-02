from bottle import debug
#debug(True)

import os
from ftplib import FTP
import re
import subprocess

from bottle import route, template, request, static_file, run, PasteServer

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

@route('/')
def index():
    return template('index', encoding_presets=ENCODING_PRESETS,
        destination_presets=DESTINATION_PRESETS,
        e=request.GET.get('e', ''),
        d=request.GET.get('d', ''),
        p=request.GET.get('p', ''),
        v=request.GET.get('v', ''),
        j=None)

@route('/joblook')
def joblook():
    return template('index', encoding_presets=ENCODING_PRESETS,
        destination_presets=DESTINATION_PRESETS,
        e="web_post_full",
        d="b2",
        p="somepath.mp4",
        v="somepath.html",
        j=5)

@route('/job/status/:id')
def job_status(id):
    db = models.DBConnection()
    (s, p) = models.Job.get_status(db, id)
    db.close()
    return {'status': s, 'percent': p}

@route('/job', method='post')
def job():
    
    file_data = request.files.get('file_data')
    
    if not file_data.filename:
        return "Error"
        
    def file_buffer(f, chunk_size=10000):
        while True:
            chunk = f.read(chunk_size)
            if not chunk: break
            yield chunk
    
    db = models.DBConnection()
    job = models.Job(db, request.forms.get('encoding_preset'), 
        request.forms.get('destination_preset'),
        request.forms.get('destination_path'),
        os.path.basename(file_data.filename))

    f = open(job.get_input_path(), 'wb', 10000)
    for chunk in file_buffer(file_data.file):
        f.write(chunk)
    f.close()
    
    job.save()
    
    pid = subprocess.Popen([ENCLOADC, '-j', str(job.id)],
        cwd=CWD).pid
    
    db.close()

    return template('index', encoding_presets=ENCODING_PRESETS,
        destination_presets=DESTINATION_PRESETS,
        e=job.encoding_preset,
        d=job.destination_preset,
        p=job.destination_path,
        v=request.forms.get('view', ''),
        j=job.id)

@route('/static/:path#.+#')
def send_static(path):
    return static_file(path, root=os.path.join(CWD, 'static'))

#run(host='0.0.0.0', port=8000, reloader=True)
run(host='0.0.0.0', port=8000, reloader=True, server=PasteServer)
