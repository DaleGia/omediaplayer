class usb_mounter:
    def __init__(mount_drives, file_formats):
    # Place to store playlist file filepaths

    _playlist = []
    # check whether omedia_usb1, omedia_usb2, omedia_usb3, 
    # omedia_usb4 exist. If they don't, create the 
    # directories.
    for drive in mount_drives
        if not(os.path.isdir(join("/mnt/", drive)))
            os.mkdir(join("/mnt/", drive)

    @property
    def playlist(self):
        return self._playlist

    def usb_mount(self):
        #poll usb devices, mounts them, and builds playlist 
        # Check if directory is already mounted
        p1 = subprocess.Popen(mount)
        p2 = subprocess.Popen(grep, mount_drives[1], stdin=p1.stdout, stdout=subprocess.PIPE)
        p2.wait()
        ret = p2.communicate()[0]

        print "mount_drive[1]: " + ret
#       if not mount | grep "/mnt/omedia_usbpython mount command raspberry pi1" > /dev/null;"
        if not ret
            p1 = subprocess.Popen("find", "/dev/disk/by-id/", "-lname", "'*.sda'")
            ret = p1.communicate()[1]
            # Check if usb drive is connected
            # if find /dev/disk/by-id/ -lname '*sda'
            if ret
                # mount usb drive
                # mount -t vfat -o ro /dev/sda1 /mnt/usb1
               p1 = subprocess.Popen("mount", "-t", "vfat", "-o", "ro", "/dev/sda1", mount_drives[1])
        if not mount | grep "/mnt/omedia_usb2" > /dev/null;
            if find /dev/disk/by-id/ -lname '*sdb'
                mount -t vfat -o ro /dev/sdb1 /mnt/usb1	
        if not mount | grep "/mnt/omedia_usb3" > /dev/null;
            if find /dev/disk/by-id/ -lname '*sdc'
                mount -t vfat -o ro /dev/sdc1 /mnt/usb1
        if not mount | grep "/mnt/omedia_usb4" > /dev/null;
	    if find /dev/disk/by-id/ -lname '*sdd'
	        mount -t vfat -o ro /dev/sdd1 /mnt/usb1

        # Clear old playlist
        self._playlist.clear()
	# Get all of the file paths from the /mnt/ directories
        for extension in file_formats
            for drive in mount_drives:
                self._playlist.extend(glob(join(drive, extension)))
        # sort files alphabetically
        self._playlist.sort()
