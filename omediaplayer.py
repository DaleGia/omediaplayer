import vlc

url = '/home/dg/Downloads/test.avi'
player = vlc.mediaPlayer()
player.fullscreen.enter()
player.play(url)