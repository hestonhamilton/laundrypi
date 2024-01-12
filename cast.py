#!/usr/bin/env python3
import pychromecast
from pychromecast.controllers.media import MediaController
import time

# Discover and connect to the Google Nest Speaker
chromecasts, browser = pychromecast.get_chromecasts()

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
        media.play_media('https://download.samplelib.com/mp3/sample-3s.mp3', 'audio/mp3')
        media.block_until_active()
        media.play()

    else:
        print("No Chromecast with the name " + cast_target + " was found")
else:
    print("No Chromecasts found on the network")

# Stop discovery
pychromecast.discovery.stop_discovery(browser)
