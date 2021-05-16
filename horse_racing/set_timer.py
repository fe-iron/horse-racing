import threading
import time
import schedule

t = time.localtime()
now_minute = int(time.strftime("%M", t))
if now_minute + 4 == 60:
    now_minute = 0
elif now_minute + 4 == 61:
    now_minute = 1
elif now_minute + 4 == 62:
    now_minute = 2
elif now_minute + 4 == 63:
    now_minute = 3
elif now_minute + 4 == 64:
    now_minute = 4
else:
    now_minute += 4
now_sec = int(time.strftime("%S", t))
now_sec = 0


def set_time():
    global now_minute, now_sec
    now = time.localtime()
    n_minute = int(time.strftime("%M", now))
    future_minute = int(now_minute)
    now_sec = time.strftime("%S", now)
    if abs(future_minute - n_minute) >= 4:
        if future_minute + 4 == 60:
            future_minute = 0
        elif future_minute + 4 == 61:
            future_minute = 1
        elif future_minute + 4 == 62:
            future_minute = 2
        elif future_minute + 4 == 63:
            future_minute = 3
        elif future_minute + 4 == 64:
            future_minute = 4
        else:
            future_minute += 4
        now_minute = future_minute


schedule.every(4).minutes.do(set_time)


class SetTime(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            schedule.run_pending()


