import json
from flask import Flask, request, jsonify
from PIL import Image
import os
from werkzeug.utils import secure_filename
from ocrErry import main
import easyocr
import time
import cv2
import re
from tool.config import Config
import argparse
from werkzeug.utils import secure_filename
from run import Pipeline
import pytesseract

mypath ='/home/tuanna/Desktop/OCR/data/images/'
config = './tool/config/configs.yaml'
pathCacheImage = 'fileUpload/cacheImage/cacheImage.png'


app = Flask(__name__)
UPLOAD_FOLDER = "fileUpload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENTIONS = set(['png', 'jpg', 'jpeg'])
app.secret_key = 'secret'
def easyocrFunction(imagePath):
    readerImage = easyocr.Reader(['vi'])
    image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    result = readerImage.readtext(image, detail = 0, paragraph=True)
    print(result)
    return result
def processWithTesseract(imgPath):
    # save cacheImageTesseract
    image = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(pathCacheImage, image)
    return pytesseract.image_to_string(pathCacheImage, lang = 'vie')

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

def no_accent_vietnamese(s):
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
def getDataCompany(text):
    loai_giay_to=''
    ma_so=''
    ten_cong_ty=''
    dia_chi_tru_so=''
    dien_thoai=''
    email=''
    date_register=''
    for line in text:
        lineNotUnicode = no_accent_vietnamese(line)
        print("------------------------------------------------")
        print(line)
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
    return (loai_giay_to,ma_so, ten_cong_ty, dia_chi_tru_so,dien_thoai,email,date_register)



def getDataRep(text):
    nameRep=''
    sexRep=''
    birthRep=''
    documentTypeRep=''
    documentNumberRep=''
    documentDateRep=''
    addressRep=''
    for line in text:
        lineNotUnicode = no_accent_vietnamese(line)
        print("------------------------------------------------")
        print(line)
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
    return (nameRep,sexRep, birthRep, documentTypeRep,documentNumberRep,documentDateRep,addressRep)


@app.route('/getData', methods=["POST"])
def index():
    image = request.files['image']
    nameModel = request.form['model']

    print(image)
    if image :
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        img_src = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        if nameModel :
            if nameModel.lower() in 'vietocr':
                data = vnOcrToolboxWithVietOcr(img_src,config)
                dataFinal = ''
                for data1 in data:
                    dataFinal = dataFinal + ' ' + data1
                dataGet = []
                dataGet.append(dataFinal)
                print(dataGet)
                (documenType, busNumber, nameCompany, addressCompany, phoneNumberCompany, emailCompany,dateRegister) = getDataCompany(dataGet)
                (nameRep,sexRep, birthRep, documentTypeRep,documentNumberRep,documentDateRep,addressRep) = getDataRep(dataGet)

                return jsonify({'Status': 'Success','Model':'vietOcr', 'data': [{'documenType' : documenType, 'busNumber' : busNumber,'nameCompany':nameCompany,
                'addressCompany': addressCompany, 'phoneNumberCompany': phoneNumberCompany, 'emailCompany': emailCompany, 'dateRegister': dateRegister,
                'nameRep': nameRep, 'sexRep': sexRep, 'birthRep':birthRep, 'documentTypeRep':documentTypeRep, 'documentNumberRep': documentNumberRep,
                'documentDateRep': documentDateRep,'addressRep':addressRep}]})
            elif nameModel.lower() in 'tesseract':
                data = processWithTesseract(img_src)
                dataGet = []
                dataGet.append(data)
                (documenType, busNumber, nameCompany, addressCompany, phoneNumberCompany, emailCompany,dateRegister) = getDataCompany(dataGet)
                (nameRep,sexRep, birthRep, documentTypeRep,documentNumberRep,documentDateRep,addressRep) = getDataRep(dataGet)


                return jsonify({'Status': 'Success','Model':'Tesseract', 'data': [{'documenType' : documenType, 'busNumber' : busNumber,'nameCompany':nameCompany,
                'addressCompany': addressCompany, 'phoneNumberCompany': phoneNumberCompany, 'emailCompany': emailCompany, 'dateRegister': dateRegister,
                'nameRep': nameRep, 'sexRep': sexRep, 'birthRep':birthRep, 'documentTypeRep':documentTypeRep, 'documentNumberRep': documentNumberRep,
                'documentDateRep': documentDateRep,'addressRep':addressRep}]})
            elif nameModel.lower() in 'easyocr':
                data = easyocrFunction(img_src)
                (documenType, busNumber, nameCompany, addressCompany, phoneNumberCompany, emailCompany,dateRegister) = getDataCompany(data)
                (nameRep,sexRep, birthRep, documentTypeRep,documentNumberRep,documentDateRep,addressRep) = getDataRep(data)


                return jsonify({'Status': 'Success', 'Model':'EasyOcr', 'data': [{'documenType' : documenType, 'busNumber' : busNumber,'nameCompany':nameCompany,
                'addressCompany': addressCompany, 'phoneNumberCompany': phoneNumberCompany, 'emailCompany': emailCompany, 'dateRegister': dateRegister,
                'nameRep': nameRep, 'sexRep': sexRep, 'birthRep':birthRep, 'documentTypeRep':documentTypeRep, 'documentNumberRep': documentNumberRep,
                'documentDateRep': documentDateRep,'addressRep':addressRep}]})
            else:
                return jsonify({'Status': 'ERROR', 'Message':'Không tồn tại mô hình '+ nameModel})
        else: 
            return jsonify({'Status': 'ERROR', 'Message':'Mô hình không được để trống'})
    return jsonify({'Status': 'ERROR', 'Message':'Bạn chưa nhập thông tin file hình ảnh'})

app.run()