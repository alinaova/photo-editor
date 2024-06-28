import cv2
import numpy as np
from tkinter import filedialog, messagebox, Tk, Label, Button, Entry, StringVar, Frame
from PIL import Image, ImageTk

class PhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение обработки изображений")

        self.image = None
        self.img_path = None

        self.frame = Frame(root)
        self.frame.pack()

        self.canvas = Label(self.frame)
        self.canvas.grid(row=0, column=0, columnspan=4)

        Button(self.frame, text="Загрузить изображение", command=self.load_image).grid(row=1, column=0)
        Button(self.frame, text="Сделать снимок с веб-камеры", command=self.capture_image).grid(row=1, column=1)

        Button(self.frame, text="Красный канал", command=lambda: self.show_channel('R')).grid(row=2, column=0)
        Button(self.frame, text="Зеленый канал", command=lambda: self.show_channel('G')).grid(row=2, column=1)
        Button(self.frame, text="Синий канал", command=lambda: self.show_channel('B')).grid(row=2, column=2)

        Label(self.frame, text="Изменить размер изображения:").grid(row=3, column=0, columnspan=2)
        self.width_entry = Entry(self.frame)
        self.width_entry.grid(row=4, column=0)
        self.height_entry = Entry(self.frame)
        self.height_entry.grid(row=4, column=1)
        Button(self.frame, text="Изменить", command=self.resize_image).grid(row=4, column=2)

        Label(self.frame, text="Понизить яркость:").grid(row=5, column=0, columnspan=2)
        self.brightness_entry = Entry(self.frame)
        self.brightness_entry.grid(row=6, column=0)
        Button(self.frame, text="Изменить", command=self.reduce_brightness).grid(row=6, column=1)

        Label(self.frame, text="Нарисовать прямоугольник (x y w h):").grid(row=7, column=0, columnspan=2)
        self.rect_x_entry = Entry(self.frame)
        self.rect_x_entry.grid(row=8, column=0)
        self.rect_y_entry = Entry(self.frame)
        self.rect_y_entry.grid(row=8, column=1)
        self.rect_w_entry = Entry(self.frame)
        self.rect_w_entry.grid(row=9, column=0)
        self.rect_h_entry = Entry(self.frame)
        self.rect_h_entry.grid(row=9, column=1)
        Button(self.frame, text="Нарисовать", command=self.draw_rectangle).grid(row=9, column=2)

    def load_image(self):
        self.img_path = filedialog.askopenfilename(filetypes=[("Файл изображения", "*.jpg *.png")])
        if self.img_path:
            self.image = cv2.imread(self.img_path)
            self.show_image()

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Ошибка", "Невозможно открыть веб-камеру.")
            return
        ret, frame = cap.read()
        cap.release()
        if ret:
            self.image = frame
            self.show_image()
        else:
            messagebox.showerror("Ошибка", "Невозможно сделать снимок с веб-камеры.")

    def show_image(self):
        if self.image is not None:
            rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.canvas.config(image=tk_image)
            self.canvas.image = tk_image

    def show_channel(self, channel):
        if self.image is not None:
            img = self.image.copy()
            if channel == 'R':
                img[:, :, 1] = 0
                img[:, :, 2] = 0
            elif channel == 'G':
                img[:, :, 0] = 0
                img[:, :, 2] = 0
            elif channel == 'B':
                img[:, :, 0] = 0
                img[:, :, 1] = 0
            self.image = img
            self.show_image()

    def resize_image(self):
        if self.image is not None:
            try:
                width = int(self.width_entry.get())
                height = int(self.height_entry.get())
                self.image = cv2.resize(self.image, (width, height))
                self.show_image()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите размеры.")

    def reduce_brightness(self):
        if self.image is not None:
            try:
                reduction = int(self.brightness_entry.get())
                self.image = cv2.convertScaleAbs(self.image, alpha=1, beta=-reduction)
                self.show_image()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите понижение яркости.")

    def draw_rectangle(self):
        if self.image is not None:
            try:
                x = int(self.rect_x_entry.get())
                y = int(self.rect_y_entry.get())
                w = int(self.rect_w_entry.get())
                h = int(self.rect_h_entry.get())
                cv2.rectangle(self.image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                self.show_image()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите правильные координаты и размер.")

if __name__ == "__main__":
    root = Tk()
    app = PhotoEditor(root)
    root.mainloop()
