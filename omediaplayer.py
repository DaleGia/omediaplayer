import usb_mounter
import time
import threading

def main():
    print("starting")
    usb = usb_mounter.usb_mounter()
    usb_mounting_thread = threading.Thread(target=mount_loop, args=(usb,))
    usb_mounting_thread.start()
    usb_mounting_thread.wait()
#    usb.usb_mount()
#    usb.usb_unmount()
 

    print("finished")

def mount_loop(usb):
    while True:
        usb.usb_mount()
        usb.playlist_lock.acquire()
        for file in usb.playlist:
            print("playlist: " + file)
        usb.playlist_lock.release()
        time.sleep(0.5)

if __name__ == '__main__':
    main()
