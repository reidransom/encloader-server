import os

CWD = os.path.dirname(__file__)
ENCODE_DIR = os.path.join(CWD, 'tmp')
DB_FILE = os.path.join(CWD, 'db', 'encload.db')
HB = os.path.join(CWD, 'handbrake', 'HandbrakeCLI')
ENCLOADC = os.path.join(CWD, 'encloadc')

# Before changing or adding your own presets you might find this super useful:
# http://trac.handbrake.fr/wiki/CLIGuide
ENCODING_PRESETS = {
    'web_post_full' : {
        'name': 'Web Post Full (SD)',
        'cmd': HB + ' --encoder x264 -vb 800 --two-pass --turbo --crop 0:0:0:0 --color-matrix 601 --audio 1,1 --aencoder faac,ac3 --ab 128,auto --arate 48,auto --mixdown stereo,auto --decomb --x264opts level=30:cabac=0:ref=3:mixed-refs=1:analyse=all:me=umh:no-fast-pskip --optimize --format mp4 --width 640 --height 480 --input %(input_path)s --output %(output_path)s',
        'extension': '.mp4',
    },
    'web_post_wide': {
        'name': 'Web Post Wide (HD)',
        'cmd': HB + ' --encoder x264 -vb 800 --two-pass --turbo --crop 0:0:0:0 --color-matrix 601 --audio 1,1 --aencoder faac,ac3 --ab 128,auto --arate 48,auto --mixdown stereo,auto --decomb --x264opts level=30:cabac=0:ref=3:mixed-refs=1:analyse=all:me=umh:no-fast-pskip --optimize --format mp4 --width 768 --height 432 --input %(input_path)s --output %(output_path)s',
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
}
