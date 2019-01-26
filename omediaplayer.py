import usb_mounter
import networking
import video_loop
import time
import threading
import subprocess
#from flask import Flask

from flask_server.uploadr.app import app

def main():
    print("starting")
    usb = usb_mounter.usb_mounter()
    usb_mounting_thread = threading.Thread(target=mount_loop, args=(usb, 0.5))
    print("starting usb mounting thread.")
    usb_mounting_thread.start()

    print("starting splash screen thread.")
    network = networking.networking()
#    splash_screen_thread = threading.Thread(target=splash_screen_renderer, args=(network, 1))
#    splash_screen_thread.start()

    print("starting video looping thread")
    video = video_loop.video_loop(usb)
    video_loop_thread = threading.Thread(target=video_looper_loop, args=(video,))
    video_loop_thread.start()

#    app = Flask(__name__)
    app.config['usb'] = usb
    app.config['network'] = network 
    app.config['video'] = video
    flask_options = dict(
        host='0.0.0.0',
        debug=True,
        port=8000,
        threaded=True,
    )
    print("Starting web server...")
    app.run(**flask_options)



    usb_mounting_thread.join()
    splash_screen_thread.join()
    video_loop_thread.join()

    print("finished")

def splash_screen_renderer(network, poll_period):
    p1 = subprocess.Popen(['setterm', '-cursor', 'off'], )
    p1.wait()
    p1 = subprocess.Popen('clear')
    p1.wait()

    for count in range(0, 15):
        p1 = subprocess.Popen('echo')    
        p1.wait()
    while(True): 
        network.get_all_ip_addresses()
        p1 = subprocess.Popen(['tput', 'sc'])
        p1.wait()
        p1 = subprocess.Popen(['figlet', 'OMEDIAPLAYER', '-ctf', 'banner'])
        p1.wait()
        p1 = subprocess.Popen(['figlet', 'eth0: ' + str(network.eth0_ip_address), '-ctf', 'term'])
        p1.wait()
        p1 = subprocess.Popen(['figlet', 'wlan0: ' + str(network.wlan0_ip_address), '-ctf', 'term'])
        p1.wait()
        p1 = subprocess.Popen(['figlet', 'Please upload/insert H.264 media content...', '-ctf', 'term'])
        p1.wait()
        p1 = subprocess.Popen(['tput', 'rc'])
        p1.wait()
        time.sleep(poll_period)

def mount_loop(usb, poll_period):
    while True:
        usb.usb_mount()
        time.sleep(poll_period)

def video_looper_loop(video):
    while True:
        video.play_playlist()
        time.sleep(0.1)

if __name__ == '__main__':
    main()
