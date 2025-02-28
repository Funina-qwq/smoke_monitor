import time
import functools
from threading import Thread

def timeout_decorator(timeout,callback = lambda:print('运行超时'),alarm=True):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            thread = Thread(target=func,args=args,kwargs=kwargs,daemon=True)
            thread.start()
            thread.join(timeout)
            if thread.is_alive():
               callback()
               if alarm == True:
                  raise TimeoutError
        return inner
    return wrapper

if __name__ == '__main__':
   @timeout_decorator(3)
   def delay(timeout=5):
       time.sleep(timeout)
   delay(1)
   delay()