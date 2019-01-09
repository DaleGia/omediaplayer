import socket
import fcntl
import struct
import threading

class networking:
    def __init__(self):
        self.eth0_ip_address = None
        self.wlan0_ip_address = None
        self.ip_address_lock = threading.Lock()

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])

    def get_all_ip_addresses(self):
        self.ip_address_lock.acquire()
        self.wlan0_ip_address = self.get_ip_address('wlan0')
        self.eth0_ip_address =  self.get_ip_address('eth0')
        self.ip_address_lock.release()
