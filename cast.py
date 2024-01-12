#!/usr/bin/env python3
import pychromecast
from pychromecast.controllers.media import MediaController
import time

# Discover and connect to the Google Nest Speaker
chromecasts, browser = pychromecast.get_chromecasts()

audio_url = "https://od.lk/s/MzdfMjc5NzQ4MDZf/laundry_ready.mp3"
cast_target = "Home group"
# Ensure that the list is not empty
if chromecasts:
    cast = None
    for cc in chromecasts:
        if cc.name == cast_target:
            cast = cc
            break

    if cast:
        # Ensure the Chromecast device is connected
        cast.wait()

        media = pychromecast.controllers.media.MediaController()
        cast.register_handler(media)
        media.play_media(audio_url, 'audio/mp3')
        media.block_until_active()
        media.play()

    else:
        print(f"No Chromecast with the name {cast_target} was found")
else:
    print("No Chromecasts found on the network")

# Stop discovery
pychromecast.discovery.stop_discovery(browser)
