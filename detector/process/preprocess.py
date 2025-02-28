import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import torch
from model.dataset.train.utils import augment
from model.dataset.collate_batch import collate_batch

#多进程优化to do
def preprocess(cfg):
    #pool = Pool(8)
    def single_image_process(img):
        orig_img, inp, trans_input, trans_output, flipped, center, scale, inp_out_hw = \
                augment(
                    img, 'test',
                    cfg.data.data_rng, cfg.data.eig_val, cfg.data.eig_vec,
                    cfg.data.mean, cfg.data.std, cfg.commen.down_ratio,
                    cfg.data.input_h, cfg.data.input_w, cfg.data.scale_range,
                    cfg.data.scale, cfg.test.test_rescale, cfg.data.test_scale
                )

        data = {'inp': torch.from_numpy(inp).cuda()}
        meta = {'center': center, 'scale': scale, 'test': '', 'img_name': ''}
        data.update({'meta': meta})
        data = collate_batch([data]) #原项目本身兼容性差
        return data['inp'],data

    # to do单传一张图
    def pre_process(imgs):
        #results = pool.map(single_image_process,imgs)
        results = [single_image_process(img) for img in imgs]
        return results
    return pre_process

if __name__ == '__main__':
   pass