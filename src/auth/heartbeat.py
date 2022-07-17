from threading import Timer
import time
import datetime

import requests
# Set rate of heartbeats in seconds
HEART_RATE = 2
MAX_HB_TIMEOUTS = 5

## Wrapper over timer class to create a repeat timer
class HeartBeat(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
