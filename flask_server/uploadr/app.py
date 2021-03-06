
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

configuration_settings = {}
configuration_settings['display'] = {}
configuration_settings['display']['display_output'] = {'hdmi': '', 'none': ''}
configuration_settings['audio'] = {}
configuration_settings['audio']['audio_output'] = {'both': 'checked', 'hdmi': '', 'analog': ''}
configuration_settings['audio']['audio_muting'] = {'mute': '', 'unmute': ''}
configuration_settings['dropbox'] = {'css_width': '0', 'html': ''}
configuration_settings['playlist'] = {'html': ''}

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

    if not app.config['video']['lock'].acquire(True, 2):
       print("Error: could not acquire video object thread lock")
       return
    
    configuration_settings['audio']['audio_output']['hdmi'] = ''
    configuration_settings['audio']['audio_output']['both'] = ''
    configuration_settings['audio']['audio_output']['analog'] = ''

    if(app.config['video']['audio_output'] == 'both'):
        configuration_settings['audio']['audio_output']['both'] = 'checked'
    elif(app.config['video']['audio_output'] == 'hdmi'):
        configuration_settings['audio']['audio_output']['hdmi'] = 'checked'
    elif(app.config['video']['audio_output'] == 'analog'):
        configuration_settings['audio']['audio_output']['analog'] = 'checked'

    app.config['video']['lock'].release()

def get_usb_path_form(number):
    return """<td><form id="upload-form-{}" action="/upload_usb{}" method="POST" enctype="multipart/form-data"><b>/mnt/omedia_usb{}</b><div class="dropbox" id="dropbox{}">Drag and Drop Files Here<p><input id="file-picker-{}" class="file-picker" type="file" accept="H.264/*" multiple><p></div></form></td>""".format(number, number, number ,number, number)
 
def get_file_paths_form(file_path, playlist_item_number):
    return """<tr><td>{}</td><td><a href="/delete_file/{}"><input type="button" class="delete_button" value="delete"></a></td></tr>""".format(file_path, playlist_item_number)
def get_available_usb_paths():
    configuration_settings['dropbox']['html'] = ''
    configuration_settings['dropbox']['css_width'] = 0
    configuration_settings['playlist']['html'] = ''

    css_width_count = 0
    app.config['usb'].lock.acquire()

    if(app.config['usb']._mount_mapping[0][3]):
        configuration_settings['dropbox']['html'] += get_usb_path_form(1)
        css_width_count += 1


    if(app.config['usb']._mount_mapping[1][3]):
        configuration_settings['dropbox']['html'] +=  get_usb_path_form(2)
        css_width_count += 1

    if(app.config['usb']._mount_mapping[2][3]):
        configuration_settings['dropbox']['html'] += "</tr><tr>"
        configuration_settings['dropbox']['html'] +=  get_usb_path_form(3)
        css_width_count += 1

    if(app.config['usb']._mount_mapping[3][3]):
        configuration_settings['dropbox']['html'] +=  get_usb_path_form(4) 
        css_width_count += 1

    index = 0    
    for file in app.config['usb'].playlist:
        configuration_settings['playlist']['html'] += get_file_paths_form(file, index)
        index += 1
    app.config['usb'].lock.release()

    if(css_width_count == 0):
        css_width_count = 1

    configuration_settings['dropbox']['html'] = Markup( configuration_settings['dropbox']['html'])
    configuration_settings['dropbox']['css_width'] = Markup(str(90/css_width_count)+"vw")
    configuration_settings['playlist']['html'] = Markup(configuration_settings['playlist']['html'])

def reboot():
    os.system('sleep 3; reboot')

@app.route("/")
def index() :
    get_configuration_settings()
    get_available_usb_paths()
    return render_template("index.html", configuration=configuration_settings)

@app.route("/upload_usb1", methods=["POST"])
def upload_usb1():
    form = request.form
    upload_handler(form, "/mnt/omedia_usb1")
    return ""

@app.route("/upload_usb2", methods=["POST"])
def upload_usb2():
    form = request.form
    upload_handler(form, "/mnt/omedia_usb2")
    return ""

@app.route("/upload_usb3", methods=["POST"])
def upload_usb3():
    form = request.form
    upload_handler(form, "/mnt/omedia_usb3")
    return ""

@app.route("/upload_usb4", methods=["POST"])
def upload_usb4():
    form = request.form
    upload_handler(form, "/mnt/omedia_usb4")
    return ""

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
        return render_template("index.html", configuration=configuration_settings)

@app.route("/reboot")
def reboot_device():
    restart_thread = threading.Thread(target=reboot, args=())
    restart_thread.start()
    return render_template("reboot.html")

@app.route("/delete_file/<string:id>", methods=["GET", "POST"])
def delete_file(id):
    print("len( playlist): " + str(len(playlist)))
    print("str(int(id)): " + str(int(id)))
    if(len(playlist) > int(id)):
        os.system("rm " +  playlist[int(id)])

    return redirect(url_for("index"))


def get_playlist():
    return playlist

@app.route("/update_configuration", methods=["POST"])
def update_configuration():
    if not app.config['video']['lock'].acquire(True, 2):
       print("Error: could not acquire video object thread lock")
       return render_template("index.html", configuration=configuration_settings)
    if(request.form.get('audio_output', 'error') == 'both'):
        print("audio_output: both")
        print("Changing audio_output to both")
        app.config['video']['audio_output'] = 'both'
        app.config['video']['arguments_change_flag'] = True
    elif(request.form.get('audio_output', 'error') == 'hdmi'):
        print("audio_output: hdmi")
        app.config['video']['audio_output'] = 'hdmi'
        app.config['video']['arguments_change_flag'] = True
    elif(request.form.get('audio_output', 'error') == 'analog'):
        print("audio_output: analog")
        app.config['video']['audio_output'] = 'analog'
        app.config['video']['arguments_change_flag'] = True
    else:
        print("audio_output: error")

    if(request.form.get('audio_output', 'error') == 'mute'):
        print("audio_muting: mute")
    if(request.form.get('audio_output', 'error') == 'unmute'):
        print("audio_muting: unmute")
    else:
        print("audio_muting: error")
    app.config['video']['lock'].release()

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
