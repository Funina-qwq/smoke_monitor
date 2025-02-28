import torch
import numpy as np
import cv2


def compute_num(offset_0, offset_1, thre=3):
    offset_0_front = torch.roll(offset_0, shifts=1, dims=1)
    offset_1_front = torch.roll(offset_1, shifts=1, dims=1)
    offset_0_front_2 = torch.roll(offset_0, shifts=2, dims=1)
    offset_1_front_2 = torch.roll(offset_1, shifts=2, dims=1)
    cos_0 = torch.sum(offset_0 * offset_0_front, dim=2)
    cos_1 = torch.sum(offset_1 * offset_1_front, dim=2)
    cos_0_2 = torch.sum(offset_0 * offset_0_front_2, dim=2)
    cos_1_2 = torch.sum(offset_1 * offset_1_front_2, dim=2)
    cos_0 = ((cos_0 < -0.1) & (cos_0_2 > 0.1)).to(torch.int)
    cos_1 = ((cos_1 < -0.1) & (cos_1_2 > 0.1)).to(torch.int)
    nums = (torch.sum(cos_1, dim=1) - torch.sum(cos_0, dim=1) >= thre).to(torch.int)
    nums = nums.unsqueeze(1).unsqueeze(2).expand(offset_0.size(0), offset_0.size(1), offset_0.size(2))
    return nums


def post_process(output):
    end_py = output['py'][-1].detach()
    gcn_py = output['py'][-2].detach()
    
    if len(end_py) == 0:
        return 0
    
    offset_1 = end_py - torch.roll(end_py, shifts=1, dims=1)
    offset_0 = gcn_py - torch.roll(gcn_py, shifts=1, dims=1)
    nokeep = compute_num(offset_0, offset_1)
    end_poly = end_py * (1 - nokeep) + gcn_py * nokeep
    output['py'].append(end_poly)


def get_null():
    category = '[]'
    vertexs = '[[[]]]'
    grayMap = '[[]]'
    return category,vertexs,grayMap


#最终处理
def final_output(img,output):
    category = output['detection'][:,-1].detach().cpu()
    if not category.numel():
       return get_null()
    else:
        category= category.numpy().astype(int) 
        vertexs=output['py']
        vertexs = vertexs[-1] if isinstance(vertexs, list) else vertexs
        vertexs = vertexs.detach().cpu().numpy()

    grayMap = cv2.cvtColor(cv2.resize(img,(640,480)),cv2.COLOR_RGB2GRAY) #大小接口重构to do 
    return category,vertexs,grayMap


