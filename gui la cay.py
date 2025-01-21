import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import tensorflow as tf

# Khởi tạo biến cap để sử dụng trong toàn bộ chương trình
cap = None

# Load mô hình đã lưu
model = tf.keras.models.load_model('model2.h5')

# Chuẩn bị danh sách tên lớp
class_names = ['Bệnh Bạc Lá', 'Bệnh Đốm Nâu', 'Bệnh Đốm Lá', 'Lá Khỏe Mạnh']

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', ['.jpg', '.jpeg', '.png', '.gif'])])
    if file_path:
        process_image(file_path)

def take_photo_from_camera():
    global cap  # Sử dụng biến cap global
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('captured_image.jpg', frame)
        process_image('captured_image.jpg')
    cap.release()  # Giải phóng tài nguyên camera

def process_image(image_path):
    image = cv2.imread(image_path)
    if image is not None:
        image = cv2.resize(image, (180, 180))
        image = np.expand_dims(image, axis=0)
        image = image.astype('float32') / 255.0
        predictions = model.predict(image)
        predicted_class_index = np.argmax(predictions)
        predicted_class_name = class_names[predicted_class_index]
        result_label.config(text="DỰ ĐOÁN BỆNH: " + predicted_class_name)

        image = cv2.cvtColor(image[0], cv2.COLOR_BGR2RGB)
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        img_label.config(image=image)
        img_label.image = image
    else:
        result_label.config(text="Failed to process the image.")

# Tạo hàm để giải phóng tài nguyên camera trước khi thoát chương trình
def on_closing():
    global cap  # Sử dụng biến cap global
    if cap is not None and cap.isOpened():
        cap.release()  # Giải phóng tài nguyên camera
    window.destroy()  # Đóng cửa sổ

# Tạo cửa sổ Tkinter
window = tk.Tk()
window.title("Image Classification")
window.geometry("800x450")

# Label và Button
label1 = tk.Label(window, text="Nhận dạng bệnh lá lúa", font=("Arial", 30), fg="red")
label1.pack()

label2 = tk.Label(window, text="Lê Hoàng Đông Phương_19430841", font=("Arial", 15), fg="black")
label2.pack()

label3 = tk.Label(window, text="Lê Ngọc Thái_19433741", font=("Arial", 15), fg="black")
label3.pack()

open_button = tk.Button(window, text="CHỌN ẢNH BỆNH", command=open_image)
open_button.pack()

capture_button = tk.Button(window, text="CHỤP ẢNH TỪ CAMERA", command=take_photo_from_camera)
capture_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

img_label = tk.Label(window)
img_label.pack()

# Gán hàm on_closing() vào sự kiện thoát cửa sổ
window.protocol("WM_DELETE_WINDOW", on_closing)

# Chạy giao diện người dùng
window.mainloop()
