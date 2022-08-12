from queue import Queue
from threading import Thread
import time 

my_queue = Queue()

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


@threaded
def lock_loop():
    for x in list(range(1,70000,2)):
        my_queue.put(f"a{x}")
        if (x ==  9701):
            with my_queue.mutex:                
                time.sleep(10)  
            my_queue.put("GG Let's see")
            my_queue.task_done()
          
                

@threaded
def normal_loop():
    for x in list(range(2,70000,2)):
        my_queue.put(f"b{x}")

normal_loop()
lock_loop()

time.sleep(70) 
print(list(my_queue.queue))