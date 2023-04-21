import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
class OCRApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.upload_button = tk.Button(self)
        self.upload_button["text"] = "Tải ảnh lên"
        self.upload_button["command"] = self.load_image
        self.upload_button.pack(side="top")

        self.ocr_button = tk.Button(self)
        self.ocr_button["text"] = "OCR ảnh"
        self.ocr_button["command"] = self.do_ocr
        self.ocr_button.pack(side="top")

        self.quit = tk.Button(self, text="Thoát", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.result_text = tk.Text(self)
        self.result_text.pack()

    def load_image(self):
        image_file = filedialog.askopenfilename()
        if image_file:
            self.image_file = image_file
            self.image = Image.open(image_file).resize((340,230))  # Resize ảnh với kích thước 640x480
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label = tk.Label(self.master, image=self.photo)
            self.image_label.pack()

    def do_ocr(self):
        if hasattr(self, 'image_file'):
            text = pytesseract.image_to_string(Image.open(self.image_file), lang='vie')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, text)

            # Tìm thông tin mã số doanh nghiệp và tên công ty trong kết quả OCR
            for line in text.split('\n'):
                if 'mã số doanh nghiệp' in line.lower():
                    ma_so = re.search(r'\d+', line).group(0)
                    print('Mã số doanh nghiệp:', ma_so)
                if 'tên công ty viết bằng tiếng việt' in line.lower():
                    ten_cong_ty = line.strip().split(':')[-1]
                    start_index = text.index(line) + len(line)
                    end_index = text.find('Tên công ty viết bằng tiếng nước ngoài', start_index)
                    ten_cong_ty += text[start_index:end_index].strip().replace('Tên công ty viết bằng tiếng Việt', '')
                    print('Tên công ty:', ten_cong_ty)
                if 'địa chỉ trụ sở chính' in line.lower():
                    dia_chi_tru_so = line.strip().split(':')[-1]
                    start_index = text.index(line) + len(line)
                    end_index = text.find('Điện thoại', start_index)
                    dia_chi_tru_so += text[start_index:end_index].strip()
                    print('Địa chỉ trụ sở chính:', dia_chi_tru_so)
                if 'điện thoại' in line.lower():
                    dien_thoai = re.search(r':\s*(.+)',line).group(1)
                    print('Điện thoại:', dien_thoai)
                if 'email' in line.lower():
                    email = line.strip().split(':')[-1]
                    start_index = text.index(line) + len(line)
                    email = text.find('website', start_index)
                    print('Email:',email)
            if not ma_so and not ten_cong_ty:
                print('Không tìm thấy thông tin mã số doanh nghiệp và tên công ty')

root = tk.Tk()
app = OCRApp(master=root)
app.mainloop()

