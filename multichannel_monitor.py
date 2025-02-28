import time
from collections import deque
from multiprocessing import Process,Queue
from threading import Thread,Lock
from camera_monitor import Camera

lock = Lock()

class CameraThread(Thread):   
    def __init__(self,cfg):        
        super().__init__(name='摄像头'+ cfg.id,daemon=True)
        self.cfg = cfg
        self.dqeue = deque(maxlen=5)

    def run(self):
          camera = Camera(self.cfg)
          while True:
            date_time = time.time()
            image = camera.read()
            data = {"id":camera.id,"date_time":date_time,"image":image}

            with lock:
                try:
                    self.dqeue.append(data)
                except Exception as e:    
                    #超出去头插尾
                    self.dqeue.popleft()
                    self.dqeue.append(data)


    def get(self):      
        with lock:    
            try:                               
                data = self.dqeue.pop()   
            except Exception as e:
                data = {"id":self.cfg.id,"date_time":0.0,"image":None}
            
            return data
       

#单例模式todo
class MulCameraProcess(Process):
      def __init__(self,cfg,queue):
          super().__init__(name='多路摄像头进程',daemon=True)
          self.cfg = cfg
          self.queue = queue
               
      def run(self):     
          threads = []
          for cfg in self.cfg:
                thread = CameraThread(cfg)
                threads.append(thread)

          for thread in threads:
              thread.start()
              print('{}开始工作.'.format(thread.name))

          while True:
                time.sleep(1)
                datas = []
                date_time = time.time()
                
                for thread in threads:                            
                    data = thread.get()
                    if date_time - data['date_time']<1:
                       data['date_time'] = date_time    
                    else:
                       data['date_time'] = date_time
                       data['image'] = None  #区分超时的image
                    datas.append(data)

                try :
                  self.queue.put(datas,block=False)
                except Exception as e:
                  print(e)
                
          for thread in threads:
              thread.join()    
                                     

if __name__ == '__main__':
   from configs.info import get_cfg

   cfg = get_cfg()
   queue = Queue(6)#测试注意队列的阻塞不是错误
   process = MulCameraProcess(cfg.cameras,queue)
   process.start()  
   while True:
       pass
   process.join()


