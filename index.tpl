<html>
<head>
    <title>Encloader</title>
    <link rel="stylesheet" type="text/css"
        href="/static/themes/default/style.css" />
    <script type="text/javascript" src="/static/jquery.js"></script>
    <script type="text/javascript" src="/static/jquery.timers.js"></script>
</head>
<body>

<div id="main"><h1>Encloader</h1>
<form action="/job" method="post" enctype="multipart/form-data">
    <label {{'class="readonly"' if e in encoding_presets.keys() else ''}}>
        <span class="name">Encoding preset:</span><br />
%if e in encoding_presets.keys():
        <input id="encoding_preset" name="encoding_preset" value="{{e}}"
            type="hidden" />{{encoding_presets[e]['name']}}
%else:
        <select id="encoding_preset" name="encoding_preset">
%for k in encoding_presets.iterkeys():
            <option value="{{k}}">{{encoding_presets[k]['name']}}</option>
%end
        </select>
%end
    </label>
    <label {{'class="readonly"' if d in destination_presets.keys() else ''}}>
        <span class="name">Destination preset:</span><br />
%if d in destination_presets.keys():
        <input id="destination_preset" name="destination_preset" value="{{d}}"
            type="hidden" />{{destination_presets[d]['name']}}
%else:
        <select id="destination_preset" name="destination_preset">
%for k in destination_presets.iterkeys():
            <option value="{{k}}">{{destination_presets[k]['name']}}</option>
%end
        </select>
%end
    </label>
    <label {{'class="readonly"' if p else ''}}>
        <span class="name">Destination path:</span><br />
        <input id="destination_path" name="destination_path" \\
%if p != "":
value="{{p}}" type="hidden" />{{p}}
%else:
type="text" />
%end
    </label>
    <label {{'class="readonly"' if v else ''}}>
        <span class="name">View:</span>
        <span class="info">(optional)</span><br />
        <input id="view" name="view" \\
%if v != "":
value="{{v}}" type="hidden" /><a href="{{v}}">{{v}}</a>
%else:
type="text" />
%end
    </label>
%if not j:
    <label><span class="name">Video:</span><br />
        <input id="file_data" name="file_data" type="file" />
    </label>
    <input value="Encload!" type="submit" /></p>
%else:
    <div class="module">
        <span id="progress">Pending...</span>
    </div>
    <script type="text/javascript">
        $('#progress').everyTime('3s', function() {
            $.getJSON('/job/status/{{j}}', function(data) {
                var s = data.status;
                if (s == 'complete') {
                    s = s + '.';
                    $('#progress').stopTime();
                    $('#progress').addClass('complete');
                }
                else {
                    s = s + '...';
                }
                s = s.charAt(0).toUpperCase() + s.slice(1);
                $('#progress').html(s);
            });
        });
    </script>
%end
</form>
</div>

</body>
</html>
