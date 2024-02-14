import application
import tkinter as tk
from tkinter import ttk
import threading
import numpy as np
import cv2
import random
from PIL import Image, ImageTk
import tkinter.font as tkFont
import time

class GUI():
    def __init__(self):
        self.path=""
        self.window=tk.Tk()
        self.window.geometry("700x900")
        self.window.title("Stock Cutting Program")
        self.errorFlag=False
        self.canRun=0
        self.chosen= ' - '
        self.menu()
        self.app = application.App()
        self.menuStyle=ttk.Style()
        self.indexCounter=[0,0,-1]
        self.check=-1
        self.getcode=['']
        self.window.iconbitmap(r'Yıldız_Technical_University_Logo.ico')
        self.menuStyle.configure("main.TFrame", background='#2c7e9c')
        self.rectangles=[]

        



        self.window.mainloop()
    def menu(self):
        print("Girdi")
        self.menuFrame=ttk.Frame(self.window,style='main.TFrame')
        self.rectangles=[]
        ytu=cv2.imread(r"ytu.png")
        img = cv2.cvtColor(ytu, cv2.COLOR_BGR2RGB)
        # PIL.Image nesnesine dönüştür
        im = Image.fromarray(img)
        # Tkinter uyumlu görüntüye çevir
        logo = ImageTk.PhotoImage(image=im)
        labelLogo = tk.Label(self.menuFrame, image=logo, bg='#2c7e9c')
        labelLogo.image=logo
       
        self.dataLabel=tk.Label(self.menuFrame,background='#2c7e9c',fg='white',font=30)      
        self.one = tk.Button(
            self.dataLabel,
            text="C1_1",
            bg="#3bcc9c",
            fg="black",
            activebackground="#68ed9b",
            activeforeground="white",
            font=24,
            
            cursor="hand2",
            command=self.path1
        )
        self.two = tk.Button(
            self.dataLabel,
            text="C1_2",
            bg="#3bcc9c",
            fg="black",
            activebackground="#68ed9b",
            activeforeground="white",
            font=24,
           
            cursor="hand2",
            command=self.path2
        )
        self.three = tk.Button(
            self.dataLabel,
            text="C1_3",
            bg="#3bcc9c",
            fg="black",
            activebackground="#68ed9b",
            activeforeground="white",
            font=24,
            
            cursor="hand2",
            command=self.path3
        )

        self.run = tk.Button(
            self.menuFrame,
            text="Çalıştır",
            bg="#3bcc9c",
            fg="black",
            activebackground="#68ed9b",
            activeforeground="white",
            font=24,
            cursor="hand2",
            command=self.runMenu
        )

        self.exitButton = tk.Button(
            self.menuFrame,
            text="Çıkış",
            bg="#3bcc9c",
            fg="black",
            activebackground="#68ed9b",
            activeforeground="white",
            font=24,
            cursor="hand2",
            command=self.exit
        )

        name=tk.Label(self.dataLabel,text='Datasetler',background='#2c7e9c',fg='white',font=(30))
        name.place(x=50,y=30,width=200,height=50)
        labelLogo.place(x=200,y=100)
        self.dataLabel.place(x=50,y=450,width=300,height=300)
        self.one.place(x=50, y=100, width=200, height=30)
        self.two.place(x=50, y=150, width=200, height=30)
        self.three.place(x=50, y=200, width=200, height=30)
        self.run.place(x=400, y=550, width=200, height=30)
        self.exitButton.place(x=400, y=600, width=200, height=30)

        if(self.errorFlag):
            error=tk.Label(self.menuFrame,text= "Önce Dataset Seçin!",background='#2c7e9c',fg='white',font=(30))
            error.place(x=400,y=480,width=200,height=50)
            self.errorFlag=False
        else:
            choosen=tk.Label(self.menuFrame,text= "Seçilen Dataset :{}".format(self.chosen),background='#2c7e9c',fg='white',font=(30))
            choosen.place(x=400,y=480,width=200,height=50)
        self.menuFrame.place(x=0,y=0,width=700, height=900)


    def exit(self):
        
        self.window.destroy()

    def crtImg(self,base):
        self.image = np.ones(((base[0]*3), (base[1])*3, 3), dtype=np.uint8) *255
        
        originX=int(self.app.base[0][0]/2)
        originY=int(self.app.base[0][1]/2)
        cv2.rectangle(self.image, (originX,originY), (originX+(base[0]*2),originY+(base[1]*2)), (0, 0, 0), thickness=3)
        self.writeim=self.image.copy()
        self.updateFromGcode=self.image.copy()

        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # PIL.Image nesnesine dönüştür
        im = Image.fromarray(img)
        # Tkinter uyumlu görüntüye çevir
        imgtk = ImageTk.PhotoImage(image=im)
        return imgtk

            
    def finalImg(self,rect):
        #self.image[:, :] = [156,126,44]
        originX=int(self.app.base[0][0]/2)
        originY=int(self.app.base[0][1]/2)
        
        for i in rect:
            cv2.rectangle(self.image, (originX+i[0]*2,+originY+i[1]*2), (originX+i[2]*2,+originY+i[3]*2), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) , thickness=-1)
            cv2.rectangle(self.image, (originX+i[0]*2,+originY+i[1]*2), (originX+i[2]*2,+originY+i[3]*2), (0, 0, 0), thickness=2)
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # PIL.Image nesnesine dönüştür
        im = Image.fromarray(img)
        resized_image = im.resize((600,600), Image.Resampling.LANCZOS)
        # Tkinter uyumlu görüntüye çevir
        imgtk = ImageTk.PhotoImage(image=resized_image)
        """cv2.imwrite(r"C:\VsCode\Python\CDTP\Final\Result_{}.png".format(self.chosen),self.image)
        cv2.imwrite(r"C:\VsCode\Python\CDTP\Final\toGcode_{}.png".format(self.chosen),writeim)"""
        return imgtk

    def printImg(self):
        rect=self.rectangles[0]

        originX=int(self.app.base[0][0]/2)
        originY=int(self.app.base[0][1]/2)
        for i in rect:
            cv2.rectangle(self.writeim, (originX+i[0]*2,+originY+i[1]*2), (originX+i[2]*2,+originY+i[3]*2), (0, 0, 0), thickness=2)
        cv2.imwrite(r"results\images\Result_{}.png".format(self.chosen),self.image)
        cv2.imwrite(r"results\images\forGcode_{}.png".format(self.chosen),self.writeim)
        
    def imgProc(self,i):
        originX=int(self.app.base[0]/2)
        originY=int(self.app.base[1]/2)
        cv2.rectangle(self.image, (originX+i[0]*2,+originY+i[1]*2), (originX+i[2]*2,+originY+i[3]*2), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) , thickness=-1)
        cv2.rectangle(self.image, (originX+i[0]*2,+originY+i[1]*2), (originX+i[2]*2,+originY+i[3]*2), (0, 0, 0), thickness=1)
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # PIL.Image nesnesine dönüştür
        im = Image.fromarray(img)
        # Tkinter uyumlu görüntüye çevir
        imgtk = ImageTk.PhotoImage(image=im)
       
        return imgtk


    def path1(self):
        self.path=r"Original\C1_1"
        self.chosen= 'C1_1'
        return self.menu()
    def path2(self):
        self.path=r"Original\C1_2"
        self.chosen= 'C1_2'
        return self.menu()
    def path3(self):
        self.path=r"Original\C1_3"
        self.chosen= 'C1_3'
        return self.menu()


    def returnEnterFromRun(self):
        self.path = ''
        self.chosen=' - '
        self.runMenuFrame.pack_forget()
        self.canRun=0
        self.menu()

    def runMenu(self):
        self.app.base=[]
        self.app.rect=[]
        self.menuFrame.place_forget()
        spl=self.path.split('\\')
        
        if(len(spl)>1):
            dataName=spl[1].split('_')
            
            if(dataName[0] != 'C1'):
                
                return self.menu()
            else:
                self.finished=[0]
                self.app.readFile(self.path,10)
                self.placedIndex=[]
                self.imTk=self.crtImg(self.app.base[0])
                if(self.chosen == 'C1_1'):
                    iterNo=32000
                    counter=31500
                elif(self.chosen == 'C1_2'):
                    iterNo=25500
                    counter=25000
                elif(self.chosen == 'C1_3'):
                    iterNo=22500
                    counter=22000
                
                thr=threading.Thread(target=self.app.getSol,args=(self.rectangles,self.finished,self.placedIndex,iterNo,counter))
                thr.start()

                self.runMenuFrame=ttk.Frame(self.window, style='main.TFrame')
                """label = tk.Label(self.runMenuFrame, image=self.imTk)
                label.image=self.imTk
                label.place(x=50,y=100)"""

                self.runMenuFrame.place(x=0,y=0,width=700, height=900)
                self.wait=0
                self.waittxt=[' .  ','  . ','   .']
                self.waittxt=['    ',' .  ',' .. ',' ...']
                self.updateRun()               
        else:
            self.errorFlag=True
            self.chosen=' - '
            
            #self.errorFlag=True

            return self.menu()


    def getGcode(self):
        self.canRun=1
        path=r"results\gcodes\{}.gcode".format(self.chosen)
        pathM=r"results\gcodes\modular_{}.gcode".format(self.chosen)
        self.app.getGcode(path)
        self.app.getGcodeModular(pathM)


    def runCncMachine(self):
        if(self.canRun==1):
            path=r'results\gcodes\{}.gcode'.format(self.chosen)
            self.indexCounter=[0,0,-1]
            sendThread=threading.Thread(target=self.sendGcode.send,args=(path,self.indexCounter,self.getcode))
            sendThread.start()
            time.sleep(0.5)
            return self.updateScreen()
        else:
            self.canRun=2
            errorMsg=tk.Label(self.runMenuFrame,text= "Gcode bulunamadı!",background='#2c7e9c',fg='white',font=(30))
            errorMsg.place(x=200, y=600, width=300, height=50)
            return self.updateRun()
        
    def updateIm(self,index):
        originX=int(self.app.base[0][0]/2)
        originY=int(self.app.base[0][1]/2)
        i=self.rectangles[0][index]
      
        #cv2.rectangle(self.updateFromGcode, (originX+i[0]*2,+originY+i[1]*2), (originX+i[2]*2,+originY+i[3]*2), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) , thickness=-1)
        cv2.rectangle(self.updateFromGcode, (originX+i[0]*2,+originY+i[1]*2), (originX+i[2]*2,+originY+i[3]*2), (0, 0, 0), thickness=2)
        
        img = cv2.cvtColor(self.updateFromGcode, cv2.COLOR_BGR2RGB)
        # PIL.Image nesnesine dönüştür
        im = Image.fromarray(img)
        resized_image = im.resize((600,600), Image.Resampling.LANCZOS)
        # Tkinter uyumlu görüntüye çevir
        imgtk = ImageTk.PhotoImage(image=resized_image)
        """cv2.imwrite(r"C:\VsCode\Python\CDTP\Final\Result_{}.png".format(self.chosen),self.image)
        cv2.imwrite(r"C:\VsCode\Python\CDTP\Final\toGcode_{}.png".format(self.chosen),writeim)"""
        return imgtk
    


    def updateScreen(self):
        print(self.indexCounter,self.check)
        if(self.indexCounter[1]==0):
            if(self.indexCounter[0]!=self.check):
                print(self.getcode[0])
                if(self.getcode[0]=='SU'):
                    if(self.indexCounter[2]>0):
                        
                        img=self.updateIm(self.indexCounter[2])
                        self.runMenuFrame.destroy()            
                        self.runMenuFrame=ttk.Frame(self.window, style='main.TFrame')
                        label = tk.Label(self.runMenuFrame, image=img)
                        label.image=img
                        label.place(x=150,y=150,height=404,width=404)
                        self.runMenuFrame.place(x=0,y=0,width=700, height=900)
                        self.check=self.indexCounter[0]
                        self.indexCounter[2]=self.indexCounter[2]+1
                    else:
                        self.indexCounter[2]=self.indexCounter[2]+1
                self.window.after(100,self.updateScreen)
            else:
                self.window.after(100,self.updateScreen)
        else:
            self.back = tk.Button(
                self.runMenuFrame,
                text="Geri Dön",
                bg="#3bcc9c",
                fg="black",
                activebackground="#68ed9b",
                activeforeground="white",
                font=24,
                cursor="hand2",
                borderwidth= 2,
                command=self.returnEnterFromRun
                
            )
            self.back.place(x=200, y=800, width=300, height=30)
            self.check=-1


    def updateRun(self):
        if(self.finished[0]==1):
            self.wait=0
            if(self.canRun!=2):
                
                print(len(self.placedIndex[0]),self.placedIndex)
                #print(self.rectangles[0])
                self.runMenuFrame.destroy()            
                self.runMenuFrame=ttk.Frame(self.window, style='main.TFrame')
                txtt=''
                txtt2=''
                for index,i in enumerate(self.placedIndex[0]):
                    if index< len(self.placedIndex[0])/2:
                        if i==1:
                            txtt=txtt+"{}x{} -> Yerleşti\n".format(int(self.app.rect[index][0]/10),int(self.app.rect[index][1]/10))
                        else:
                            txtt=txtt+"{}x{} -> Yerleşmedi\n".format(int(self.app.rect[index][0]/10),int(self.app.rect[index][1]/10))
                    else:
                        if i==1:
                            txtt2=txtt2+"{}x{} -> Yerleşti\n".format(int(self.app.rect[index][0]/10),int(self.app.rect[index][1]/10))
                        else:
                            txtt2=txtt2+"{}x{} -> Yerleşmedi\n".format(int(self.app.rect[index][0]/10),int(self.app.rect[index][1]/10))
                    

                if(self.canRun==0):
                    #print("DONNN ULANNN:",self.rectangles)
                    self.imTk=self.finalImg(self.rectangles[0])
            self.back = tk.Button(
                self.runMenuFrame,
                text="Geri Dön",
                bg="#3bcc9c",
                fg="black",
                activebackground="#68ed9b",
                activeforeground="white",
                font=24,
                cursor="hand2",
                borderwidth= 2,
                command=self.returnEnterFromRun
            )
            self.print = tk.Button(
                self.runMenuFrame,
                text="Resmi Yazdır",
                bg="#3bcc9c",
                fg="black",
                activebackground="#68ed9b",
                activeforeground="white",
                font=24,
                cursor="hand2",
                borderwidth= 2,
                command=self.printImg
            )
            self.gcode = tk.Button(
                self.runMenuFrame,
                text="Gcode Çıktısını Al",
                bg="#3bcc9c",
                fg="black",
                activebackground="#68ed9b",
                activeforeground="white",
                font=24,
                cursor="hand2",
                borderwidth= 2,
                command=self.getGcode
            )
            """self.runCnc = tk.Button(
                self.runMenuFrame,
                text="Çalıştır",
                bg="#3bcc9c",
                fg="black",
                activebackground="#68ed9b",
                activeforeground="white",
                font=24,
                cursor="hand2",
                borderwidth= 2,
                command=self.runCncMachine
            )"""
            
            placeLabr=tk.Label(self.runMenuFrame,text= txtt,background='#2c7e9c',fg='black',font=(20),anchor="w")
            placeLabr.place(x=340,y=620,width=150,height=200)
            placeLabr2=tk.Label(self.runMenuFrame,text= txtt2,background='#2c7e9c',fg='black',font=(20),anchor="w")
            placeLabr2.place(x=500,y=620,width=150,height=200)
            #print(self.image.shape," - ",type(self.image.shape[0]))
            label = tk.Label(self.runMenuFrame, image=self.imTk)
            label.place(x=150,y=100,height=404,width=404)
            self.print.place(x=100, y=650, width=200, height=30)
            self.gcode.place(x=100, y=700, width=200, height=30)
            #self.runCnc.place(x=200, y=750, width=300, height=30)
            self.back.place(x=100, y=750, width=200, height=30)
            self.runMenuFrame.place(x=0,y=0,width=700, height=900)
        else:
            font_style = tkFont.Font(family="Helvetica", size=23)
            self.waitLabel=tk.Label(self.runMenuFrame,text= 'En uygun sonuç aranıyor{}'.format(self.waittxt[self.wait%4]),font=font_style,background='#2c7e9c')
            self.waitLabel.place(x=50,y=300,width=600,height=200)
            self.wait=self.wait+1
            self.window.after(100,self.updateRun)
            
if __name__=='__main__':
    run=GUI()