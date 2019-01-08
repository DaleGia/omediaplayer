import os

class usb_mounter:
    def __init__():
        # Place to store playlist file filepaths

        _playlist = []
        _mount_mapping = [("/dev/sda1", "/mnt/omedia_usb1", "sda"), ("/dev/sdb1", "/mnt/omedia_usb2", "sdb"), ("/dev/sdc1", "/mnt/omedia_usb3", "sdc"), ("/dev/sdd1", "/mnt/omedia_usb4", "sdd")]
        _file_formats = [".avi", ".mov", ".mkv", ".mp4", ".m4v", ".mp3"]
        # check whether omedia_usb1, omedia_usb2, omedia_usb3, 
        # omedia_usb4 exist. If they don't, create the 
        # directories.
        for drive in self._mount_mapping:
            if not(os.path.isdir(drive[1])):
                os.mkdir(drive[1])

    @property
    def _playlist(self):
        return self._playlist
   
    @property
    def _mount_mapping(self):
        return self._mount_mapping

    @property
    def _file_formats(self):
        return self._file_formats

    def usb_mount(self):
        #poll usb devices, mounts them, and builds playlist 
        # Check if directory is already mounted
        for drive in self._mount_mapping:
            # tests if USB drive is mounted
            p1 = subprocess.Popen(mount)
            p2 = subprocess.Popen(grep, drive[0], stdin=p1.stdout, stdout=subprocess.PIPE)
            p2.wait()
            ret = p2.communicate()[0]
            print "mount_drive: " + ret
            # If it isn't, it mounts the drive to it's assigned mount point.
            if not ret:
                p1 = subprocess.Popen("find", "/dev/disk/by-id/", "-lname", drive[2])
                ret = pi.communicate()[1]
                if ret:
                   p1 = subprocess.Popen("mount", "-t", "vfat", "-o", "ro", drive[0], drive[1])

        # Clear old playlist
        self._playlist.clear()
	# Get all of the file paths from the /mnt/ directories
        for extension in _file_formats:
            for drive in _mount_mapping:
                self._playlist.extend(glob(join(drive[1], extension)))
        # sort files alphabetically
        self._playlist.sort()
