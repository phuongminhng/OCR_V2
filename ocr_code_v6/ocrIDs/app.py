from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from ocrErry import main
import easyocr
import time
import cv2
import re
from tool.config import Config
import argparse
from run import Pipeline

# from tool.config import Config
# import argparse
# from run import Pipeline


#load config
mypath ='/home/tuanna/Desktop/OCR/data/images/'
config = './tool/config/configs.yaml'
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
    texts = pipeline.startVietOcr(img)
    return texts
    

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

def easyocrFunction(imagePath):
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
def join_strings(strings):
    result = ''
    for s in strings:
        result += ' ' + s
    return result
def join_strings_better(strings):
    return ' '.join(strings)

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
            loai_giay_to = line
            print('Loại giấy tờ:', loai_giay_to)
        if 'ma so doanh nghiep' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('ma so doanh nghiep')
            end_index = lineNotUnicode.lower().find('dang ky lan dau', start_index)
            ma_so = line[start_index+20:end_index].strip()
            print('Mã số doanh nghiệp:', ma_so)
        if 'dang ky lan dau' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('dang ky lan dau')
            date_register = line[start_index+17:start_index+17+25].strip()
            print('Ngày đăng ký:', date_register)
        if 'tieng viet' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('tieng viet')
            end_index = lineNotUnicode.lower().find('ten cong ty', start_index)
            ten_cong_ty = line[start_index+12:end_index].strip()
            print('Tên công ty:', ten_cong_ty)
        if 'tru so chinh' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('tru so chinh')
            end_index = lineNotUnicode.lower().find('dien thoai', start_index)
            dia_chi_tru_so = line[start_index+14:end_index].strip()
            print('Địa chỉ trụ sở chính:', dia_chi_tru_so)
        if 'dien thoai' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('dien thoai')
            end_index = lineNotUnicode.lower().find('fax', start_index)
            dien_thoai = line[start_index+12:end_index].strip()
            print('Điện thoại:', dien_thoai)
        if 'email' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('email')
            end_index = lineNotUnicode.lower().find('website', start_index)
            email = line[start_index+6:end_index].strip()
            print('Email:',email)
    return (loai_giay_to,ma_so, ten_cong_ty, dia_chi_tru_so,dien_thoai,email,date_register)

def getDataCompanyWithUnicode(text):
    loai_giay_to=''
    ma_so=''
    ten_cong_ty=''
    dia_chi_tru_so=''
    dien_thoai=''
    email=''
    date_register=''
    for line in text:
        print("------------------------------------------------")
        print(line)
        if 'giấy chứng nhận đăng ký' in line.lower():
            loai_giay_to = line
            print('Loại giấy tờ:', loai_giay_to)
        if 'mã số doanh nghiệp' in line.lower():
            start_index = line.find('Mã số doanh nghiệp')
            end_index = line.find('Đăng ký lần đầu', start_index)
            ma_so = line[start_index+20:end_index].strip()
            print('Mã số doanh nghiệp:', ma_so)
        if 'đăng ký lần đầu' in line.lower():
            start_index = line.lower().find('đăng ký lần đầu')
            date_register = line[start_index+17:start_index+17+25].strip()
            print('Ngày đăng ký:', date_register)
        if 'tiếng việt' in line.lower():
            start_index = line.lower().find('tiếng việt')
            end_index = line.find('Tên công ty viết bằng tiếng nước ngoài', start_index)
            ten_cong_ty = line[start_index+12:end_index].strip()
            print('Tên công ty:', ten_cong_ty)
        if 'trụ sở chính:' in line.lower():
            start_index = line.lower().find('trụ sở chính:')
            end_index = line.find('Điện thoại', start_index)
            dia_chi_tru_so = line[start_index+14:end_index].strip()
            print('Địa chỉ trụ sở chính:', dia_chi_tru_so)
        if 'điện thoại' in line.lower():
            start_index = line.lower().find('điện thoại:')
            end_index = line.find('Fax', start_index)
            dien_thoai = line[start_index+12:end_index].strip()
            print('Điện thoại:', dien_thoai)
        if 'email' in line.lower():
            start_index = line.lower().find('email')
            end_index = line.find('Website', start_index)
            email = line[start_index+6:end_index].strip()
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
            nameRep = line[start_index+11:end_index].strip()
            print('Họ và tên:', nameRep)
        if 'gioi tinh' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('gioi tinh')
            end_index = lineNotUnicode.lower().find('chuc danh', start_index)
            sexRep = line[start_index+11:end_index].strip()
            print('Giới tính:', sexRep)
        if 'sinh ngay' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('sinh ngay')
            end_index = lineNotUnicode.lower().find('dan toc', start_index)
            birthRep = line[start_index+11:end_index].strip()
            print('Sinh ngày:', birthRep)
        if 'loai giay to phap ly' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('loai giay to phap ly')
            end_index = lineNotUnicode.lower().find('so giay to', start_index)
            documentTypeRep = line[start_index+34:end_index].strip()
            print('Loại giấy tờ:', documentTypeRep)
        if 'so giay to' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('so giay to')
            end_index = lineNotUnicode.lower().find('ngay cap', start_index)
            documentNumberRep = line[start_index+32:end_index].strip()
            print('Số giấy tờ:', documentNumberRep)
        if 'ngay cap' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('ngay cap')
            end_index = lineNotUnicode.lower().find('noi cap', start_index)
            documentDateRep = line[start_index+10:end_index].strip()
            print('Ngày cấp:', documentDateRep)
        if 'noi cap' in lineNotUnicode.lower():
            start_index = lineNotUnicode.lower().find('noi cap')
            end_index = lineNotUnicode.lower().find('noi dang ky ho', start_index)
            addressRep = line[start_index+9:end_index].strip()
            print('Nơi cấp:',addressRep)
    return (nameRep,sexRep, birthRep, documentTypeRep,documentNumberRep,documentDateRep,addressRep)

def getDataRepWithUnicode(text):
    nameRep=''
    sexRep=''
    birthRep=''
    documentTypeRep=''
    documentNumberRep=''
    documentDateRep=''
    addressRep=''
    for line in text:
        print("------------------------------------------------")
        print(line)
        if 'họ và tên' in line.lower():
            start_index = line.lower().find('họ và tên')
            end_index = line.lower().find('giới tính', start_index)
            nameRep = line[start_index+11:end_index].strip()
            print('Họ và tên:', nameRep)
        if 'giới tính' in line.lower():
            start_index = line.lower().find('giới tính')
            end_index = line.lower().find('chức danh', start_index)
            sexRep = line[start_index+11:end_index].strip()
            print('Giới tính:', sexRep)
        if 'sinh ngày' in line.lower():
            start_index = line.lower().find('sinh ngày')
            end_index = line.lower().find('dân tộc', start_index)
            birthRep = line[start_index+11:end_index].strip()
            print('Sinh ngày:', birthRep)
        if 'loại giấy tờ pháp lý' in line.lower():
            start_index = line.lower().find('loại giấy tờ pháp lý')
            end_index = line.lower().find('số giấy tờ', start_index)
            documentTypeRep = line[start_index+34:end_index].strip()
            print('Loại giấy tờ:', documentTypeRep)
        if 'số giấy tờ' in line.lower():
            start_index = line.lower().find('số giấy tờ')
            end_index = line.lower().find('ngày cấp', start_index)
            documentNumberRep = line[start_index+32:end_index].strip()
            print('Số giấy tờ:', documentNumberRep)
        if 'ngày cấp' in line.lower():
            start_index = line.lower().find('ngày cấp')
            end_index = line.lower().find('nơi cấp', start_index)
            documentDateRep = line[start_index+10:end_index].strip()
            print('Ngày cấp:', documentDateRep)
        if 'nơi cấp' in line.lower():
            start_index = line.lower().find('nơi cấp')
            end_index = line.lower().find('nơi đăng ký hộ', start_index)
            addressRep = line[start_index+9:end_index].strip()
            print('Nơi cấp:',addressRep)
    return (nameRep,sexRep, birthRep, documentTypeRep,documentNumberRep,documentDateRep,addressRep)



app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = "static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENTIONS = set(['png', 'jpg', 'jpeg'])
app.secret_key = 'secret'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":

        image = request.files['file']
        #Thông tin cần lấy
        # documenTypeBoolean = (request.form.get("documenType") == "true")
        # busNumberBoolean = (request.form.get("busNumber") == "true")
        # nameCompanyBoolean = (request.form.get("nameCompany") == "true")
        # addressCompanyBoolean = (request.form.get("addressCompany") == "true")
        # phoneNumberCompanyBoolean = (request.form.get("phoneNumberCompany") == "true")
        # emailCompanyBoolean = (request.form.get("emailCompany") == "true")
        # dateRegisterBoolean = (request.form.get("dateRegister") == "true")
        #Mô hình lựa chọn
        toolBoxWithOcr = (request.form.get("toolBoxWithOcr") == "true")
        toolBoxWithTesseract = (request.form.get("toolBoxWithTesseract") == "true")
        easyOcr = (request.form.get("easyOcr") == "true")
        if toolBoxWithOcr or toolBoxWithTesseract or easyOcr:
            print("su dung mo hinh")
        else:    
            return render_template('web.html', msg='Bạn chưa lựa chọn mô hình')

        if image :
           # image = request.files['file']
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            img_src = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            start = time.time()
            if toolBoxWithOcr:
                data = vnOcrToolboxWithVietOcr(img_src,config)
                # data = join_strings_better(data)
                print(data)
            elif toolBoxWithTesseract:
                data = vnOcrToolboxWithTesseract(img_src,config)
                # data = join_strings_better(data)
            elif easyOcr:
                data = easyocrFunction(img_src)
            # dataJoinString = join_strings_better(data)
            # print(dataJoinString)
            (documenType, busNumber, nameCompany, addressCompany, phoneNumberCompany, emailCompany,dateRegister) = getDataCompany(data)
            (nameRep,sexRep, birthRep, documentTypeRep,documentNumberRep,documentDateRep,addressRep) = getDataRep(data)
            end = time.time()
            
            return render_template("web.html", user_image=image.filename, msg="Tải lên thành công",
             documenType=documenType, busNumber=busNumber, nameCompany=nameCompany, addressCompany=addressCompany,
             time=end - start, dateRegister=dateRegister,phoneNumberCompany=phoneNumberCompany, emailCompany=emailCompany,
             nameRep=nameRep, sexRep=sexRep,documentTypeRep=documentTypeRep, documentNumberRep=documentNumberRep,birthRep=birthRep,
             documentDateRep=documentDateRep, addressRep=addressRep)





            # return render_template("web.html", user_image=image.filename, msg="Tải lên thành công",
            #  documenTypeBoolean=documenTypeBoolean, busNumberBoolean=busNumberBoolean,
            #  nameCompanyBoolean=nameCompanyBoolean, 
            #  addressCompanyBoolean=addressCompanyBoolean, phoneNumberCompanyBoolean=phoneNumberCompanyBoolean, 
            #  documenType=documenType, dateRegisterBoolean=dateRegisterBoolean,
            #  busNumber=busNumber, nameCompany=nameCompany, addressCompany=addressCompany,
            #  time=end - start, dateRegister=dateRegister,
            #  phoneNumberCompany=phoneNumberCompany, emailCompany=emailCompany, emailCompanyBoolean=emailCompanyBoolean)
        else:
            return render_template('web.html', msg='Bạn chưa lựa chọn file')

    else:
        return render_template('web.html')

    

if __name__ == '__main__':
    app.run(debug=True)

