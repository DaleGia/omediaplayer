import subprocess

class video_looper:
    def __init__(self):
       playlist_paths = []
       omx_arguments = [
    def loop_playlist(self):
        while True:
            number_of_files = len(playlist_paths)
             if(number_of_files > 1)
                omx_arguments.extend(['-b', '-r', 
                for files in playlist_paths:
                    p1 = subprocess.Popen("omxplayer"

