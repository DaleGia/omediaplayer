import os
import subprocess
import glob
import threading
import time
class usb_mounter:
    def __init__(self):
        # Place to store playlist file filepaths

        self.playlist = []
        self.playlist_lock = threading.Lock()
        self._mount_mapping = [("/dev/sda1", "/mnt/omedia_usb1", "sda", False), ("/dev/sdb1", "/mnt/omedia_usb2", "sdb", False), ("/dev/sdc1", "/mnt/omedia_usb3", "sdc", False), ("/dev/sdd1", "/mnt/omedia_usb4", "sdd", False)]
        self._is_drive_mounted = [False, False, False, False]
        self._file_formats = [".avi", ".mov", ".mkv", ".mp4", ".m4v", ".mp3"]
        # check whether omedia_usb1, omedia_usb2, omedia_usb3, 
        # omedia_usb4 exist. If they don't, create the 
        # directories.
        for drive in self._mount_mapping:
            if not(os.path.isdir(drive[1])):
                os.mkdir(drive[1])
                #if(os.mkdir(drive[1])):
                    #print("Created directory: " + drive)

    def usb_unmount(self): 
        for drive in self._mount_mapping:
            # tests if USB drive is mounted
            p1 = subprocess.Popen("mount", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p1.wait()
            is_mounted = str(p1.communicate()[0]).find(drive[0])
            # If it isn't, it mounts the drive to it's assigned mount point.
            if(is_mounted != -1):
               #print("unmounting: " + drive[0] + " from " + drive[1])
                p1 = subprocess.Popen(["umount", drive[1]], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                p1.wait()

    def usb_mount(self):
        #poll usb devices, mounts them, and builds playlist 
        # Check if directory is already mounted
        for drive in self._mount_mapping:
            # tests if USB drive is mounted
            #print("Searching for mounted drives on:", drive[2])
            p1 = subprocess.Popen("mount", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p1.wait()
            is_mounted = str(p1.communicate()[0]).find(drive[0])
            #print("is_mounted: " + str(is_mounted))
            #print("Searching for connected USB devices on:", drive[2])
            p1 = subprocess.Popen(["find", "/dev/", "-name", drive[2]], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p1.wait()
            is_usb_connected = str(p1.communicate()[0]).find(drive[2])
            #print("is_usb_connected: " + str(is_usb_connected))
            # If it isn't, it mounts the drive to it's assigned mount point.
            if(is_mounted == -1):
                if(is_usb_connected > -1):
                   #print("Mounting: " + drive[0] + " to: " + drive[1])
                   p1 = subprocess.Popen(["mount", "-t", "vfat", drive[0], drive[1]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                   p1.wait() 
                   #Check if mounting was successful
                   p1 = subprocess.Popen("mount", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                   p1.wait() 
                   is_mounted = str(p1.communicate()[0]).find(drive[0])
                   #print("is_mounted: " + str(is_mounted))
                   p1 = subprocess.Popen(["find", "/dev/", "-name", drive[2]], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                   p1.wait() 
                   is_usb_connected = str(p1.communicate()[0]).find(drive[2])
                   #print("is_usb_connected: " + str(is_usb_connected))
                   if(is_mounted > -1):
                      if(is_usb_connected > -1):
                          #print("Mount successful")
                          drive = (drive[0], drive[1], drive[2], True)
                      else:
                          #print("Mount unsuccessful")
                          drive = (drive[0], drive[1], drive[2], False)
                   else:
                       #print("Mount unsuccessful")
                       drive = (drive[0], drive[1], drive[2], False)

                #else:
                    #print("No USB connected to " + drive[0])
            else:
                if(is_usb_connected == -1):
                   #print(drive[0] + "has been disconnected. I am unmounting it...")
                   p1 = subprocess.Popen(["umount", drive[1]], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                   p1.wait()
                #else:
                   #print(drive[0][0] + " is already mounted to: " + drive[1])        
            #print("")
        # Clear old playlist
        self.playlist_lock.acquire()
        self.playlist.clear()
	# Get all of the file paths from the /mnt/ directories
        for extension in self._file_formats:
            for drive in self._mount_mapping:
                os.chdir(drive[1])
                for file in glob.glob("*"+extension):
                   self.playlist.append(drive[1] + "/" + file)
        # sort files alphabetically
        self.playlist.sort()
        self.playlist_lock.release()
