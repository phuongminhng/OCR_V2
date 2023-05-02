import csv
import cv2
from os import listdir
from os.path import isfile, join
import easyocr
from tool.config import Config
import argparse
from run import Pipeline
import matplotlib.pyplot as plt
import numpy as np
import time
import pytesseract
import fastwer
import re

#load config
mypath ='/home/tuanna/Desktop/OCR/data/images/'
config = './tool/config/configs.yaml'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



def vnOcrToolboxWithVietOcr(imgPath,config):
    config = Config(config)
    #load param
    parser = argparse.ArgumentParser("vnOcrToolboxWithVietOcr")
    parser.add_argument("--input")
    parser.add_argument("--output", default="./results")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--do_retrieve", action="store_true")
    parser.add_argument("--find_best_rotation", action="store_true")
    args = parser.parse_args()
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite('cacheImageTesseract/cacheImage.png', img)
    img = cv2.imread('cacheImageTesseract/cacheImage.png')
    pipeline = Pipeline(args, config)
    text = pipeline.startVietOcr(img)
    return text

def processWithTesseract(imgPath):
    # save cacheImageTesseract
    image = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite('cacheImageTesseract/cacheImage.png', image)
    return pytesseract.image_to_string('cacheImageTesseract/cacheImage.png', lang = 'vie')
    

def vnOcrToolboxWithTesseract(imgPath,config):
    config = Config(config)
    #load param
    parser = argparse.ArgumentParser("vnOcrToolboxWithTesseractn")
    parser.add_argument("--input")
    parser.add_argument("--output", default="./results")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--do_retrieve", action="store_true")
    parser.add_argument("--find_best_rotation", action="store_true")
    args = parser.parse_args()
    img = cv2.imread(imgPath)
    pipeline = Pipeline(args, config)
    textv3 = pipeline.startTesseract(img)
    return textv3

def easyocrtest(imagePath):
    readerImage = easyocr.Reader(['vi'])
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
     # convert GRAY
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = readerImage.readtext(image, detail = 0, paragraph=True)
    print(result)
    return result


header = ['STT', 'Image', 'EasyOcr', 'Tesseract', 'VietOcr']
with open('dataDetect.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    stt = 0
    for nameImage in onlyfiles:
        data = []
        stt+=1
        data.append(stt)
        data.append(nameImage)
        print(nameImage)
        #EasyOCR
        data.append(easyocrtest(mypath + nameImage))
        #VietOcr
        data.append(vnOcrToolboxWithVietOcr(mypath + nameImage,config))
        #Tesseract
        data.append(processWithTesseract(mypath + nameImage))
        writer.writerow(data)






















