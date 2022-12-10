import tkinter as tk
from tkinter import filedialog, Text, Label
from PIL import ImageTk, Image
import numpy as np
from skimage import io, color
import cv2
from matplotlib import pyplot as plt
import os
import matplotlib.image
from sift import SIFT


root = tk.Tk()

image = 0
lab2 = 0
frame2 = 0
button2 = 0

colors = ["Orange", "Yellow"]
avgColors = [0, 0]
colorCounter = 0

def addFile():
    global image, lab2, frame2, button2, colors
    filename = filedialog.askopenfilename(initialdir="/", title = "Select File",
    filetypes=(("executables", "*.jpg"),("executables", "*.png"), ("all files", "*.*")))
    frame1.pack_forget()

    frame2 = tk.Frame(root, bg = "black")
    image = io.imread(filename)

    img = ImageTk.PhotoImage(Image.open(filename))
    lab2 = tk.Label(frame2, text = "Choose Colors for Callibration", image = img, cursor="dot")
    lab2.bind('<Button-1>', on_click)
    lab2.photo = img


    lab2.place(x=0, y=0, relwidth=1, relheight=1)
    
    colorString = "Choose {}".format("Orange")
    button2 = tk.Button(frame2, text = colorString)
    
    
    lab2.pack()
    button2.pack()
    frame2.pack()


def getColor(x, y):
    global avgColors, image, colorCounter

    labImage = color.rgb2lab(image)

    x = round(x)
    y = round(y)
    r = 5
    ret = np.zeros(3)
    for i in range(r):
        for j in range(r):
            ret = ret + labImage[y-round((r-1)/2)+j][x-round((r-1)/2)+i]
    ret = ret/(r*r)
    avgColors[colorCounter] = ret
    print(avgColors)
    return ret
    


def on_click(event):
    global lab2, colors, colorCounter, avgColors
    ret = []
    getColor(event.x, event.y)

    colorCounter += 1

    if colorCounter == 2: 
        return

    colorString = "Choose {}".format(colors[colorCounter])
    

    if colorCounter == 2:
        print(avgColors)
        return

    lab2.config(cursor = "dot")
    button2.config(text = colorString)
    
def calcDeltaE(img1, img2):
    return np.sqrt(np.sum((img1 - img2) ** 2, axis=-1))/255

def getAllColor(c1, image):
    colorImage = np.full((image.shape), c1)
    delt = calcDeltaE(image, colorImage)
    m = np.mean(delt)
    newImage = np.zeros((image.shape[0], image.shape[1]))
    print(m/2)
    newImage[delt < 0.16] = 1
    return newImage


frame1 = tk.Frame(root, bg = "white")
lab1 = tk.Label(frame1, text = "Please Upload a Photo")
button1 = tk.Button(frame1, text = "Open Files", command = addFile)

lab1.pack()
button1.pack()


frame1.pack()
root.mainloop()


