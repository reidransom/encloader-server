import os

CWD = os.path.dirname(__file__)
ENCODE_DIR = os.path.join(CWD, 'uploads')
DB_FILE = os.path.join(CWD, 'db', 'encload.db')
HB = os.path.join(CWD, 'bin', 'HandbrakeCLI')
ENCLOADC = os.path.join(CWD, 'encloadc')

# Before changing or adding your own presets you might find this super useful:
# http://trac.handbrake.fr/wiki/CLIGuide
ENCODING_PRESETS = {
    'web_post_full' : {
        'name': 'Web Post Full (SD)',
        'cmd': HB + ' -i %(input_path)s -o %(output_path)s -e x264 -q 20.0 -a 1 -E faac -B 128 -6 dpl2 -R Auto -D 0.0 -f mp4 --width 480 --height 360 --decomb --crop 0:0:0:0 --optimize -m -x cabac=0:ref=2:me=umh:bframes=0:weightp=0:subme=6:8x8dct=0:trellis=0',
        'extension': '.mp4',
    },
    'web_post_wide': {
        'name': 'Web Post Wide (HD)',
        'cmd': HB + ' -i %(input_path)s -o %(output_path)s -e x264 -q 20.0 -a 1 -E faac -B 128 -6 dpl2 -R Auto -D 0.0 -f mp4 --width 480 --height 270 --decomb --crop 0:0:0:0 --optimize -m -x cabac=0:ref=2:me=umh:bframes=0:weightp=0:subme=6:8x8dct=0:trellis=0',
        'extension': '.mp4',
    },
}

# Add your ftp site here
DESTINATION_PRESETS = {
    'ftp_site': {
        'name': 'Example FTP',
        'host': 'ftp.example.com',
        'user': 'username',
        'passwd': 'password',
        #"port" : 21,
        #"path" : "/",
    },
    'b2': {
        'name': 'B2 User',
        'host': 'b2-studios.com',
        'user': 'b2user@b2-studios.com',
        'passwd': 'w00leyb2',
        #"port" : 21,
        #"path" : "/",
    },
}
