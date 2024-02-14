import numpy as np
import random
import time
import stockCutting
import threading
import copy

class App():
    def __init__(self):
        self.rect=[]
        self.base=[]
        self.solution=[]
        

    def readFile(self,fileName,multipler):
        with open(fileName, 'r') as file:
            content = file.read()  
            list=content.split('\n')
            for i,val in enumerate(list):
                vals=val.split(' ')
                if i == 1 :
                    self.base.append([int(vals[0])*multipler,int(vals[1])*multipler])
                elif(i>1):
                    self.rect.append([int(vals[0])*multipler,int(vals[1])*multipler])
    
    def getGcode(self,filePath):
        filename = r"C:\VsCode\Python\CDTP\Final\C1_1.gcode"
        code="M03 S90\n\nG90 ; Use absolute positioning\nG21 ; Set units to millimeters\nG1 F100 ; Set units to millimeters\n"
        code=code+"G4 P0.5\nG1 X0 Y0\nG4 P0.5\nM03 S150\nG4 P0.5\n"
        
        code=code+"G1 X250 Y0\nG1 X250 Y250\nG1 X0 Y250\nG1 X0 Y0\nM03 S90\nG4 P0.5\nG1 X25 Y25\nG4 P0.5\nM03 S150\nG4 P0.5\n"


        """code=code+"G1 X{} Y{} ;Base\n".format(self.base[0][0],0)
        code=code+"G1 X{} Y{} ;Base\n".format(self.base[0][0],self.base[0][1])
        code=code+"G1 X{} Y{} ;Base\n".format(0,self.base[0][1])
        code=code+"G1 X{} Y{} ;Base\n".format(0,0)
        
        for index, i in enumerate(self.solution):
            code=code+"M03 S90\nG4 P0.5\n"
            code=code+"G1 X{} Y{}\nM03 S150\nG4 P0.5\n".format(i[0],i[1])
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[2],i[1],index)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[2],i[3],index)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[0],i[3],index)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[0],i[1],index)


        code=code+"M03 S250\nG1 X0 Y0\n"""

        code=code+"G1 X{} Y{} ;Base\n".format(self.base[0][0]+25,0+25)
        code=code+"G1 X{} Y{} ;Base\n".format(self.base[0][0]+25,self.base[0][1]+25)
        code=code+"G1 X{} Y{} ;Base\n".format(0+25,self.base[0][1]+25)
        code=code+"G1 X{} Y{} ;Base\n".format(25,25)
        
        for index, i in enumerate(self.solution):
            code=code+"M03 S90\nG4 P0.5\n"
            code=code+"G1 X{} Y{}\nM03 S150\nG4 P0.5\n".format(i[0]+25,i[1]+25)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[2]+25,i[1]+25,index)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[2]+25,i[3]+25,index)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[0]+25,i[3]+25,index)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[0]+25,i[1]+25,index)


        code=code+"M03 S90\nG1 X0 Y0\nM03 S150"

        with open(filePath, 'w') as file:
            # Metni dosyaya yazın
            file.write(code)

    def getGcodeModular(self,filePath):
        frame=self.base[0][0]*1.25
        diff=(frame-self.base[0][0])/2

        code="M03 S90\n\nG90 ; Use absolute positioning\nG21 ; Set units to millimeters\nG1 F1000 ; Set units to millimeters\n"
        code=code+"G4 P0.5\nG1 X0 Y0\nM03 S150\nG4 P0.5\n"
        
        code=code+"G1 X{} Y0\nG1 X{} Y{}\nG1 X0 Y{}\nG1 X0 Y0\nM03 S90\nG4 P0.5\n G1 X{} Y{}\nM03 S150\nG4 P0.5\n".format(frame,frame,frame,frame,diff,diff)

        code=code+"G1 X{} Y{} ;Base\n".format(self.base[0][0]+diff,diff)
        code=code+"G1 X{} Y{} ;Base\n".format(self.base[0][0]+diff,self.base[0][1]+diff)
        code=code+"G1 X{} Y{} ;Base\n".format(diff,self.base[0][1]+diff)
        code=code+"G1 X{} Y{} ;Base\n".format(diff,diff)
        
        for index, i in enumerate(self.solution):
            code=code+"M03 S90\nG4 P0.5\n"
            code=code+"G1 X{} Y{}\nM03 S150\nG4 P0.5\n".format(i[0]+diff,i[1]+diff)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[2]+diff,i[1]+diff,index)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[2]+diff,i[3]+diff,index)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[0]+diff,i[3]+diff,index)
            code=code+"G1 X{} Y{} ;{} Block\n".format(i[0]+diff,i[1]+diff,index)


        code=code+"M03 S{}\nG1 X{} Y{}\n".format(frame,diff,diff)

        with open(filePath, 'w') as file:
            # Metni dosyaya yazın
            file.write(code)

    def getGcodeManual(self,filePath):
        filename = r"C:\VsCode\Python\CDTP\Final\C1_1.gcode"
        code="SU\nG1 X0 Y0 ; 0\nSD\n"

        code=code+"G1 X{} Y{} ;Base\n".format(self.base[0][0]+15,0+15)
        code=code+"G1 X{} Y{} ;Base\n".format(self.base[0][0]+15,self.base[0][1]+15)
        code=code+"G1 X{} Y{} ;Base\n".format(0+15,self.base[0][1]+15)
        code=code+"G1 X{} Y{} ;Base\n".format(15,15)
        
        for index, i in enumerate(self.solution):
            code=code+"SU\n"
            code=code+"G1 X{} Y{}\nSD\n".format(i[0]+15,i[1]+15)
            code=code+"G1 X{} Y{} ;{} \n".format(i[2]+15,i[1]+15,index)
            code=code+"G1 X{} Y{} ;{} \n".format(i[2]+15,i[3]+15,index)
            code=code+"G1 X{} Y{} ;{} \n".format(i[0]+15,i[3]+15,index)
            code=code+"G1 X{} Y{} ;{} \n".format(i[0]+15,i[1]+15,index)


        code=code+"SU\nG1 X0 Y0\n"

        with open(filePath, 'w') as file:
            # Metni dosyaya yazın
            file.write(code)

    def getSol(self,retSol,finished,placed,iterNo,counter):
        tmpRect=self.rect
        sortRect=sorted(tmpRect,key= lambda tmpRect: tmpRect[0]*tmpRect[1],reverse=True)
        self.rect=[]
        for index, i in enumerate(sortRect):
            self.rect.append([sortRect[index][0],sortRect[index][1],-1,-1])
        #iterNo=32000
        #print(usingRect)

        no=1
        #counter=31500
        allRect=[]
        areas=[]
        areas=[0,0,0,0,0]
        maximumArea=0
        bestSol=[]
        maxPlacedIndex=[]
        while(counter < iterNo ):
            tmpRect1=copy.deepcopy(self.rect)
            tmpRect2=copy.deepcopy(self.rect)
            tmpRect3=copy.deepcopy(self.rect)
            tmpRect4=copy.deepcopy(self.rect)
            tmpRect5=copy.deepcopy(self.rect)
            
            #print("----{}----\n".format(counter))
            list1=stockCutting.chngIndex(counter)
            list2=stockCutting.chngIndex(counter + 1)
            list3=stockCutting.chngIndex(counter + 2)
            list4=stockCutting.chngIndex(counter + 3)
            list5=stockCutting.chngIndex(counter + 4)
            #print(list1, list2, list3, list4, list5)
            placedR1=[]
            placedR2=[]
            placedR3=[]
            placedR4=[]
            placedR5=[]

            retRect1=[]
            retRect2=[]
            retRect3=[]
            retRect4=[]
            retRect5=[]

            for i in list1:
                tmp=tmpRect1[i][0]
                tmpRect1[i][0]=tmpRect1[i][1]
                tmpRect1[i][1]=tmp
            #print("\n1",tmpRect1)
            for i in list2:
                tmp=tmpRect2[i][0]
                tmpRect2[i][0]=tmpRect2[i][1]
                tmpRect2[i][1]=tmp
            #print("\n2",tmpRect2)
            for i in list3:
                tmp=tmpRect3[i][0]
                tmpRect3[i][0]=tmpRect3[i][1]
                tmpRect3[i][1]=tmp
            #print("\n3",tmpRect3)
            for i in list4:
                tmp=tmpRect4[i][0]
                tmpRect4[i][0]=tmpRect4[i][1]
                tmpRect4[i][1]=tmp
            #print("\n1",tmpRect4)
            for i in list5:
                tmp=tmpRect5[i][0]
                tmpRect5[i][0]=tmpRect5[i][1]
                tmpRect5[i][1]=tmp




            allRect.append(tmpRect1)
            allRect.append(tmpRect2)
            allRect.append(tmpRect3)
            allRect.append(tmpRect4)
            allRect.append(tmpRect5)
            
            placedIndex1=[]
            placedIndex2=[]
            placedIndex3=[]
            placedIndex4=[]
            placedIndex5=[]

            
            
            th1X=stockCutting.Stock(tmpRect1,200,200,5,5,no)
            th2X=stockCutting.Stock(tmpRect2,200,200,5,5,no)
            th3X=stockCutting.Stock(tmpRect3,200,200,5,5,no)
            th4X=stockCutting.Stock(tmpRect4,200,200,5,5,no)
            th5X=stockCutting.Stock(tmpRect5,200,200,5,5,no)


            th1=threading.Thread(target=th1X.placeRect,args=((counter)%5,areas,placedR1,retRect1,placedIndex1))
            th2=threading.Thread(target=th2X.placeRect,args=((counter+1)%5,areas,placedR2,retRect2,placedIndex2))
            th3=threading.Thread(target=th3X.placeRect,args=((counter+2)%5,areas,placedR3,retRect3,placedIndex3))
            th4=threading.Thread(target=th4X.placeRect,args=((counter+3)%5,areas,placedR4,retRect4,placedIndex4))
            th5=threading.Thread(target=th5X.placeRect,args=((counter+4)%5,areas,placedR5,retRect5,placedIndex5))
            
            th1.start()
            th2.start()
            th3.start()
            th4.start()
            th5.start()

            th1.join()
            th2.join()
            th3.join()
            th4.join()
            th5.join()
            allRect=[]
            allRect.append(retRect1)
            allRect.append(retRect2)
            allRect.append(retRect3)
            allRect.append(retRect4)
            allRect.append(retRect5)
            allPlacedIndex=[]
            allPlacedIndex.append(placedIndex1)
            allPlacedIndex.append(placedIndex2)
            allPlacedIndex.append(placedIndex3)
            allPlacedIndex.append(placedIndex4)
            allPlacedIndex.append(placedIndex5)
            """for i in allRect:
                print(i)"""
            """print(placedR1,len(placedR1))
            print(placedR2,len(placedR2))
            print(placedR3,len(placedR3))
            print(placedR4,len(placedR4))
            print(placedR5,len(placedR5))"""

            counter=counter+5
            """print("Areas=",areas)"""
            maxArea=max(areas)
            maxIndex=areas.index(maxArea)
            #print(allRect[maxIndex])
            """print('max area=',maxArea,'Max array=',allRect[maxIndex])"""
            if(maxArea > maximumArea):
                maximumArea=maxArea
                bestSol=copy.deepcopy(allRect[maxIndex])
                maxPlacedIndex=copy.deepcopy(allPlacedIndex[maxIndex])
            if(maxArea > 39900):
                counter=7000000

            #print("next iter Tamamlandı")
        #print("son")
        #print(bestSol)
        tmp=[]
        print("BEST=",bestSol)
        for index,i in enumerate(bestSol):
            #print('FOR:',index,i)
            tmp.append([i[2],i[3],i[4],i[5]])

        placed.append(maxPlacedIndex)
        retSol.append(tmp)
        #print("Ret")
        #print(retSol)
        finished[0]=1
        self.solution=retSol[0]

if __name__ == '__main__':
    run=App()
    run.readFile(r"C:\VsCode\Python\CDTP\Final\Original\C1_1",10)
    print(run.rect)
    a=[]
    b=[0]
    run.getSol(a,b)
    print(run.rect)

    #run.getSol()
    """run.getInner()
    run.getGcode() """