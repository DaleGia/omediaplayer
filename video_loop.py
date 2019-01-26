import subprocess
import time
import threading

class video_loop(object):
    def __init__(self, arg):
       self.playlist_paths = []
       self.lock = threading.Lock()
       self.omx_arguments = {'black_background': True, 'refresh': True, 'audio_output': 'both', 'loop': False, 'mute': False}
       self._argument_list = ['']
       self._argument_change_flag = False
       self.usb = arg

    def _arguments_builder(self):
        self.lock.acquire(True, 2)
        self._argument_list.clear()
        if(self.omx_arguments['black_background']):
             self._argument_list.append("-b")
        if(self.omx_arguments['refresh']):
             self._argument_list.append("-r")
        if(self.omx_arguments['audio_output'] == 'both'):
             self._argument_list.extend(["-o","both"])
        if(self.omx_arguments['audio_output'] == 'hdmi'):
             self._argument_list.extend(["-o","hdmi"])
        if(self.omx_arguments['audio_output'] == 'analog'):
             self._argument_list.extend(["-o","analog"])
        if(self.omx_arguments['loop']):
             self._argument_list.append("--loop")
        self.lock.release()
 
    def play_playlist(self):
        if not self.usb.lock.acquire(True, 2):
            return
        self.playlist_paths = self.usb.playlist
        number_of_files = len(self.playlist_paths)
        self.usb.lock.release()
        if(number_of_files > 1):
            if not self.lock.acquire(True, 2):
                return
            self.omx_arguments['loop'] = False 
            self.omx_arguments['refresh'] = True 
            self.omx_arguments['black_background'] = True 
            self._arguments_builder()
            self.lock.release()

            for file in playlist_paths:
                if not self.lock.acquire(True, 2):
                    return
                logging.info('Playing: ' + file) 
                print('Playing: ' + file) 
                p1 = subprocess.Popen("omxplayer", file, self._argument_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.lock.release()
                poll = p1.poll()
                while not p1.poll():
                    if not self.lock.acquire(True, 2):
                        return
                    if(self._argument_change_flag):
                        logging.info('argument change flag detected, reseting') 
                        print('argument change flag detected, reseting') 
                        p1.kill()
                        self.argument_change_flag = False
                        self.lock.release()
                    
                    self.lock.release()
                    time.sleep(0.1)

        elif(number_of_files > 0):
            if not self.lock.acquire(True, 2):
                return
            self.omx_arguments['loop'] = True 
            self.omx_arguments['refresh'] = True 
            self.omx_arguments['black_background'] = True 
            self._arguments_builder()
            p1 = subprocess.Popen(["omxplayer", self.playlist_paths[0]] + self._argument_list,  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.lock.release()
            poll = p1.poll()
            while not p1.poll():
                if not self.lock.acquire(True, 2):
                    return
                if(self._argument_change_flag):
                    logging.info('argument change flag detected, reseting') 
                    print('argument change flag detected, reseting') 
                    p1.kill()
                    self.argument_change_flag = False

                self.lock.release()
                time.sleep(0.1)
