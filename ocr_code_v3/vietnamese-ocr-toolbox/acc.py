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
import Levenshtein

#load config
mypath ='/home/tuanna/Desktop/OCR/data/images/'
config = './tool/config/configs.yaml'
pathCacheImage = 'cacheImageTesseract/cacheImageGray.png'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def no_accent_vietnamese(s):
    # print("NO_ACCENT_VIETNAMESE",s)
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s


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
    cv2.imwrite(pathCacheImage, img)
    img = cv2.imread(pathCacheImage)
    pipeline = Pipeline(args, config)
    text = pipeline.startVietOcr(img)
    return text

def processWithTesseract(imgPath):
    # save cacheImageTesseract
    pathCache = ''
    image = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(pathCacheImage, image)
    return pytesseract.image_to_string(pathCacheImage, lang = 'vie')
    

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

def getDataCompany(text,nameModel):
    # textApp = []
    # textApp.append(text)
    loai_giay_to=''
    ma_so=''
    ten_cong_ty=''
    dia_chi_tru_so=''
    dien_thoai=''
    email=''
    date_register=''

    nameRep=''
    sexRep=''
    birthRep=''
    documentTypeRep=''
    documentNumberRep=''
    documentDateRep=''
    addressRep=''

    for line in text:
        lineNotUnicode = no_accent_vietnamese(line)
        # print("Not Unicode: ",line)
        print("------------------------------------------------")
        print(lineNotUnicode)
        if 'giay chung nhan dang ky' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('giay chung nhan dang ky')
            end_index = lineNotUnicode.lower().find('ma so doanh nghiep', start_index)
            loai_giay_to = line[start_index:end_index].strip()
            print('Loại giấy tờ:', loai_giay_to)
        if 'ma so doanh nghiep' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('ma so doanh nghiep')
            end_index = lineNotUnicode.lower().find('dang ky lan dau', start_index)
            ma_so = line[start_index+18:end_index].replace(":","").strip()
            print('Mã số doanh nghiệp:', ma_so)
        if 'dang ky lan dau' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('dang ky lan dau')
            date_register = line[start_index+17:start_index+17+25].strip()
            print('Ngày đăng ký:', date_register)
        if 'tieng viet' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('tieng viet')
            end_index = lineNotUnicode.lower().find('ten cong ty', start_index)
            ten_cong_ty = line[start_index+10:end_index].replace(":","").strip()
            print('Tên công ty:', ten_cong_ty)
        if 'tru so chinh' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('tru so chinh')
            end_index = lineNotUnicode.lower().find('dien thoai', start_index)
            dia_chi_tru_so = line[start_index+12:end_index].replace(":","").strip()
            print('Địa chỉ trụ sở chính:', dia_chi_tru_so)
        if 'dien thoai' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('dien thoai')
            end_index = lineNotUnicode.lower().find('fax', start_index)   
            dien_thoai = line[start_index+10:end_index].replace(":","").strip()
            print('Điện thoại:', dien_thoai)
        if 'email' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('email')
            end_index = lineNotUnicode.lower().find('website', start_index)
            email = line[start_index+5:end_index].replace(":","").strip()
            print('Email:',email)

        # thong tin nguoi dai dien
        if 'ho va ten' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('ho va ten')
            end_index = lineNotUnicode.lower().find('gioi tinh', start_index)
            nameRep = line[start_index+10:end_index].replace(":","").strip()
            print('Họ và tên:', nameRep)
        if 'gioi tinh' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('gioi tinh')
            end_index = lineNotUnicode.lower().find('chuc danh', start_index)
            sexRep = line[start_index+10:end_index].replace(":","").strip()
            print('Giới tính:', sexRep)
        if 'sinh ngay' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('sinh ngay')
            end_index = lineNotUnicode.lower().find('dan toc', start_index)
            birthRep = line[start_index+10:end_index].replace(":","").strip()
            print('Sinh ngày:', birthRep)
        if 'loai giay to phap ly' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('loai giay to phap ly')
            end_index = lineNotUnicode.lower().find('so giay to', start_index)
            documentTypeRep = line[start_index+33:end_index].replace(":","").strip()
            print('Loại giấy tờ:', documentTypeRep)
        if 'so giay to' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('so giay to')
            end_index = lineNotUnicode.lower().find('ngay cap', start_index)
            documentNumberRep = line[start_index+31:end_index].replace(":","").strip()
            print('Số giấy tờ:', documentNumberRep)
        if 'ngay cap' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('ngay cap')
            end_index = lineNotUnicode.lower().find('noi cap', start_index)
            documentDateRep = line[start_index+9:end_index].strip()
            print('Ngày cấp:', documentDateRep)
        if 'noi cap' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('noi cap')
            end_index = lineNotUnicode.lower().find('noi dang ky ho', start_index)
            addressRep = line[start_index+8:end_index].replace(":","").strip()
            print('Nơi cấp:',addressRep)
    # return (loai_giay_to,ma_so, ten_cong_ty, dia_chi_tru_so,dien_thoai,email)
    return (loai_giay_to,ma_so, ten_cong_ty, dia_chi_tru_so,dien_thoai,email,date_register,nameRep,sexRep,birthRep,documentTypeRep,documentNumberRep,documentDateRep,addressRep)

def getAcc(nameModel):
    print("Start process with model: ", nameModel)
    reader = csv.DictReader(open("/home/tuanna/Desktop/OCR/data/acc_v2.csv"))
    imageResult=[]
    werResultForImages = []
    cerResultForImages = []
    for raw in reader:
        nameImage=raw['Ten_anh']
        documenType=raw['Loai_giay_to']
        busNumber=raw['Ma_so_DN']
        nameCompany=raw['Ten_cong_ty']
        addressCompany=raw['Dia_chi']
        phoneNumberCompany=raw['Dien_thoai']
        emailCompany=raw['Email']

        dateRegister=raw['Ngay_dang_ki']
        nameRep=raw['Nguoi_dai_dien']
        sexRep=raw['Gioi_tinh']
        birthRep=raw['Ngay_sinh']
        documentTypeRep=raw['Loai_giay_to_ca_nhan']
        documentNumberRep=raw['So_giay_to']
        documentDateRep=raw['Ngay_cap']
        addressRep=raw['Noi_cap']

        dataReference = []
        dataOutput = []
        werResultForImage = []
        cerResultForImage = []
        dataReference.append(documenType)
        dataReference.append(busNumber)
        dataReference.append(nameCompany)
        dataReference.append(addressCompany)
        dataReference.append(phoneNumberCompany)
        dataReference.append(emailCompany)

        dataReference.append(dateRegister)
        dataReference.append(nameRep)
        dataReference.append(sexRep)
        dataReference.append(birthRep)
        dataReference.append(documentTypeRep)
        dataReference.append(documentNumberRep)
        dataReference.append(documentDateRep)
        dataReference.append(addressRep)

        dataFinal = ''
        if(nameImage in onlyfiles):
            # imageData=[]
            print("Start process image:", nameImage)
            if nameModel in "EasyOcr":
                data = easyocrtest(mypath + nameImage)
                dataOutput = getDataCompany(data,nameModel)
            if nameModel in "VietOcr":
                data = vnOcrToolboxWithVietOcr(mypath + nameImage,config)
                for data1 in data:
                    dataFinal = dataFinal + ' ' + data1
                print("DATA VietOcr: ", dataFinal)
                dataGet = []
                dataGet.append(dataFinal)
                dataOutput = getDataCompany(dataGet,nameModel)
            if nameModel in "Tesseract":
                data = processWithTesseract(mypath + nameImage)
                dataGet = []
                dataGet.append(data)
                dataOutput = getDataCompany(dataGet,nameModel)
        for i in range(len(dataReference)):
            werResultForImage.append(wer(dataReference[i],dataOutput[i]))
            cerResultForImage.append(cer(dataReference[i],dataOutput[i]))
        imageResult.append(nameImage)
        werResultForImages.append(werResultForImage)
        cerResultForImages.append(cerResultForImage)
    print("End process with model: ", nameModel)
    return imageResult, werResultForImages, cerResultForImages

def chartAccuracy(listImage,werWithModelFirst, werWithModelSecond,
    werWithModelThirt,nameChart, ylabel):
    # print(listImage)
    numberImage = []
    for i in range(int(len(listImage))):
        numberImage.append(i+1)
    print(numberImage)
    print(werWithModelFirst)
    plt.plot(numberImage, werWithModelFirst, color='green', marker='o', linestyle='solid')
    plt.plot(numberImage, werWithModelSecond, color='red', marker='o', linestyle='solid')
    plt.plot(numberImage, werWithModelThirt, color='blue', marker='o', linestyle='solid')
    plt.title(ylabel + '-' + nameChart)
    plt.ylabel(ylabel + '(%)')
    plt.xlabel("Number Image")
    plt.legend(['EasyOcr','VietOcr','Tesseract'])
    plt.savefig('resultAcc/'+ no_accent_vietnamese(ylabel+ '-' + nameChart)+'.png')
    plt.show()

def wer(ref, hyp):
    if ref in '':
        return 0.0
    # Tách các từ trong văn bản
    ref = ref.split()
    hyp = hyp.split()
    if len(ref) < len(hyp):
        hyp = hyp[:len(ref)]
    # Khởi tạo ma trận lỗi
    matrix = [[0 for x in range(len(hyp) + 1)] for y in range(len(ref) + 1)]
    
    # Điền giá trị ban đầu vào ma trận
    for i in range(len(ref) + 1):
        for j in range(len(hyp) + 1):
            if i == 0:
                matrix[i][j] = j
            elif j == 0:
                matrix[i][j] = i
    # Tính giá trị cho ma trận
    for i in range(1, len(ref) + 1):
        for j in range(1, len(hyp) + 1):
            if ref[i - 1] == hyp[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                substitute = matrix[i - 1][j - 1] + 1 #2
                insert = matrix[i][j - 1] + 1 #0
                delete = matrix[i - 1][j] + 1 
                matrix[i][j] = min(substitute, insert, delete)
    wer = (matrix[len(ref)][len(hyp)]) / len(ref)
    print("Text reference: ", ref)
    print("Text output: ", hyp)
    print("WER: {:.2%}".format(wer))
    print("-------------END-------------- ")
    
    return wer

def cer(reference, hypothesis):
    if len(reference) == 0 :
        return 0.0
    # print("reference: ",reference)
    # Cut the longer string to the length of the shorter string
    reference_cut, hypothesis_cut = cut_strings_to_same_length(reference, hypothesis)

    # Calculate the Levenshtein distance between the two strings
    distance = Levenshtein.distance(reference_cut, hypothesis_cut)
    # Calculate the CER
    cer = distance / len(reference_cut)

    print("Text reference: ", reference_cut)
    print("Text output: ", hypothesis_cut)
    print("CER: {:.2%}".format(cer))
    print("-------------END-------------- ")
    return cer

def cut_strings_to_same_length(reference, hypothesis):
    # Get the lengths of the reference and hypothesis
    ref_len = len(reference)
    hyp_len = len(hypothesis)

    # If the reference is shorter than the hypothesis, swap them
    if ref_len < hyp_len:
        hypothesis = hypothesis[:ref_len]

    return reference, hypothesis

def calculate_average(data):
    dataAverage= []
    for i in range(len(data)):
        z =0
        for x in data[i]:
            z=z+x
        dataAverage.append(z/len(data[i]))
    return dataAverage


def accAverage(easyOcr,vietOcr,tesseract,label):
    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))
    # listFills = ["Loại Giấy Tờ","Mã Số Doanh Nghiệp", "Tên Công Ty", "Địa Chỉ", "Số Điện Thoại", "Email"]
    listFills = ["Loại Giấy Tờ","Mã Số Doanh Nghiệp", "Tên Công Ty", "Địa Chỉ", "Số Điện Thoại", "Email","Ngày đăng ký", "Tên người đại diên", "Giới tính", "Ngày sinh", "Loại giấy tờ", "Số giấy tờ", "Ngày đăng ký giấy tờ", "Địa chỉ người đại diện"]
    # set height of bar
    easyOcrAverage = calculate_average(easyOcr)
    vietOcrAverage = calculate_average(vietOcr)
    tesseractAverage = calculate_average(tesseract)
    
    # Set position of bar on X axis
    br1 = np.arange(len(easyOcr))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    
    # Make the plot
    plt.bar(br1, easyOcrAverage, color ='r', width = barWidth,
            edgecolor ='grey', label ='EasyOcr')
    plt.bar(br2, vietOcrAverage, color ='g', width = barWidth,
            edgecolor ='grey', label ='vietOcr')
    plt.bar(br3, tesseractAverage, color ='b', width = barWidth,
            edgecolor ='grey', label ='tesseract')
    
    # Adding Xticks
    # plt.xlabel('Branch', fontweight ='bold', fontsize = 15)
    plt.ylabel(label + '(%)', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(easyOcrAverage))],
            listFills)
    
    plt.legend()
    plt.savefig('resultAcc/' + label+'.png')
    plt.show()


def calculate_average_v2(data):
    dataAverage= []
    for i in range(len(data)):
        z =0
        for x in data[i]:
            z=z+x
        dataAverage.append(z*100/len(data[i]))
    return dataAverage

def accAverage_V2(easyOcr,vietOcr,tesseract,label):
    print("easyOcr: ",easyOcr)
    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))
    # listFills = ["Loại Giấy Tờ","Mã Số Doanh Nghiệp", "Tên Công Ty", "Địa Chỉ", "Số Điện Thoại", "Email"]
    listFills = ["Loại Giấy Tờ","Mã Số Doanh Nghiệp", "Tên Công Ty", "Địa Chỉ", "Số Điện Thoại", "Email","Ngày đăng ký", "Tên người đại diên", "Giới tính", "Ngày sinh", "Loại giấy tờ", "Số giấy tờ", "Ngày đăng ký giấy tờ", "Địa chỉ người đại diện"]
    xlabel = []
    for i in range(len(easyOcr)):
        xlabel.append(i+1)
    # set height of bar
    easyOcrAverage = calculate_average_v2(easyOcr)
    vietOcrAverage = calculate_average_v2(vietOcr)
    tesseractAverage = calculate_average_v2(tesseract)

    print("easyOcrAverage: ", easyOcrAverage)
    print("vietOcrAverage: ", vietOcrAverage)
    print("tesseractAverage: ", tesseractAverage)

    get_Acc_all(easyOcrAverage,vietOcrAverage,tesseractAverage,label)
    # Set position of bar on X axis
    br1 = np.arange(len(easyOcr))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    
    # Make the plot
    plt.bar(br1, easyOcrAverage, color ='r', width = barWidth,
            edgecolor ='grey', label ='EasyOcr')
    plt.bar(br2, vietOcrAverage, color ='g', width = barWidth,
            edgecolor ='grey', label ='VietOcr')
    plt.bar(br3, tesseractAverage, color ='b', width = barWidth,
            edgecolor ='grey', label ='Tesseract')
    
    # Adding Xticks
    plt.xlabel('Number Image', fontweight ='bold', fontsize = 15)
    plt.ylabel(label + '(%)', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(easyOcrAverage))],
            xlabel)
    
    plt.legend()
    plt.savefig('resultAcc/' + label+'.png')
    plt.show()

def get_Acc_all(easyOcrAverage,vietOcrAverage,tesseractAverage,titel):
    x = np.array(['EasyOcr','VietOcr','Tesseract'])
    easyOcr=0.0
    vietOcr=0.0
    tesseract=0.0
    for i in easyOcrAverage:
        easyOcr = easyOcr + i
    easyOcr = easyOcr/len(easyOcrAverage)
    for i in vietOcrAverage:
        vietOcr = vietOcr + i
    vietOcr = vietOcr/len(vietOcrAverage)
    for i in tesseractAverage:
        tesseract = tesseract + i
    tesseract = tesseract/len(tesseractAverage)

    y = np.array([easyOcr,vietOcr,tesseract])
    plt.ylabel(titel + '(%)')
    plt.title(titel + ' All Images')
    plt.bar(x,y, width=0.5)
    plt.savefig('resultAcc/' + titel + 'allImage.png')
    plt.show()


# listModel = ["VietOcr","Tesseract"]
listModel = ["EasyOcr","Tesseract","VietOcr"]
imageResultEasyOcr=[]
imageResultToolboxWithVietOcr = []
imageResultToolboxWithTesseract = []
werEasyOcrResultForImages= []
werTesseractResultForImages= []
werVietOcrResultForImages= []
cerEasyOcrResultForImages= []
cerTesseractResultForImages= []
cerVietOcrResultForImages= []
time1 = ''
time2 = ''
time3 = ''
for x in listModel:
    starttime = time.time()
    if x in "EasyOcr":
        imageResultEasyOcr,werEasyOcrResultForImages,cerEasyOcrResultForImages = getAcc(x)
        endtime = time.time()
        time1 = endtime - starttime
        print("Time process with EasyOcr model: ", time1)
    if x in "VietOcr":
        imageResultToolboxWithVietOcr,werVietOcrResultForImages,cerVietOcrResultForImages = getAcc(x)
        endtime = time.time()
        time2 = endtime - starttime
        print("Time process with VietOcr model: ", time2)
    if x in "Tesseract":
        imageResultToolboxWithTesseract,werTesseractResultForImages,cerTesseractResultForImages = getAcc(x)
        endtime = time.time()
        time3 = endtime - starttime
        print("Time process with Tesseract model: ", time2)
listFills = ["Loại Giấy Tờ","Mã Số Doanh Nghiệp", "Tên Công Ty", "Địa Chỉ", "Số Điện Thoại", "Email","Ngày đăng ký", "Tên người đại diên", "Giới tính", "Ngày sinh", "Loại giấy tờ", "Số giấy tờ", "Ngày đăng ký giấy tờ", "Địa chỉ người đại diện"]
countFill=0

werAverageEasyOcr = []
werAverageTesseract = []
werAverageVietOcr = []
cerAverageEasyOcr = []
cerAverageTesseract = []
cerAverageVietOcr = []

for fill in listFills:
    werEasyOcr = []
    werTesseract = []
    werVietOcr = []
    cerEasyOcr = []
    cerTesseract = []
    cerVietOcr = []
    for i in range(int(len(imageResultEasyOcr))):
        werEasyOcr.append(werEasyOcrResultForImages[i][countFill]*100)
        werTesseract.append(werTesseractResultForImages[i][countFill]*100)
        werVietOcr.append(werVietOcrResultForImages[i][countFill]*100)

        cerEasyOcr.append(cerEasyOcrResultForImages[i][countFill]*100)
        cerTesseract.append(cerTesseractResultForImages[i][countFill]*100)
        cerVietOcr.append(cerVietOcrResultForImages[i][countFill]*100)
    
    # set data
    werAverageEasyOcr.append(werEasyOcr)
    werAverageTesseract.append(werTesseract)
    werAverageVietOcr.append(werVietOcr)
    cerAverageEasyOcr.append(cerEasyOcr)
    cerAverageTesseract.append(cerTesseract)
    cerAverageVietOcr.append(cerVietOcr)


    chartAccuracy(imageResultEasyOcr,werEasyOcr,
    werVietOcr,werTesseract,fill,"WER")

    chartAccuracy(imageResultEasyOcr,cerEasyOcr,
    cerVietOcr,cerTesseract,fill, "CER")
    countFile += 1

#get acc average wer
# accAverage(werAverageEasyOcr,werAverageTesseract,werAverageVietOcr,"WER-Average")
# #get acc average cer
# accAverage(cerAverageEasyOcr,cerAverageTesseract,cerAverageVietOcr,"CER-Average")

#get acc v2:
accAverage_V2(werEasyOcrResultForImages,werTesseractResultForImages,werVietOcrResultForImages,"WER-Average")
accAverage_V2(cerEasyOcrResultForImages,cerTesseractResultForImages,cerVietOcrResultForImages,"CER-Average")



x = np.array(['EasyOcr','VietOcr','Tesseract'])
y = np.array([time1,time2,time3])
plt.ylabel('Time Process (seconds)')
plt.title("Thời gian xử lý")
plt.bar(x,y, width=0.5)
plt.savefig('resultAcc/time_acc.png')
plt.show()

