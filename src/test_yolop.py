from classes.yolop_model import YolopModel

model = YolopModel(weights='weights/End-to-end.pth', img_size=640, conf_thres=0.25, iou_thres=0.45, device='cpu', save_dir='inference/output')
model.process_image('images/main-qimg-e3fb8611e739c86330bc21ce1f50afe2-lq.jpg')