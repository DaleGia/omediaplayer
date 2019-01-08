import usb_mounter

def main():
    print("starting")
    usb = usb_mounter.usb_mounter()
    usb.usb_mount()
#    usb.usb_unmount()
 
    for file in usb.playlist:
        print("playlist: " + file)

    print("finished")

if __name__ == '__main__':
    main()
