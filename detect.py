from multiprocessing import Process
from detector.detector import Detector
from communication import SmokeData
from detector.process.post_process import get_null 
import time 

class DetectProcess(Process):
    def __init__(self,cfg,mulcamera_detect_queue,detect_database_queue):
        super().__init__(name='识别进程',daemon=True)
        self.cfg = cfg
        self.mulcamera_detect_queue = mulcamera_detect_queue
        self.detect_database_queue = detect_database_queue

    def run(self):
        detector = Detector(self.cfg)  
        while True:
            time.sleep(self.cfg.interval)
            if not self.mulcamera_detect_queue.empty():
                ids = []
                images = []
                images_copy = []
                results = []
                datas = self.mulcamera_detect_queue.get()  #id ,time,image
                date_time = datas[0]['date_time']
              
                for data in datas:
                    ids.append(data['id'])
                    images.append(data['image'])
                    if data['image'] is not None:
                        images_copy.append(data['image'])

                outputs = detector.detect(images_copy)   
                null_num = 0
                for i,id in enumerate(ids):
                    if images[i] is not None:
                       data = SmokeData(id,date_time,*outputs[i-null_num])
                    else:
                       null_num += 1
                       data = SmokeData(id,date_time,*get_null())
                    results.append(data)
               # print(results[0].__dict__)
                self.detect_database_queue.put(results)#暂时不写异常因为提交频率低
                


if __name__ == '__main__':
    from configs.info import get_cfg
    from multiprocessing import Queue
    import numpy as np
    import cv2

    cfg = get_cfg()
    queue1 = Queue()
    queue2 = Queue()
    img1 =cv2.imread('0.jpg')
    img2 =cv2.imread('1.jpg')
    images = [{'id':0,'date_time':0,'image':img1},
             {'id':1,'date_time':0,'image':img2}
              ]
    #images.append({'id':3,'data_time':0,'image':None})
    queue1.put(images)
    detect = DetectProcess(cfg.model,queue1,queue2)
    detect.start()

    while True:
         if not queue2.empty():
            datas = queue2.get()
            print(datas[0].__dict__)