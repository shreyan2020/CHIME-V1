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

class SmoothGrad():
    """
    Compute smoothgrad 
    """

    def __init__(self, model, device='cpu', num_samples=100, std_spread=0.15):
        self.model = model
        self.num_samples = num_samples
        self.std_spread = std_spread
        self.device = 'cuda:0'
        

    def _getGradients(self, image, target_class=None):
        """
        Compute input gradients for an image
        """

        image = image.requires_grad_()
        self.model = self.model.to(self.device)
        out = self.model(image.to(self.device))
        # print(out)

        if target_class is None:
            target_class = out.data.max(1, keepdim=True)[1]
            target_class = target_class.flatten()

        loss = -1. * F.nll_loss(out, target_class, reduction='sum')

        self.model.zero_grad()
        # Gradients w.r.t. input and features
        input_gradient = torch.autograd.grad(outputs = loss, inputs = image, only_inputs=True)[0]

        return input_gradient

    def saliency(self, image, target_class=None):
        #SmoothGrad saliency
        
        self.model.eval()

        grad = self._getGradients(image, target_class=target_class)
        std_dev = self.std_spread * (image.max().item() - image.min().item())

        cam = torch.zeros_like(image).cuda()
        # add gaussian noise to image multiple times
        for i in tqdm(range(self.num_samples)):
            noise = torch.normal(mean = torch.zeros_like(image).to(self.device), std = std_dev).cuda()
            cam += (self._getGradients(image + noise, target_class=target_class)) / self.num_samples

        return cam.abs().sum(1, keepdim=True)
        
def save_saliency_map(image, saliency_map, filename):
    """ 
    Save saliency map on image.
    
    Args:
        image: Tensor of size (3,H,W)
        saliency_map: Tensor of size (1,H,W) 
        filename: string with complete path and file extension

    """

    image = image.data.cpu().numpy()
    saliency_map = saliency_map.data.cpu().numpy()

    saliency_map = saliency_map - saliency_map.min()
    saliency_map = saliency_map / saliency_map.max()
    saliency_map = saliency_map.clip(0,1)

    saliency_map = np.uint8(saliency_map * 255).transpose(1, 2, 0)
    saliency_map = cv2.resize(saliency_map, (224,224))

    image = np.uint8(image * 255).transpose(1,2,0)
    image = cv2.resize(image, (224, 224))

    # Apply JET colormap
    color_heatmap = cv2.applyColorMap(saliency_map, cv2.COLORMAP_JET)
    
    # Combine image with heatmap
    img_with_heatmap = np.float32(color_heatmap) + np.float32(image)
    img_with_heatmap = img_with_heatmap / np.max(img_with_heatmap)

    cv2.imwrite(filename, np.uint8(255 * img_with_heatmap))





def main():
    # path = '../data/dataset/single/'
    # model_name_or_path = 'google/vit-base-patch16-224-in21k'
    # feature_extractor = ViTFeatureExtractor.from_pretrained(model_name_or_path)
    # model_torch = ViTForImageClassification.from_pretrained("../../shreyan/notebooks/utensils",num_labels=16)
    # saliency_map = SmoothGrad(model_torch, 'cuda:0')
    # imagesList = os.listdir(path)
    # loadedImages = []
    # for image in imagesList:
    #     img = PImage.open(path + image)
    #     data = feature_extractor(img, return_tensors='pt')
    #     # print(type(data['pixel_values']))
    #     cam = saliency_map.saliency(data['pixel_values'].cuda())
    #     filename = pathlib.PurePath(path, image)
    #     # print(cam[0].shape,data['pixel_values'][0].shape)
    #     save_saliency_map(data['pixel_values'][0],cam[0],'../code/AnnotationScreen/src/assets/saliency/ppp_'+image)
    data_transforms = transforms.Compose([
        transforms.Resize(299),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    path = '../data/dataset/prod_run_saliency/'
    # path = '../data/dataset/prod_run_saliency_imageneta/'
    # imagenet = '3600_inception_finetune_imageneta.pkl'
    # squeeze_imagenet = 'best_squeezenet_finetune_imageneta.pkl'
    squeeze_shape = '800_squeezenet_finetune_biased_shape.pkl'
    squeeze_color = 'best_squeezenet_finetune_biased_color.pkl'
    squeeze_both = 'best_squeezenet_finetune_original.pkl'
    mapper = [{'model':squeeze_shape, 'folder':'squeezenet_utensil_shape_bias'},
              {'model':squeeze_color, 'folder':'squeezenet_utensil_color_bias'},
              {'model':squeeze_both, 'folder':'squeezenet_utensil_both_bias'}
             ]
    # model_main=torch.load("./final_models/1200_inception_finetune_biased_shape.pkl")
    
    for item in mapper:
        model_main = torch.load('./final_models/'+item['model'])
        model = model_main['model']
        model.load_state_dict(model_main['model_state_dict'])
        saliency_map = SmoothGrad(model, 'cuda:0')
        imagesList = os.listdir(path)
        for image in imagesList:
            img = PImage.open(path + image)
            data = data_transforms(img).unsqueeze(0)
            # print(data.shape)
            cam = saliency_map.saliency(data.cuda())
            # filename = pathlib.PurePath(path, image)
            # print(cam[0].shape,data['pixel_values'][0].shape)
            save_saliency_map(data[0],cam[0],'../data/dataset/sal_results_prod/'+item['folder']+'/ppp_'+image)


if __name__ == "__main__":
    main()