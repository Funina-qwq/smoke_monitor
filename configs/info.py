#配置文件模板
import os
import sys
import configparser
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detector.model.configs.coco import config

def get_cfg():
    cfg = Config()
    return cfg

class CameraConfig(object):
      def __init__(self):
          self.id = None
          self.source = None

class ModelConfig(object):
    def __init__(self):
       self.settings = config
       self.checkpoint = None


class DataBaseConfig(object):
      def __init__(self):
        self.attrs=['host','port','user','password','database','datasheet']
        for attr in self.attrs:
           setattr(self,attr,None)


class Config(object):
    def __init__(self,cfgpath=None):
        self.model = None
        self.cameras = []
        self.database = DataBaseConfig()

        #读取配置文件
        cfgpath = os.path.dirname(os.path.abspath(__file__)) + '\config.ini' if cfgpath == None else cfgpath
        conf = configparser.ConfigParser()
        try:
            conf.read(cfgpath,encoding="utf-8")
        except Exception as e:
            print(e)
            print('读取配置文件失败.')
            sys.exit()

        #检查model、camera和database配置节点
        try:
            #model配置
            self.model = ModelConfig()
            self.model.checkpoint =os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                   conf.items('checkpoint')[0][1])

            #cameras配置
            for camera_cfg in conf.items('camera'):
                cfg = CameraConfig()
                cfg.id = camera_cfg[0]
                cfg.source = camera_cfg[1]
                self.cameras.append(cfg)   
 
            #database配置
            for argname,argvalue in conf.items('database') :
                integer = ['port']
                if integer.count(argname):
                    argvalue = int(argvalue)
                setattr(self.database,argname,argvalue)
            
            #detection配置
            for argname,argvalue in conf.items('detection') :
                setattr(self,argname,argvalue)
            self.model.settings.test.ct_score = self.confidence
            setattr(self.model,'interval',int(self.interval))

            #判断是否有属性缺失
            for attr in self.database.attrs:
                assert getattr(self.database,attr) is not None,'缺失{}参数'.format(attr)

        except Exception as e:
            print(e)
            print('配置文件内容缺失.')
            sys.exit()

        
if __name__ == '__main__':
   cfg= Config()
   print('摄像头配置:')
   for camera in cfg.cameras:
       print(camera.__dict__)
   delattr(cfg.database,'attrs')
   print('数据库配置:\n{}'.format(cfg.database.__dict__))
   print('模型路径:\n{}'.format(cfg.model.checkpoint))
   
   
    
  