import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from process import nms,preprocess,post_process
from model.train.model_utils.utils import load_network
from model.network import make_network


class Detector(object):
      def __init__(self,cfg):
          network = make_network.get_network(cfg.settings).cuda()
          load_network(network,cfg.checkpoint)
          network.eval()         
          self.network = network
          self.preprocess = preprocess.preprocess(cfg.settings)

      def detect(self,imgs):
          if len(imgs) == 0:
             return post_process.get_null()
          inputs=self.preprocess(imgs)  
          outputs= []
          for i,input in enumerate(inputs):
            #不同模型输入参数格式调整
            if isinstance(input,tuple):    
              output=self.network(*input)                    
            else:
              output=self.network(input)
            post_process.post_process(output)
            nms.post_process(output)
            output = post_process.final_output(imgs[i],output)
            outputs.append(output)
            
          return outputs

if __name__ == '__main__':
   from model.configs.coco import config
   import cv2
   import warnings
   warnings.filterwarnings("ignore")

   cur_dir = os.path.dirname(os.path.abspath(__file__)) 
   test_imgs_dir = cur_dir +'/'+'test/data/'

   class cfg:
         settings = config
         checkpoint = cur_dir +'/'+'model/data/models/99.pth' 
   
   with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      imgs=[cv2.imread(test_imgs_dir+img)for img in os.listdir(test_imgs_dir)]

   detector = Detector(cfg)
   for item in detector.detect(imgs)[0]:
       print(item.shape)