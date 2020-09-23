import tkinter as tk
import cv2
from tkinter import filedialog
import tkinter.simpledialog
import tkinter.messagebox
import PIL
from PIL import Image,ImageTk
import numpy as np
import cv2
import os
from tkinter import messagebox
import logging

logger=logging.getLogger()
con=[]

# Python code to remove duplicate elements
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


def convert():
    return

def export(con):

    unicode=["\u0B85","\u0B86","\u0B87","\u0B88","\u0B89","\u0B8A","\u0B8E","\u0B8F","\u0B92","\u0B93",
                 "\u0B95""\u0B82","\u0B99""\u0B82","\u0B9A""\u0B82","\u0B9E""\u0B82",
                "\u0B9F""\u0B82","\u0BA3""\u0B82","\u0BA4""\u0B82","\u0BA8""\u0B82",
                "\u0BAA""\u0B82","\u0BAE""\u0B82","\u0BAF""\u0B82","\u0BB0""\u0B82",
                "\u0BB2""\u0B82","\u0BB5""\u0B82","\u0BB4""\u0B82","\u0BA9""\u0B82"]
    
    #Sorting the stored array
    con.sort()
           
    # Remove duplicate number The first co-ordinate point
    Remove(con)

    #File Write Operation to wirte a chars into a file .txt
    output=open("output.txt","w",encoding="utf-8")
              
    #string name
    out=''

    #printing the 3rd element which means the actual character
    j=0
    for i in con:
                 
        x=con[j][2]
        print(unicode[x],end=' ')
        out+=str(unicode[x])
        j=j+1

    #join all chars into one
    output.write(''.join(out))
                 
    logger.debug("Values exported")
    return
            
#IMport Image to be tested
def get_image():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        img_bgr = cv2.imread(file_path)

        img_gray = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2GRAY)

        con=[]
        namelist=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26"]
        unicode=["\u0B85","\u0B86","\u0B87","\u0B88","\u0B89","\u0B8A","\u0B8E","\u0B8F","\u0B92","\u0B93","\u0B94",
                 "\u0B95""\u0B82","\u0B99""\u0B82","\u0B9A""\u0B82","\u0B9E""\u0B82",
                "\u0B9F""\u0B82","\u0BA3""\u0B82","\u0BA4""\u0B82","\u0BA8""\u0B82",
                "\u0BAA""\u0B82","\u0BAE""\u0B82","\u0BAF""\u0B82","\u0BB0""\u0B82",
                "\u0BB2""\u0B82","\u0BB5""\u0B82","\u0BB4""\u0B82","\u0BA9""\u0B82"]

        #unicode_mei=[]
        i=1
        
        for i in range(len(namelist)):
            
            name="test-data/"+namelist[i]+".png"
            im = Image.open(name)
            
            #get the file name to print it 
            x=im.filename
            value=int(namelist[i])
            
            #print(x)
            template = cv2.imread(name,0)
            w,h=template.shape[::-1]

            #Matching the features with the therushold value
            res=cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            
            #if threshold value change the result can be modified as per our need
            threshold=0.90
            loc=np.where(res>=threshold)
            
            #Draw Rectangle on the particular portion in a imgae where the values matches
            for pt in zip(*loc[::-1]):
                 #Prints the co-ordinates value of the letters
                 print(pt,end='')
                 print(i,end='')
                 cv2.rectangle(img_bgr,pt,(pt[0]+w,pt[1]+h),(0,255,0),2)
                 con.append((pt[0],pt[1],i))
                 
        export(con)
        
        cv2.imshow('detected',img_bgr)

        return 



#Main   
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

root.title('Tamil AD2 - OCR')
root.geometry('400x500')

# this removes the maximize button
root.resizable(0,0)


#import button fro test image

var = "Conversion of Early Tamil Brahmi character into \n Modern Tamil Characters Using Template Matching"
label1 = tk.Label( root, text=var,compound='top',font=("Helvetica", 12),bg="white",fg="black")
label1.pack()

var1 = "\n\n 1.Import Image from your local computer\n\n2.Text Extracted from Imgae\n\n3.Open 'output.txt' file for extracted text"
label = tk.Label( root, text=var1,compound='left',font=("Helvetica", 12))
label.pack()

button1 = tk.Button(frame, 
                   text="Import Image", 
                   fg="blue",
                   command=get_image,
                   height = 4, width = 50)
#button.pack(side=tk.TOP)
button1.grid(row=1, column=0, padx=10, pady=20)

button4 = tk.Button(frame,
                   text="Exit",
                   fg="green",
                   command=quit,
                   height = 4, width = 50)

button4.grid(row=6, column=0, padx=10, pady=20)


root.mainloop()





