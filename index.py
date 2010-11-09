import os

from bottle import route, template, request, debug, static_file, run
debug(True)

CWD = os.path.dirname(__file__)

@route('/hello')
def hello():
    return "Hello World!"

@route('/')
def index():
    return template('upload')

@route('/upload', method='post')
def upload():
    data = request.files.get('data')
    message = ""
    if data.filename:
        def file_buffer(f, chunk_size=10000):
            while True:
                chunk = f.read(chunk_size)
                if not chunk: break
                yield chunk
        filename = os.path.basename(data.filename)
        f = open('/tmp/%s' % filename, 'wb', 10000)
        for chunk in file_buffer(data.file):
            f.write(chunk)
        f.close()
        message = "The file (%s) was uploaded successfully" % filename
    else:
        message = "No file was uploaded"
    return template('<p><a href="">index</a></p><p>{{message}}</p>', message=message)

@route('/static/:filename')
def send_static(filename):
    return static_file(filename, root=os.path.join(CWD, 'static'))

run(host='0.0.0.0', port=8080, reloader=True)
