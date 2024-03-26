import time
from datetime import timedelta
class Swatch:
    def __init__(self, initial_time="00:00:00"):
        hours, minutes, seconds = map(int, initial_time.split(":"))
        self.current_time = hours * 3600 + minutes * 60 + seconds
        self.start_time = time.time() - self.current_time
        self.running = False

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.current_time
            self.running = True

    def stop(self):
        if self.running:
            self.current_time = time.time() - self.start_time
            self.running = False

    def restart(self):
        self.current_time = 0
        if self.running:
            self.start_time = time.time()
    def reset(self):
        self.current_time = 0
        self.running = False
    def get_time(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
        else:
            elapsed_time = self.current_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    def get_time_seconds(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
        else:
            elapsed_time = self.current_time
        #seconds = int(elapsed_time % 60)
        return elapsed_time
def seconds_to_time(total_seconds):
    duration = timedelta(seconds=total_seconds)
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

def time_format_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds