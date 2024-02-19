import torch
import cv2
import os
import shutil
import numpy as np
from pathlib import Path
import torchvision.transforms as transforms
from numpy import random
from lib.core.general import non_max_suppression, scale_coords
from lib.utils.utils import create_logger, select_device, time_synchronized
import PIL.Image as image
from lib.config import cfg
from lib.models import get_net
from lib.dataset import LoadImages, LoadStreams
from tqdm import tqdm
from lib.utils import plot_one_box,show_seg_result
from lib.core.postprocess import morphological_process, connect_lane


class YolopModel:
    def __init__(self, weights, img_size=640, conf_thres=0.25, iou_thres=0.45, device='cpu', save_dir='inference/output'):
        self.weights = weights
        self.img_size = img_size
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.save_dir = save_dir
        self.device = select_device(device = device)
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA
        self.model = self.load_model()
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def load_model(self):
        model = get_net(cfg)  # Assuming get_net is a function that returns your model's architecture
        checkpoint = torch.load(self.weights, map_location=self.device)  # Load the model weights
        model.load_state_dict(checkpoint['state_dict'])
        model.to(self.device)
        if self.half:
            model.half()  # Convert model to half precision if using a CUDA device
        model.eval()  # Set the model to evaluation mode
        return model

    def detect(self, image):
        # Prepare the image
        img_original = img.copy()  # Keep an original copy for scaling results back
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        img = image.fromarray(img)  # Convert to PIL image
        img_transformed = self.transform(img).to(self.device)  # Apply transformations
        img_transformed = img_transformed.half() if self.half else img_transformed.float()  # uint8 to fp16/32
        img_transformed = img_transformed.unsqueeze(0)  # Add batch dimension

        # Inference
        with torch.no_grad():  # Inference without gradient calculation
            det_out, da_seg_out, ll_seg_out = self.model(img_transformed)

        # Process detection output
        inf_out, _ = det_out
        det_pred = non_max_suppression(inf_out, conf_thres=self.conf_thres, iou_thres=self.iou_thres, classes=None, agnostic=False)
        det = det_pred[0]

        detections = []
        if len(det):
            det[:, :4] = scale_coords(img_transformed.shape[2:], det[:, :4], img_original.shape[:2]).round()
            for *xyxy, conf, cls in reversed(det):
                label = f'{self.model.names[int(cls)]} {conf:.2f}'
                box = [coord.item() for coord in xyxy]  # Convert tensor to list
                detections.append({'box': box, 'label': label, 'confidence': conf.item(), 'class': cls.item()})

        # Process segmentation output
        # Assuming da_seg_out and ll_seg_out are segmentation masks, convert them to numpy arrays.
        # This example assumes the output is a single channel mask, you might need to adjust based on your model output.
        da_seg_mask = da_seg_out.squeeze().cpu().numpy()
        ll_seg_mask = ll_seg_out.squeeze().cpu().numpy()

        # Post-process segmentation masks if necessary (e.g., thresholding, morphological operations)
        # Example: Convert segmentation logits to binary mask (you may need to adjust this based on your model's output)
        da_seg_mask = (da_seg_mask > 0.5).astype(np.uint8)  # Dummy thresholding example
        ll_seg_mask = (ll_seg_mask > 0.5).astype(np.uint8)  # Dummy thresholding example

        # Return both detections and segmentation data
        return {
            'detections': detections,
            'da_seg_mask': da_seg_mask,
            'll_seg_mask': ll_seg_mask
        }

    def process_image(self, image_path):
        # clear the output directory
        if os.path.exists(self.save_dir):  # output dir
            shutil.rmtree(self.save_dir)  # delete dir
        os.makedirs(self.save_dir)  # make new dir

        # Load the image
        dataset = LoadImages(image_path, img_size=self.img_size)
        bs = 1  # batch_size

        # Get names and colors
        names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

        vid_path, vid_writer = None, None
        img = torch.zeros((1, 3, self.img_size, self.img_size), device=self.device)  # init img
        _ = self.model(img.half() if self.half else img) if self.device.type != 'cpu' else None  # run once
        
        for i, (path, img, img_det, vid_cap,shapes) in tqdm(enumerate(dataset),total = len(dataset)):
            img = self.transform(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
            
            # Inference
            det_out, da_seg_out,ll_seg_out= self.model(img)
            
            #     print(det_out)
            inf_out, _ = det_out

            # Apply NMS
            det_pred = non_max_suppression(inf_out, conf_thres=self.conf_thres, iou_thres=self.iou_thres, classes=None, agnostic=False)

            det=det_pred[0]

            save_path = str(self.save_dir +'/'+ Path(path).name) if dataset.mode != 'stream' else str(self.save_dir + '/' + "web.mp4")

            _, _, height, width = img.shape
            h,w,_=img_det.shape
            pad_w, pad_h = shapes[1][1]
            pad_w = int(pad_w)
            pad_h = int(pad_h)
            ratio = shapes[1][0][1]

            da_predict = da_seg_out[:, :, pad_h:(height-pad_h),pad_w:(width-pad_w)]
            da_seg_mask = torch.nn.functional.interpolate(da_predict, scale_factor=int(1/ratio), mode='bilinear')
            _, da_seg_mask = torch.max(da_seg_mask, 1)
            da_seg_mask = da_seg_mask.int().squeeze().cpu().numpy()
            da_seg_mask = morphological_process(da_seg_mask, kernel_size=7)

            
            ll_predict = ll_seg_out[:, :,pad_h:(height-pad_h),pad_w:(width-pad_w)]
            ll_seg_mask = torch.nn.functional.interpolate(ll_predict, scale_factor=int(1/ratio), mode='bilinear')
            _, ll_seg_mask = torch.max(ll_seg_mask, 1)
            ll_seg_mask = ll_seg_mask.int().squeeze().cpu().numpy()
            # Lane line post-processing
            ll_seg_mask = morphological_process(ll_seg_mask, kernel_size=7, func_type=cv2.MORPH_OPEN)
            ll_seg_mask = connect_lane(ll_seg_mask)

            img_det = show_seg_result(img_det, (da_seg_mask, ll_seg_mask), _, _, is_demo=True)

            if len(det):
                det[:,:4] = scale_coords(img.shape[2:],det[:,:4],img_det.shape).round()
                for *xyxy,conf,cls in reversed(det):
                    label_det_pred = f'{names[int(cls)]} {conf:.2f}'
                    plot_one_box(xyxy, img_det , label=label_det_pred, color=colors[int(cls)], line_thickness=2)
            
            cv2.imwrite(save_path,img_det)