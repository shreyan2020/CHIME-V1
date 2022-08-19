import torch
import torchvision.models as models
from torchvision import datasets, models, transforms
import numpy as np
from transformers import ViTForImageClassification
from transformers import ViTFeatureExtractor
import os
from PIL import Image as PImage
import pathlib
import torch
import torch.nn as nn
import torch.nn.functional as F
from math import isclose
from tqdm import tqdm
import cv2
from sqlite3 import Error
import sqlite3


def main():
    data_transforms = transforms.Compose([
        transforms.Resize(299),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    path = '../data/dataset/prod_run_saliency/'
    # model_main=torch.load("./final_models/best_inception_finetune_biased_color.pkl")
    model_main=torch.load("./final_models/800_squeezenet_finetune_biased_shape.pkl")
   
    model = model_main['model']
    model.load_state_dict(model_main['model_state_dict'])
    # saliency_map = SmoothGrad(model, 'cuda:0')
    imagesList = os.listdir(path)
    model.eval()
    model.cuda()

    database_path = '../code/services/db.sqlite3'
    try:
        conn = sqlite3.connect(database_path, timeout=10)
    except Error as e:
        print(e)

    sql = '''INSERT INTO apiservice_images(
        ImageName,ModelName,Pred1Score,Pred2Score,Pred3Score,Pred1Label,Pred2Label,Pred3Label,Status)
                  VALUES(?,?,?,?,?,?,?,?,0) '''
    
    model_name = 'squeezenet_utensil_shape_bias'
    
    classes = dict((y,x) for x,y in model_main['classes'].items())
    for image in imagesList:
        img = PImage.open(path + image)
        data = data_transforms(img).unsqueeze(0)
        preds = model(data.cuda()).cpu()
        probs = F.softmax(preds, dim=1)
        probs5 = probs.topk(3)
        cls_probs = probs5[0][0].detach().numpy()
        cls_ids = probs5[1][0].detach().numpy()
        cls_labels = [classes[c] for c in cls_ids]
        temp = tuple(np.hstack(([image],[model_name],cls_probs,cls_labels)).ravel())
        print(temp)
        cur = conn.cursor()
        cur.execute(sql, temp)
        conn.commit()
        # break

if __name__ == "__main__":
    main()