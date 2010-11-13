PRESETS = {
    "web_post_full" : {
        "name" : "SD Web Post",
        "cmd" : "/usr/bin/HandBrakeCLI -e x264 -q 0.589999973773956 -a 1,1 -E faac,ac3 -B 128,auto -R 48,Auto -6 dpl2,auto --decomb -x level=30:cabac=0:ref=3:mixed-refs=1:analyse=all:me=umh:no-fast-pskip -O -f mp4 -w 640 -l 480 -i %(input_path)s -o %(output_path)s",
        "host" : "localhost",
        "user" : "test",
        "passwd" : "test",
        #"port" : 21,
        #"path" : "/",
    },
    "web_post_wide" : {
        "name" : "SD Web Post",
        "cmd" : "/usr/bin/HandBrakeCLI -e x264 -q 0.589999973773956 -a 1,1 -E faac,ac3 -B 128,auto -R 48,Auto -6 dpl2,auto --decomb -x level=30:cabac=0:ref=3:mixed-refs=1:analyse=all:me=umh:no-fast-pskip -O -f mp4 -w 768 -l 432 -i %(input_path)s -o %(output_path)s",
        "host" : "localhost",
        "user" : "test",
        "passwd" : "test",
    },
}
