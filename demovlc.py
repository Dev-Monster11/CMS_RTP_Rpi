import vlc
from time import sleep


instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new("10-6.mp4")
media.get_mrl()
player.set_media(media)
player.play()
sleep(1)
while True:
    pass
# player.set_mrl("rtsp://jewell:Jennydog14@jewellfamily.ddns.net/stream1")
# media = vlc.MediaPlayer("10-6.mp4")
# print(media)
# media.play()
