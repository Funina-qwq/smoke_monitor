import argparse
import os 
import sys
from configs.info import Config
from multichannel_monitor import MulCameraProcess
from multiprocessing import Queue
from detect import DetectProcess
import json

if __name__ == '__main__':
    spawn_path = os.path.dirname(os.path.abspath(__file__))+'/samples.json'
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--number",default=100)
    args = parser.parse_args()

    cfg =Config(os.path.dirname(os.path.abspath(__file__)) + '/configs/makedata.ini')
    mulcamera_detect_queue = Queue()
    detect_database_queue = Queue()

    mulcamera_process = MulCameraProcess(cfg.cameras,mulcamera_detect_queue)
    detect_process = DetectProcess(cfg.model,mulcamera_detect_queue,detect_database_queue)
    mulcamera_process.start()
    detect_process.start()

    number = args.number
    samples = []
    while number > 0:
        if not detect_database_queue.empty():
           datas = detect_database_queue.get()
           for data in datas:
                print(data)
                if data.category != '[]':
                    samples.append({'camera_id':data.camera_id,"category":data.category,"output":data.vertexs,"grap_map":data.gray_map,"time":data.time})
                    number -= 1
                    print('生成进度：{}/{}'.format((args.number-number),args.number))
        
    
    print("正在写入...")
    with open(spawn_path,'w') as f:
             num = 0
             datas = {}
             for data in samples:
                if num<100:
                   datas.update({num:data})
                   num +=1  
             print(datas.keys())
             json.dump(datas,f)   
    print("写入完成")  
    """   
    with open(spawn_path,'r') as f:
         datas = json.load(f)
         print(datas['29']['output'])
    
    
    sys.exit()