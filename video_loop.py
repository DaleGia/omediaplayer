import os
import signal
import subprocess
import time
import threading
import logging
class video_loop(object):
    def __init__(self, arg):
       self.playlist_paths = []
       self.lock = threading.Lock()
       self.omx_arguments = {'black_background': True, 'refresh': True, 'audio_output': 'both', 'loop': False, 'mute': False, 'arguments_change_flag': False, 'lock': threading.Lock()}
       self._argument_list = ['']
       self._argument_change_flag = False
       self.usb = arg

    def _arguments_builder(self):
        if not self.omx_arguments['lock'].acquire(True, 2):
            return
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
        self.omx_arguments['lock'].release()
 
    def play_playlist(self):
        if not self.usb.lock.acquire(True, 2):
            return
        self.playlist_paths = self.usb.playlist
        number_of_files = len(self.playlist_paths)
        self.usb.lock.release()
        if(number_of_files > 1):
            if not self.omx_arguments['lock'].acquire(True, 2):
                logging.info('Video looper couldnt get lock. exiting') 
                return
            self.omx_arguments['loop'] = False 
            self.omx_arguments['refresh'] = True 
            self.omx_arguments['black_background'] = True 
            self._arguments_builder()
            self.omx_arguments['lock'].release()
#            print(str(self.playlist_paths)) 
            for file in self.playlist_paths:
                p1 = subprocess.Popen(["omxplayer", file] + self._argument_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(str(p1.pid) +': Playing: ' + file) 
                while(p1.poll() == None):
                    if not self.omx_arguments['lock'].acquire(True, 2):
                        print('Video looper couldnt get lock. exiting') 
                        os.killpg(p1.pid, signal.SIGTERM)
                        return
                    if(self.omx_arguments['arguments_change_flag']):
                        print('argument change flag detected, reseting') 
                        print('argument change flag detected, reseting') 
                        os.killpg(p1.pid, signal.SIGTERM)
                        exit_flag = True
                        self.omx_arguments['arguments_change_flag'] = False
                    
                    self.omx_arguments['lock'].release()
                    time.sleep(0.1)
#                    print(str(p1.pid) +': Polling: ' + str(p1.poll()))

        elif(number_of_files > 0):
            if not self.omx_arguments['lock'].acquire(True, 2):
                return
            self.omx_arguments['loop'] = True 
            self.omx_arguments['refresh'] = True 
            self.omx_arguments['black_background'] = True 
            self._arguments_builder()
            self.omx_arguments['lock'].release()
            p1 = subprocess.Popen(["omxplayer", self.playlist_paths[0]] + self._argument_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(str(p1.pid) +': Playing: ' +  self.playlist_paths[0]) 
            while(p1.poll() == None):
                if not self.omx_arguments['lock'].acquire(True, 2):
                    os.killpg(p1.pid, signal.SIGTERM)
                    return
                if(self.omx_arguments['arguments_change_flag']):
                    logging.info('argument change flag detected, reseting') 
                    print('argument change flag detected, reseting') 
                    os.killpg(p1.pid, signal.SIGTERM)
                    self.omx_arguments['arguments_change_flag'] = False

                self.omx_arguments['lock'].release()
                time.sleep(0.1)
