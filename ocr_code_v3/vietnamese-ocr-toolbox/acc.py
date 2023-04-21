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
    img = cv2.imread(imgPath)
    pipeline = Pipeline(args, config)
    text = pipeline.startVietOcr(img)
    return text
    

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
    image = cv2.imread(imagePath)
    # results = reader.readtext(image)
    result = readerImage.readtext(image, detail = 0, paragraph=True)
    # print(result)
    return result

def checkLoop(textSource, textCompare, threshold):
    for text in textSource:
        lenTextCompare = len(textCompare.split(None))
        duplicate = 0
        for textCompare in textCompare.split(None):
            if(textCompare in text):
                duplicate+=1 
            if(duplicate/lenTextCompare > threshold):
                return True
    return False


def getData(textDetect, textSource):
    for text in textSource:
        lenTextDetect = len(textDetect.split(None))
        duplicate = 0
        for textDetect in textDetect.split(None):
            if(textDetect in text):
                duplicate+=1 
            if(duplicate/lenTextDetect > 0.5):
                return text
    return ''



def getAcc(numberModel):
    print("Start process with model number: ", numberModel)
    reader = csv.DictReader(open("/home/tuanna/Desktop/OCR/data/DBB.csv"))
    imageResult=[]
    for raw in reader:
        nameImage=raw['Ten_anh']
        documenType=raw['Loai_giay_to']
        busNumber=raw['Ma_so_DN']
        nameCompany=raw['Ten_cong_ty']
        addressCompany=raw['Dia_chi']
        phoneNumberCompany=raw['Dien_thoai']
        emailCompany=raw['Email']
        countTrue = 0

        if(nameImage in onlyfiles):
            # imageData=[]
            print("Start process image:", nameImage)
            if numberModel == 0:
                data = easyocrtest(mypath + nameImage)
            if numberModel == 1:
                data = vnOcrToolboxWithVietOcr(mypath + nameImage,config)
            if numberModel == 2:
                data = vnOcrToolboxWithTesseract(mypath + nameImage,config)

            if(checkLoop(data,nameCompany,0.8)):
                countTrue+=1
            if(checkLoop(data,documenType,0.8)):
                countTrue+=1
            if(checkLoop(data,busNumber,0.8)):
                countTrue+=1
            if(checkLoop(data,addressCompany,0.5)):
                countTrue+=1
            if(checkLoop(data,phoneNumberCompany,0.5)):
                countTrue+=1
            if(checkLoop(data,emailCompany,0.5)):
                countTrue+=1
            if(countTrue >= 4):
                imageResult.append(nameImage)
            # imageData.append(getData('Mã số doanh nghiệp',data))
            # imageData.append(getData('Tên công ty viết bằng tiếng việt',data))
            # imageData.append(getData('Điện thoại',data))
            # imageData.append(getData('Email',data))
            # print("End process image:", nameImage)
            # print(imageData)
    print("End process with model number: ", numberModel)
    return imageResult





imageResultEasyOcr=[]
imageResultToolboxWithVietOcr = []
imageResultToolboxWithTesseract = []
time1 = ''
time2 = ''
time3 = ''
for x in range(3):
    starttime = time.time()
    if x == 0:
        #call 1
        imageResultEasyOcr = getAcc(x)
        endtime = time.time()
        time1 = endtime - starttime
        print("Time process with model 1: ", time1)
    if x == 1:
        #call 2
        imageResultToolboxWithVietOcr = getAcc(x)
        endtime = time.time()
        time2 = endtime - starttime
        print("Time process with model 2: ", time2)
    if x == 2:
        #call 3
        imageResultToolboxWithTesseract = getAcc(x)
        endtime = time.time()
        time3 = endtime - starttime
        print("Time process with model 3: ", time2)


x = np.array(['EasyOcr','VietOcr','Tesseract'])
y = np.array([int(len(imageResultEasyOcr)),int(len(imageResultToolboxWithVietOcr)),int(len(imageResultToolboxWithTesseract))])
plt.xlabel('Model')
plt.title("Độ chính xác")
plt.ylabel('Number image')
plt.bar(x,y, width=0.5)
plt.savefig('acc.png')
plt.show()

y = np.array([time1,time2,time3])
plt.ylabel('Time Process (seconds)')
plt.title("Thời gian xử lý")
plt.bar(x,y, width=0.5)
plt.savefig('time_acc.png')
plt.show()



