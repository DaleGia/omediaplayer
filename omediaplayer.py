import usb_mounter
import networking
import time
import threading
import subprocess
#from flask import Flask

from flask_server.uploadr.app import app

def main():
    print("starting")
    usb = usb_mounter.usb_mounter()
    network = networking.networking()
    usb_mounting_thread = threading.Thread(target=mount_loop, args=(usb, 0.5))
#    splash_screen_thread = threading.Thread(target=splash_screen_renderer, args=(network, 1))
    

    print("Starting usb mounter...")
    usb_mounting_thread.start()
#    splash_screen_thread.start()

#    app = Flask(__name__)
    app.config['usb'] = usb
    app.config['network'] = network 
    flask_options = dict(
        host='0.0.0.0',
        debug=True,
        port=8000,
        threaded=True,
    )
    print("Starting web server...")
    app.run(**flask_options)



#    splash_screen_thread.join()
    usb_mounting_thread.join()

#    flask_server = subprocess.Popen(["python3", "flask_server/runserver.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)   
#    web_server_thread = threading.Thread(target=app.run, kwargs=(flask_options))
#    web_server_thread.start()   

    print("finished")

def splash_screen_renderer(network, poll_period):
    p1 = subprocess.Popen(['setterm', '-cursor', 'off'], )
    p1.wait()
    p1 = subprocess.Popen('clear')
    p1.wait()

    for count in range(0, 15):
        p1 = subprocess.Popen('echo')    
        p1.wait()
    network.get_all_ip_addresses()
    p1 = subprocess.Popen(['figlet', 'OMEDIAPLAYER', '-ctf', 'banner'])
    p1.wait()
    p1 = subprocess.Popen(['figlet', 'eth0: ' + str(network.eth0_ip_address), '-ctf', 'term'])
    p1.wait()
    p1 = subprocess.Popen(['figlet', 'wlan0: ' + str(network.wlan0_ip_address), '-ctf', 'term'])
    p1.wait()
    p1 = subprocess.Popen(['figlet', 'Please upload/insert H.264 media content...', '-ctf', 'term'])

def mount_loop(usb, poll_period):
    while True:
        usb.usb_mount()
        time.sleep(poll_period)

if __name__ == '__main__':
    main()
