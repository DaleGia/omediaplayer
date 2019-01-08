import usb_mounter

def main():
    print("starting")
    usb = usb_mounter()
    usb.usb_mount()
    print("finished")
