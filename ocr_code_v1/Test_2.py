import cv2
import pytesseract
# pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# Đọc ảnh
image = cv2.imread('../data/GPKD_FIX_1.jpg')

# Hiển thị ảnh và cho phép chọn vùng

(x,y,w,h) = cv2.selectROI(image)
# ROI = image[y:y+h, x:x+w]

# Tìm kiếm vùng chứa mã số thuế và trích xuất thông tin
taxcode_roi = image[y:h+y, x:x+w] # tọa độ x, y và chiều rộng, chiều cao của vùng quan tâm
taxcode_text = pytesseract.image_to_string(taxcode_roi, lang='vie')

# Tìm kiếm vùng chứa tên công ty và trích xuất thông tin
#company_roi = img[394:423, 100:715] # tọa độ x, y và chiều rộng, chiều cao của vùng quan tâm
#company_text = pytesseract.image_to_string(company_roi, lang='vie')

# In kết quả
print(taxcode_text)
#print('Tên công ty:', company_text)



