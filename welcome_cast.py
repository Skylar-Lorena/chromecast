import time
import pychromecast

NAME = "Lord"          # or "Goddess"
MESSAGE = f"Welcome {NAME}!"

# 1. Discover Chromecasts on the network
chromecasts, browser = pychromecast.get_chromecasts()
if not chromecasts:
    raise SystemExit("No Chromecast found – check Wi-Fi")

# 2. Pick the one connected to your Hisense TV (by friendly name or UUID)
cc = next(c for c in chromecasts if "Hisense" in c.name or "Living Room TV" in c.name)

# 3. Stop whatever is playing
cc.quit_app()
time.sleep(1)

# 4. Launch a tiny receiver that shows HTML
mc = cc.media_controller
mc.play_media(
    "https://cdn.jsdelivr.net/gh/coding-to-music/welcome-cast@latest/receiver.html",
    "text/html"
)
mc.block_until_active()
time.sleep(2)

# 5. Inject the message via the Cast "data" channel
cc.send_message(
    "urn:x-cast:com.google.cast.sample.helloworld",
    {"type": "SHOW_TEXT", "text": MESSAGE}
)

print(f"Cast sent: {MESSAGE}")