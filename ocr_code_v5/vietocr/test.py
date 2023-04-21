from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg


config = Cfg.load_config_from_name('vgg_transformer') 
config['weights'] = '/home/tuanna/Desktop/OCR/ocr_code_v3/vietnamese-ocr-toolbox/weights/transformerocr.pth'
config['device'] = 'cpu' 

detector = Predictor(config)

img = '/home/tuanna/Desktop/OCR/data/GPKD_1.jpg'
img = Image.open(img)
# dự đoán 
s = detector.predict(img, return_prob=False) 

















