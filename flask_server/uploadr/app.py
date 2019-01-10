from flask import Flask, request, redirect, url_for, render_template, Markup
import os
import json
import glob
import re
import time
import os
import threading
from uuid import uuid4
from werkzeug.utils import secure_filename
from subprocess import Popen, PIPE
import subprocess 
from time import sleep

app = Flask(__name__)
#UPLOAD_FOLDER="uploadr/static/uploads/"

configuration_settings = {}
configuration_settings['display'] = {}
configuration_settings['display']['display_output'] = {'hdmi': '', 'none': ''}
configuration_settings['audio'] = {}
configuration_settings['audio']['audio_output'] = {'both': 'checked', 'hdmi': '', 'analog': ''}
configuration_settings['audio']['audio_muting'] = {'mute': '', 'unmute': ''}
configuration_settings['player'] = {'time_server_address': 'pool.ntp.org'}
configuration_settings['dropbox'] = {'css_width': '0', 'html': ''}

usb_paths = []

def get_display_status():
    p = Popen(['vcgencmd', 'display_power'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    p.wait()
    output = str(p.communicate()[0])
    if(output.find('1') > -1):
        print(output)
        print(str(output.find('1')))
        print("output deemed on")
        return True
    else:
        print(output)
        print("output deemed off")
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
def get_form(number):
    return """<td><form id="upload-form-{}" action="/upload_usb{}" method="POST" enctype="multipart/form-data"><b>/mnt/omedia_usb{}</b><div class="dropbox" id="dropbox{}">Drag and Drop Files Here<p><input id="file-picker-{}" class="file-picker" type="file" accept="H.264/*" multiple><p></div></form></td>""".format(number, number, number ,number, number)
 

def get_available_usb_paths():
    usb_paths.clear()
    configuration_settings['dropbox']['html'] = ''
    configuration_settings['dropbox']['css_width'] = 0
    css_width_count = 0
    p1 = subprocess.Popen("mount", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    p1.wait()
    output = str(p1.communicate()[0])
    if(output.find("/dev/sda1") > -1):
        usb_paths.append("/mnt/omedia_usb1")
        configuration_settings['dropbox']['html'] += get_form(1)
        css_width_count += 1

    if(output.find("/dev/sdb1") > -1):
        usb_paths.append("/mnt/omedia_usb2")
        configuration_settings['dropbox']['html'] += get_form(2)
        css_width_count += 1

    if(output.find("/dev/sdc1") > -1):
        usb_paths.append("/mnt/omedia_usb3")
        configuration_settings['dropbox']['html'] += "</tr><tr>"
        configuration_settings['dropbox']['html'] += get_form(3)
        css_width_count += 1

    if(output.find("/dev/sdd1") > -1):
        usb_paths.append("/mnt/omedia_usb4")
        configuration_settings['dropbox']['html'] += get_form(4) 
        css_width_count += 1
    
    configuration_settings['dropbox']['html'] = Markup( configuration_settings['dropbox']['html'])
    configuration_settings['dropbox']['css_width'] = Markup(str(90/css_width_count)+"vw")

def reboot():
    os.system('sleep 3; reboot')

@app.route("/")
def index() :
    get_configuration_settings()
    get_available_usb_paths()
    return render_template("index.html", configuration=configuration_settings, usb=usb_paths)

@app.route("/upload_usb1", methods=["POST"])
def upload_usb1():
    form = request.form
    upload_handler(form, "/mnt/omedia_usb1")
    return render_template("index.html", configuration=configuration_settings, usb=usb_paths)

@app.route("/upload_usb2", methods=["POST"])
def upload_usb2():
    form = request.form
    upload_handler(form, "/mnt/omedia_usb2")
    return render_template("index.html", configuration=configuration_settings, usb=usb_paths)

@app.route("/upload_usb3", methods=["POST"])
def upload_usb3():
    form = request.form
    upload_handler(form, "/mnt/omedia_usb3")
    return render_template("index.html", configuration=configuration_settings, usb=usb_paths)

@app.route("/upload_usb4", methods=["POST"])
def upload_usb4():
    form = request.form
    upload_handler(form, "/mnt/omedia_usb4")
    return render_template("index.html", configuration=configuration_settings, usb=usb_paths)

def upload_handler(form, upload_path):
    # Is the upload using Ajax, or a direct POST by the form?
    upload_key = str(uuid4())
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([upload_path, filename])
        secure_filename(destination)
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    if is_ajax:
        return ajax_response(True, upload_key)
    else:
#        return redirect(url_for("upload_complete", uuid=upload_key))
        return render_template("index.html", configuration=configuration_settings)

#@app.route("/upload", methods=["POST"])
#def upload():
#    """Handle the upload of a file."""
#    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
#    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
#    is_ajax = False
#    if form.get("__ajax", None) == "true":
#        is_ajax = True

#    print("=== Form Data ===")
#    for key, value in list(form.items()):
#        print(key, "=>", value)

#    for upload in request.files.getlist("file"):
#        filename = upload.filename.rsplit("/")[0]
#        destination = "/".join([UPLOAD_FOLDER, filename])
#        secure_filename(destination)
#        print("Accept incoming file:", filename)
#        print("Save it to:", destination)
#        upload.save(destination)

#    if is_ajax:
#        return ajax_response(True, upload_key)
#    else:
#        return redirect(url_for("upload_complete", uuid=upload_key))
#        return render_template("index.html", configuration=configuration_settings)


#@app.route("/files/<uuid>")
#def upload_complete(uuid):
    # Get their files.
#    root = "uploadr/static/uploads/{}".format(uuid)
#    if not os.path.isdir(root):
#        return "Error: UUID not found!"

#    files = []
#    for file in glob.glob("{}/*.*".format(root)):
#        fname = file.split(os.sep)[-1]
#        files.append(fname)

#    return render_template("index.html",
#        uuid=uuid,
#        files=files,
#    )

@app.route("/reboot")
def reboot_device():
    restart_thread = threading.Thread(target=reboot, args=())
    restart_thread.start()
    return render_template("reboot.html")

@app.route("/update_configuration", methods=["POST"])
def update_configuration():
    if(request.form.get('audio_output', 'error') == 'both'):
        print("audio_output: both")
    elif(request.form.get('audio_output', 'error') == 'hdmi'):
        print("audio_output: hdmi")
    elif(request.form.get('audio_output', 'error') == 'analog'):
        print("audio_output: analog")
    else:
        print("audio_output: error")

    if(request.form.get('audio_output', 'error') == 'mute'):
        print("audio_muting: mute")
    if(request.form.get('audio_output', 'error') == 'unmute'):
        print("audio_muting: unmute")
    else:
        print("audio_muting: error")

    if(request.form.get('display_output', 'error') == 'hdmi'):
        print("display_output: hdmi")
        p = subprocess.Popen(["vcgencmd", "display_power 1"])
        p.wait()
    
    elif(request.form.get('display_output', 'error') == 'none'):
        print("display_output: none")
        p = subprocess.Popen(["vcgencmd", "display_power 0"])
        p.wait()
    else:
        print("display_output: error")

    get_configuration_settings()
    return render_template("index.html", configuration=configuration_settings)

def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))
