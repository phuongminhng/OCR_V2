import easyocr
import cv2
reader = easyocr.Reader(['vi']) # this needs to run only once to load the model into memory
# result = reader.readtext('/home/tuanna/Desktop/OCR/data/GPKD_2.jpg',detail=0)
# print(result)

# img = cv2.imread('chinese_tra.jpg')
# result = reader.readtext(img)
# with open("/home/tuanna/Desktop/OCR/data/GPKD_2.jpg", "rb") as f:
#     img = f.read()
# result = reader.readtext(img, detail = 0, paragraph=True)


# specify languages and other configs
# import cv2
import os

# for image_name in os.listdir("images"):
#     # read image
image = cv2.imread('/home/tuanna/Desktop/OCR/data/GPKD_2.jpg')
results = reader.readtext(image)
result = reader.readtext(image, detail = 0, paragraph=True)
print(result)
# draw rectangle on easyocr results
for res in results:
    top_left = (int(res[0][0][0]), int(res[0][0][1])) # convert float to int
    bottom_right = (int(res[0][2][0]), int(res[0][2][1])) # convert float to int
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 3)
    cv2.putText(image, res[1], (top_left[0], top_left[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
# write image
cv2.imwrite(f'a.jpg', image)
cv2.putText(image, res[1], (top_left[0], top_left[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)