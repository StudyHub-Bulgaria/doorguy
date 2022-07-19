from threading import Timer
import time
import datetime

import requests
# Set rate of heartbeats in seconds
HEART_RATE = 30
MAX_HB_TIMEOUTS = 3
DOORGUY_VER = "0.0.2"

## Wrapper over timer class to create a repeat timer
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
