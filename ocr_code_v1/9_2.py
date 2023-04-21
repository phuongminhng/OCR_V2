import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
img = cv2.imread("GPKD.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
text = pytesseract.image_to_string(img, lang="vie")
split_text = text.split("\n")
print(text)
with open("dịch.txt","a",encoding="utf-8") as f:
    f.writelines(text)