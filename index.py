from bottle import debug
debug(True)

import os
from ftplib import FTP
import re

from bottle import route, template, request, static_file, run

import settings

CWD = os.path.dirname(__file__)
ENCDIR = "/tmp/"

def is_safe(s):
    if re.match("^[\w\.-]+$", s):
        return True
    return False

def get_temp_path(base_name):
    return os.path.join('/tmp', base_name)

def get_preset(preset_name):
    try:
        return settings.PRESETS[preset_name]
    except KeyError:
        return "preset not defined"
    
def P(s):
    return '<p>' + s + '</p>'

@route('/')
def index():
    return template('upload')

@route('/ftp/:input_basename/:preset_name')
def ftp(input_basename, preset_name):
    
    # configure paths
    input_path = get_temp_path(input_basename)
    output_basename = input_basename
    
    # test if file exists
    if not os.path.isfile(input_path):
        return "file not found"

    # open the file
    input_fileobj = open(input_path, "rb")
    
    # get settings
    preset = get_preset(preset_name)
    
    # connect to the ftp server
    ftp = FTP(preset["host"], preset["user"], preset["passwd"])
    ftp.storbinary("STOR %s" % output_basename, input_fileobj)
    ftp.close()
    
    # close the file
    input_fileobj.close()
    
    # clean up - remove the original file
    os.remove(input_path)
    
    return "it may have worked"

@route('/encode/:input_basename/:preset_name')
def encode(input_basename, preset_name):
    
    # test for unsafe input
    if not is_safe(input_basename):
        #raise HTTPError(output="unsafe characters")
        return "unsafe characters"
    
    # configure paths
    input_path = get_temp_path(input_basename)
    output_basename = input_basename + '.mp4'
    output_path = get_temp_path(output_basename)

    # test if file exists
    if not os.path.isfile(input_path):
        return "file not found"

    # get settings
    preset = get_preset(preset_name)
    
    # form the encode command
    cmd = preset["cmd"] % locals()
    
    # encode the video
    os.system(cmd)

    # clean up - remove the original file
    os.remove(input_path)
    
    # return success
    return P("%s was encoded with %s preset as %s" % \
        (input_basename, preset_name, output_basename)) + \
        P('<a href="/ftp/%s/%s">Upload</a>' % (output_basename, preset_name))

@route('/upload', method='post')
def upload():
    
    data = request.files.get('data')
    preset = "web_post_full"
    message = ""
    
    if data.filename:
        def file_buffer(f, chunk_size=10000):
            while True:
                chunk = f.read(chunk_size)
                if not chunk: break
                yield chunk
        uploadfn = os.path.basename(data.filename)
        f = open('/tmp/%s' % uploadfn, 'wb', 10000)
        for chunk in file_buffer(data.file):
            f.write(chunk)
        f.close()
        message = '<p>The file (%(uploadfn)s) was uploaded successfully' + \
            '</p><p><a href="/encode/%(uploadfn)s/%(preset)s">encode' + \
            '</a></p>'
        message = message % locals()
    
    else:
        message = "No file was uploaded"
    
    return template('<p><a href="">index</a></p>{{!message}}', message=message)

@route('/static/:filename')
def send_static(filename):
    return static_file(filename, root=os.path.join(CWD, 'static'))

run(host='0.0.0.0', port=8080, reloader=True)
