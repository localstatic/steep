
import thread
import time

class Timer:
    def __init__(self, interval, function, length = None):
        self._ticks = self._remaining = length
        self._lock = thread.allocate_lock()
        self._interval = interval
        self._function = function
        self._running = False

    def start(self):
        self._lock.acquire()
        self._remaining = self._ticks
        self._running = True
        thread.start_new_thread(self._run, ())
        self._lock.release()
        
    def stop(self):
        self._lock.acquire()
        self._running = False
        self._lock.release()
        
    def is_running(self):
        return self._running
    
    def _run(self):
        while self._running and (self._remaining == None or self._remaining > 0):
            time.sleep(self._interval)
            self._function()

            if self._remaining <> None: 
                self._remaining = self._remaining - 1

     
