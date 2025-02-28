import cv2
from tools.decorator import timeout_decorator

#处理rstp网络摄像头未连接的延时问题
def open_camera(camera,timeout=3):
    @timeout_decorator(timeout,lambda:print('摄像头{}读取超时.'.format(camera.id)),False) 
    def get_capture(source):
        camera.cap = cv2.VideoCapture(source)#引用传递
          
    get_capture(camera.source)

def check_camera(camera):
    camera_state = True
    if camera.cap == None: 
       camera_state = False
    else:
      ret,frame = camera.cap.read()   
      if not ret:
         camera_state = False
    return camera_state
      
#单摄像头
class Camera:
     def __init__(self,cfg):
         id,source=cfg.id,cfg.source
         self.id=id 
         self.source=source if source != '0' else 0 #rstp与内置摄像头与mp4                 
         self.cap = None
         open_camera(self)     #专用函数打开摄像头

     def read(self):           
         if check_camera(self) == False:
            print('重新打开摄像头{}'.format(self.id))
            open_camera(self)

         if check_camera(self): 
            ret,frame = self.cap.read()  
         else:
            frame = None             

         return frame
 

if __name__ == '__main__':
   import os
   import sys
   import time
   sys.path.append(os.path.dirname(os.path.abspath(__file__)))
   from configs.info import get_cfg
   
   cfg = get_cfg()
   camera = Camera(cfg.cameras[0])#VideoCapture读取rstp如果摄像头未连接会卡死
   while True:
       # _time = time.time()
        result = camera.read()
       # print(time.time()-_time)   
       