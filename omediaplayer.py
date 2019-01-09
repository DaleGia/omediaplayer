import usb_mounter
import networking
import time
import threading
import subprocess

def main():
    print("starting")
#    usb = usb_mounter.usb_mounter()
    network = networking.networking()
#    usb_mounting_thread = threading.Thread(target=mount_loop, args=(usb, 0.5))
    splash_screen_thread = threading.Thread(target=splash_screen_renderer, args=(network, 1))
#    usb_mounting_thread.start()
    splash_screen_thread.start()
    splash_screen_thread.join()
#    usb_mounting_thread.join() 

    print("finished")
def splash_screen_renderer(network, poll_period):
    p1 = subprocess.Popen(['setterm', '-cursor', 'off'])
    p1.wait()
    p1 = subprocess.Popen('clear')
    p1.wait()

    for count in range(0, 15):
        p1 = subprocess.Popen('echo')    
        p1.wait()

    p1 = subprocess.Popen(['figlet', 'OMEDIAPLAYER', '-ctf', 'banner'])
    p1.wait()

    while True:
        network.get_all_ip_addresses()
        render_splash_screen(network.eth0_ip_address, network.wlan0_ip_address)
        time.sleep(poll_period)

def render_splash_screen(eth0_ip_address, wlan0_ip_address):
    p1 = subprocess.Popen(['tput', 'sc'])
    p1 = subprocess.Popen(['figlet', 'eth0: ' + eth0_ip_address, '-ctf', 'term'])
    p1.wait()
    p1 = subprocess.Popen(['figlet', 'wlan0: ' + wlan0_ip_address, '-ctf', 'term'])
    p1.wait()
    p1 = subprocess.Popen(['figlet', 'Please upload/insert H.264 media content...', '-ctf', 'term'])
    p1.wait()
    p1 = subprocess.Popen(['tput', 'rc'])
def mount_loop(usb, poll_period):
    while True:
        usb.usb_mount()
        usb.playlist_lock.acquire()
        for file in usb.playlist:
            print("playlist: " + file)
        usb.playlist_lock.release()
        time.sleep(poll_period)

if __name__ == '__main__':
    main()
