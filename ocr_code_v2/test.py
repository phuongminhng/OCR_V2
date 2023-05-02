import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
import math

#Declare pytessecart excuteable path
# pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR/tesseract'
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesserac'
#My custom class for declare region of interest.
import ImageConstantROI 

#Custom function to show open cv image on notebook.
def display_img(cvImg):
    cvImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10,8))
    plt.imshow(cvImg)
    plt.axis('off')
    plt.show()


# Step 2
#Loading image using cv2
baseImg = cv2.imread('../data/GPKD_2.jpg')

#Declare image size, width height and chanel
baseH, baseW, baseC = baseImg.shape

# display_img(baseImg)




#Step 3
#Create a custom function to cropped image base on religion of interest
def cropImageRoi(image, roi):
    roi_cropped = image[
        int(roi[1]) : int(roi[1] + roi[3]), int(roi[0]) : int(roi[0] + roi[2])
    ]
    return roi_cropped

testCrop = cropImageRoi(baseImg, ImageConstantROI.GETROI.ROIS_GPKD['msdn'][0])
# display_img(testCrop)

#step 4
# pytesseract.image_to_string(testCrop, config='--oem 1 --psm 6')


#step 5
def preprocessing_image(img):

    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    display_img(img)
    #convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.multiply(gray, 0.5)
    
    #blur remove noise
    blured1 = cv2.medianBlur(gray,3)
    blured2 = cv2.medianBlur(gray,81)
    divided = np.ma.divide(blured1, blured2).data
    normed = np.uint8(255*divided/divided.max())
    
    
    #Threshold image
    th, threshed = cv2.threshold(normed, 100, 255, cv2.THRESH_OTSU )
    
    return threshed

testPreprocess = preprocessing_image(testCrop)
# display_img(testPreprocess)

# step 6
pytesseract.image_to_string(testCrop, config='--oem 1 --psm 6')


# step 7
MODEL_CONFIG = '-l vie --oem 1 --psm 6'
for key, roi in ImageConstantROI.GETROI.ROIS_GPKD.items():
    data = ''
    for r in roi:
        crop_img = cropImageRoi(baseImg, r)
        
        #For a small pxi image only has number, do not preprocessing it is better
        if key != 'date_expire':
            crop_img = preprocessing_image(crop_img)
        
        # display_img(crop_img)

        
        data += pytesseract.image_to_string(crop_img, config = MODEL_CONFIG) + ' '
            
    print(f"{key} : {data.strip()}")


def extractDataFromIdCard(img):
    for key, roi in ImageConstantROI.GETROI.ROIS_GPKD.items():
        data = ''
        for r in roi:
            crop_img = cropImageRoi(img, r)
            
          
            
            # display_img(crop_img)

            #Extract data from image using pytesseract
            data += pytesseract.image_to_string(crop_img, config = MODEL_CONFIG) + ' '
                
        print(f"{key} : {data.strip()}")

extractDataFromIdCard(baseImg)
#Load image
img2 = cv2.imread('../data/GPKD_gcndkdoanhnghiepcongtycophan_16.jpg')

# display_img(img2)


basePreImg = preprocessing_image(baseImg)
# display_img(basePreImg)


#Init orb, keypoints detection on base Image
orb = cv2.ORB_create(1000)

kp, des = orb.detectAndCompute(basePreImg, None)
imgKp = cv2.drawKeypoints(basePreImg,kp, None)

display_img(imgKp)

img2 = preprocessing_image(img2)


PER_MATCH = 0.25

#Detect keypoint on img2
kp1, des1 = orb.detectAndCompute(img2, None)

#Init BF Matcher, find the matches points of two images
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = list(bf.match(des1, des))

#Select top 30% best matcher 
matches.sort(key=lambda x: x.distance)
best_matches = matches[:int(len(matches)*PER_MATCH)]

#Show match img  
imgMatch = cv2.drawMatches(img2, kp1, basePreImg, kp, best_matches,None, flags=2)
display_img(imgMatch)


#Init source points and destination points for findHomography function.
srcPoints = np.float32([kp1[m.queryIdx].pt for m in best_matches]).reshape(-1,1,2)
dstPoints = np.float32([kp[m.trainIdx].pt for m in best_matches]).reshape(-1,1,2)


#Find Homography of two images
matrix_relationship, _ = cv2.findHomography(srcPoints, dstPoints,cv2.RANSAC, 5.0)

#Transform the image to have the same structure as the base image
img_final = cv2.warpPerspective(img2, matrix_relationship, (baseW, baseH))

display_img(img_final)

display_img(img2)


extractDataFromIdCard(img_final)


























































