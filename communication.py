from multiprocessing import Queue

# to delete
class CameraThreadsData:
      def __init__(self,queue,barrier,date_time):
        self.queue = queue
        self.barrier = barrier
        self.date_time = date_time
  

class SmokeData:
    def __init__(self,camera_id,time,category,vertexs,gray_map):
        self.camera_id = str(camera_id)
        self.time = time
        self.category = str(category)
        self.vertexs = str(vertexs)
        self.gray_map = str(gray_map)
