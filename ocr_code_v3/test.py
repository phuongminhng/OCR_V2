import cv2
import pytesseract
import fastwer


# Define reference text and output text
# ref = 'my ab abc '
# output = 'my nime '

# cer = ''
# wer = ''
# # Obtain Sentence-Level Character Error Rate (CER)
# cer = fastwer.score_sent(output, ref, char_level=True)

# wer = fastwer.score_sent(output, ref)

# print(cer)

# # print(wer)
def wer(ref, hyp):
    # Tách các từ trong văn bản
    ref = ref.split()
    hyp = hyp.split()
    print(len(ref))
    print(len(hyp))
    # Khởi tạo ma trận lỗi
    matrix = [[0 for x in range(len(hyp) + 1)] for y in range(len(ref) + 1)]

    print(matrix)
    
    # Điền giá trị ban đầu vào ma trận
    for i in range(len(ref) + 1):
        for j in range(len(hyp) + 1):
            if i == 0:
                matrix[i][j] = j
            elif j == 0:
                matrix[i][j] = i
        print(matrix)
    # print(matrix) 
    # Tính giá trị cho ma trận
    for i in range(1, len(ref) + 1):
        # tinh cho doan ref
        print(ref[i-1])
# ref = "this is a test"
# hyp = "this a test1 dfas asfa wertwe"
        for j in range(1, len(hyp) + 1):
            if ref[i - 1] == hyp[j - 1]:
                print(j-1)
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                substitute = matrix[i - 1][j - 1] + 1 #2
                insert = matrix[i][j - 1] + 1 #0
                delete = matrix[i - 1][j] + 1 
                matrix[i][j] = min(substitute, insert, delete)
                print("min :", min(substitute, insert, delete))
    print(matrix)
    # Tính tỷ lệ lỗi WER
    print(matrix[len(ref)][len(hyp)])
    wer = (matrix[len(ref)][len(hyp)]) / len(ref)
    
    return wer

# import editdistance
# import nltk
# # nltk.download('punkt')
# def wer(reference, hypothesis):
#     # Tách từ trong hai văn bản
#     ref_words = nltk.word_tokenize(reference.lower())
#     hyp_words = nltk.word_tokenize(hypothesis.lower())

#     # Tính số lỗi từ
#     distance = editdistance.eval(ref_words, hyp_words)
#     error_rate = distance / len(ref_words)

#     # Chuyển đổi thành phần trăm
#     wer = error_rate

#     return wer

# ref = "this is a test"
# hyp = "this a test1 dfas asfa wertwe"

# # 2 + 4 + 2 / 6




# wer_score = wer(ref, hyp)

# print("WER: {:.2%}".format(wer_score))



# from PIL import Image, ImageFilter, ImageOps

# # mở ảnh và chuyển sang định dạng xám
# image = Image.open('image.jpg').convert('L')

# # làm nét và giảm mờ ảnh
# image = image.filter(ImageFilter.SHARPEN).filter(ImageFilter.MedianFilter())

# # xử lý độ tương phản của ảnh
# enhancer = ImageOps.autocontrast(image)

# # chuyển ảnh sang định dạng đen trắng bằng cách đặt ngưỡng giữa
# image = enhancer.point(lambda x: 0 if x < 128 else 255)

# # hiển thị ảnh đã xử lý
# image.show()


# x = np.array(['EasyOcr','VietOcr','Tesseract'])
# y = np.array([int(len(imageResultEasyOcr)),int(len(imageResultToolboxWithVietOcr)),int(len(imageResultToolboxWithTesseract))])
# plt.xlabel('Model')
# plt.title("Độ chính xác")
# plt.ylabel('Number image')
# plt.bar(x,y, width=0.5)
# plt.savefig('acc.png')
# plt.show()


import matplotlib.pyplot as plt
import numpy as np
# years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
# gdp = [300.2, 543.3, 100.9, 10.5, 5979.6, 10289.7, 14958.3]
# gdp1 = [10.2, 103.3, 100.9, 10.5, 59.6, 289.7, 958.3]
# plt.plot(years, gdp,label='Tuanna', color='green', marker='o', linestyle='solid')
# plt.plot(years, gdp1, label='tuanna1', color='red', marker='o', linestyle='solid')
# plt.legend(['Tuanna','tuanna1'])
# plt.title("Word X")
# plt.ylabel("WER (%)")
# plt.xlabel("Number Image")
# plt.savefig('acc/'+'test'+'.png')
# plt.show()
# import fastwer
# hypo = ['This is an example  sada abc']
# ref = ['This is the example ']

# # Corpus-Level WER: 40.0
# error = fastwer.score(hypo, ref)

# print(error)


import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))
 
# set height of bar
easyOcr = [12, 30, 1, 8, 22]
vietOcr = [28, 6, 16, 5, 10]
tesseract = [29, 3, 24, 25, 17]
 
# Set position of bar on X axis
br1 = np.arange(len(easyOcr))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
 
# Make the plot
plt.bar(br1, easyOcr, color ='r', width = barWidth,
        edgecolor ='grey', label ='EasyOcr')
plt.bar(br2, vietOcr, color ='g', width = barWidth,
        edgecolor ='grey', label ='vietOcr')
plt.bar(br3, tesseract, color ='b', width = barWidth,
        edgecolor ='grey', label ='tesseract')
 
# Adding Xticks
plt.xlabel('Branch', fontweight ='bold', fontsize = 15)
plt.ylabel('Students passed', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(easyOcr))],
        ['2015', '2016', '2017', '2018', '2019'])
 
plt.legend()
plt.savefig('test'+'.png')
plt.show()