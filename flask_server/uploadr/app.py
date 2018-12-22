from flask import Flask, request, redirect, url_for, render_template
import os
import json
import glob
import re
from uuid import uuid4
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE

app = Flask(__name__)
UPLOAD_FOLDER="uploadr/static/uploads/"

configuration_settings = {}
configuration_settings['display'] = {}
configuration_settings['display']['display_output'] = {'hdmi': '', 'none': ''}
configuration_settings['audio'] = {}
configuration_settings['audio']['audio_output'] = {'both': 'checked', 'hdmi': '', 'analog': ''}
configuration_settings['audio']['audio_muting'] = {'mute': '', 'unmute': ''}
configuration_settings['player'] = {'time_server_address': 'pool.ntp.org'}

def get_display_status():
    p = Popen(['vcgencmd', 'display_power'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    if(int(str(output)[16])):
        return True
    else:
        return False

def get_configuration_settings():
    if(get_display_status()):
        print("Display active")
        configuration_settings['display']['display_output']['hdmi'] = 'checked'
        configuration_settings['display']['display_output']['none'] = ''	
    else:
        print("Display not active")
        configuration_settings['display']['display_output']['hdmi'] = ''
        configuration_settings['display']['display_output']['none'] = 'checked'	

@app.route("/")
def index() :
    get_configuration_settings()
    return render_template("index.html", configuration=configuration_settings)


@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([UPLOAD_FOLDER, filename])
        secure_filename(destination)
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return redirect(url_for("upload_complete", uuid=upload_key))


@app.route("/files/<uuid>")
def upload_complete(uuid):
    # Get their files.
    root = "uploadr/static/uploads/{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template("index.html",
        uuid=uuid,
        files=files,
    )


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))
