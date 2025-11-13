import time
import pychromecast
from pychromecast.controllers import BaseController

# -----------------------------
#  Custom Namespace Controller
# -----------------------------
class HelloWorldController(BaseController):
    def __init__(self):
        super().__init__("urn:x-cast:com.google.cast.sample.helloworld")

    def show_text(self, text):
        """Send the SHOW_TEXT message to the custom receiver."""
        self.send_message({"type": "SHOW_TEXT", "text": text})


# -----------------------------
#  Config
# -----------------------------
NAME = "Lord of the Drums"
MESSAGE = f"Welcome {NAME}!"

# Change this to your GitHub Pages URL:
RECEIVER_URL = "https://skylar-lorena.github.io/chromecast/v=2"


# -----------------------------
#  Discover Chromecast
# -----------------------------
chromecasts, browser = pychromecast.get_chromecasts()

if not chromecasts:
    raise SystemExit("No Chromecast found — check WiFi or network isolation.")

# Pick the Hisense TV (or fallback to the first one)
cc = next(
    (c for c in chromecasts if "Hisense" in c.name or "Living Room TV" in c.name),
    chromecasts[0]
)

print(f"Connecting to Chromecast '{cc.name}'…")
cc.wait()
print("Connected.")
print("is_connected:", cc.socket_client.is_connected)


# -----------------------------
#  Stop Current App Safely
# -----------------------------
try:
    if cc.app_id != pychromecast.IDLE_APP_ID:
        print("Stopping current app…")
        cc.quit_app()
        time.sleep(1)
    else:
        print("Chromecast already idle.")
except Exception as e:
    print("Warning during quit_app:", e)


# -----------------------------
#  Load Your Receiver App
# -----------------------------
print(f"Loading receiver URL: {RECEIVER_URL}")

mc = cc.media_controller
mc.play_media(RECEIVER_URL, "text/html")

mc.block_until_active()
time.sleep(2)

print("Receiver active.")


# -----------------------------
#  Register Custom Namespace
# -----------------------------
hwc = HelloWorldController()
cc.register_handler(hwc)

print("Sending message…")
hwc.show_text(MESSAGE)

print("Cast sent successfully!")
