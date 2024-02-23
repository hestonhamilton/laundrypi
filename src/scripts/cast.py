#!/usr/bin/env python3
import pychromecast
from pychromecast.controllers.media import MediaController
import time

# Discover and connect to the Google Nest Speaker
chromecasts, browser = pychromecast.get_chromecasts()

AUDIO_URL = "https://od.lk/s/MzdfMjc5NzQ4MDZf/laundry_ready.mp3"
CAST_TARGET = "Home group"
BROADCAST_VOLUME = 0.8

# Ensure that the list is not empty
if chromecasts:
    cast = None
    for cc in chromecasts:
        if cc.name == CAST_TARGET:
            cast = cc
            break

    if cast:
        # Ensure the Chromecast device is connected
        cast.wait()

        original_volume = cast.status.volume_level
        print(str(original_volume)) 
        # Only change volume if it differs from target
        if original_volume != BROADCAST_VOLUME:
            cast.set_volume(BROADCAST_VOLUME)        

        media = pychromecast.controllers.media.MediaController()
        cast.register_handler(media)
        media.play_media(AUDIO_URL, 'audio/mp3')
        media.block_until_active()
        media.play()

        # Set volume back to original value
        if original_volume != BROADCAST_VOLUME:
            time.sleep(5)
            cast.set_volume(original_volume)        

    else:
        print(f"No Chromecast with the name {cast_target} was found")
else:
    print("No Chromecasts found on the network")

# Stop discovery
pychromecast.discovery.stop_discovery(browser)
