from configs.info import get_cfg
from multiprocessing import Queue
from multichannel_monitor import MulCameraProcess
from detect import DetectProcess
from database import DatabaseProcess

#八个摄像头捆绑在一起数据升维
def main():
    cfg = get_cfg()    

    #通信队列
    mulcamera_detect_queue =  Queue(16)
    detect_database_queue =  Queue(16)
    
    #启动多路摄像头系统和数据库读写进程
    mulcamera_process = MulCameraProcess(cfg.cameras,mulcamera_detect_queue)
    detect_process = DetectProcess(cfg.model,mulcamera_detect_queue,detect_database_queue)
    database_process = DatabaseProcess(cfg.database,detect_database_queue)

    mulcamera_process.start()
    detect_process.start()
    database_process.start()
    #to do
    mulcamera_process.join()
    detect_process.join()
    database_process.join()


if __name__ == "__main__":      
   main()
   while True:
       pass
   

