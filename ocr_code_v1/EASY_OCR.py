import cv2

# Đọc ảnh
img = cv2.imread('../data/cccd.jpg')

# Chuyển ảnh sang đen trắng
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Tìm contours (đường viền)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Vẽ hình chữ nhật bao quanh các contours
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

# Hiển thị ảnh với ROI đã xác định
cv2.imshow('ROI', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

