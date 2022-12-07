import tkinter as tk
from tkinter import filedialog, Text, Label
import PIL
from PIL import ImageTk, Image
import cv2
import os

root = tk.Tk()

def addFile():
    filename = filedialog.askopenfilename(initialdir="/", title = "Select File",
    filetypes= (("executables", "*.exe"), ("all files", "*.*")))


canvasHeight, canvasWidth = 700, 1000

canvas = tk.Canvas(root, height = canvasHeight, width = canvasWidth, bg = "#263D42")
canvas.pack()

cap = cv2.VideoCapture(0)



frame = tk.Frame(root, bg = "white")
frame.place(relwidth = (cap.get(3)/canvasWidth), relheight=(cap.get(4)/canvasHeight), relx= (0.5 - (cap.get(3)/2)/canvasWidth), rely = (0.5 - (cap.get(4)/2)/canvasHeight))

lmain = Label(frame)
lmain.grid()

openFile = tk.Button(root, text = "Open File", padx = 10, pady = 5, fg = "white", bg = "#263D42", command=addFile)
openFile.pack()


def video_stream():
    _, frame = cap.read()
    frame = cv2.flip(frame, flipCode=10)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream)


video_stream()

root.mainloop()