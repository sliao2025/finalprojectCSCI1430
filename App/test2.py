import tkinter as tk
from tkinter import filedialog, Text, Label
from PIL import ImageTk, Image
import cv2
import os



def addFile():
    filename = filedialog.askopenfilename(initialdir="/", title = "Select File",
    filetypes=(("executables", "*.jpg"), ("all files", "*.*")))
    introFrame.pack_forget()
    file_chosen_frame.pack()



is_capturing = True

root = tk.Tk()

canvasWidth = 1000
canvasHeight = 700



canvas = tk.Canvas(root, height = canvasHeight, width = canvasWidth)
canvas.pack()


introFrame = tk.Frame(root, bg = "white")
file_chosen_frame = tk.Frame(root, bg= "black")
main_cap_frame = tk.Frame(root, bg = "white")

introFrameLabel = tk.Label(introFrame, text = "First frame")
introFrameLabel.pack()

file_chosen_frame_label = tk.Label(file_chosen_frame, text = "Second Frame")
file_chosen_frame_label.pack()


open_file_button = tk.Button(root, text = "Open File", padx = 10, pady = 5, fg = "black", command = addFile)
open_file_button.pack()







def begin_capture():
    cap = cv2.VideoCapture(0)
def video_stream():
    global cap
    _, frame = cap.read()
    curr_frame = frame
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2image = cv2.flip(cv2image, 10)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = img)
    mainCapture.imgtk = imgtk
    mainCapture.configure(image = imgtk)
    if is_capturing == True:
        mainCapture.after(1, video_stream)
    




root.mainloop()

