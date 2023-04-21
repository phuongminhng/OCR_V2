# import cv2
#
# # Load ảnh
# image = cv2.imread('5.jpg')
#
# # Hiển thị ảnh và cho phép chọn vùng
#
# (x,y,w,h) = cv2.selectROI(image)
# ROI = image[y:y+h, x:x+w]
#
#
# # In ra tọa độ và kích thước của vùng
# print("x:", x)
# print("y:", y)
# print("width:", w)
# print("height:", h)
import cv2

image = cv2.imread('../data/cccd.jpg')
(x,y,w,h) = cv2.selectROI(image)
# ROI = image[y:y+h, x:x+w]
print("x:", x)
print("y:", y)
print("width:", w)
print("height:", h)


