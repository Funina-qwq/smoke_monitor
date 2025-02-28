import time
import pymysql
from multiprocessing import Process


class DatabaseProcess(Process):
    def __init__(self,cfg,queue):
        super().__init__(name= "数据库传输进程",daemon=True)
        self.cfg = cfg
        self.queue = queue

    def run(self):
        database = self.get_database()
        while True:
            datas = self.queue.get()
            for data in datas:
                self.save_to_database(database,data)

    # to do
    def get_database(self):
        database = pymysql.connect(
                host=self.cfg.host,
                port=self.cfg.port,
                user=self.cfg.user,
                passwd=self.cfg.password,
                db=self.cfg.database,
                charset='utf8')

        return database

    def save_to_database(self,database,data):
            while True:
                try:           
                    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))   
                    cursor = database.cursor()  
                    try:      
                        sql = "insert into %s(camera_id,time,category,output,gray_map) values(%d,'%s','%s','%s','%s')"%(
                            str(self.cfg.datasheet),int(data.camera_id),date_time,str(data.category),str(data.vertexs),str(data.gray_map))   
                    except Exception as e:
                        print(e)
                    cursor.execute(sql)
                    database.commit()
                    break
                except Exception as e:
                    print("Submit failed.reconnecting...")
                    database.ping(True)


if __name__ == '__main__':
    from multiprocessing import Queue
    from configs.info import get_cfg
    from communication import SmokeData
    cfg = get_cfg()
    detect_database_queue = Queue()
    detect_database_queue.put([SmokeData(1,0.0,[],[],[])])
    database_process = DatabaseProcess(cfg.database,detect_database_queue)
    database_process.start()
    while True:
        pass