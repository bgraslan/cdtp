import cv2
import time
import random
import numpy as np
import copy
import threading

class Stock():
    def __init__(self,rectangles,height,width,originX,originY,dtNo):
        self.rectangles=rectangles
        self.maxRectangles=copy.deepcopy(self.rectangles)
        self.baseRectangles=copy.deepcopy(self.rectangles)
        self.maxArea=0
        self.currentArea=0
        self.height=height
        self.width=width
        self.originX=originX
        self.originY=originY
        self.image = np.ones((210, 210, 3), dtype=np.uint8) * 255
        
        self.baseimage=self.image.copy()
        self.dtNo=dtNo

    def calculateNFP(self,mainRectOrigin,mainRect,refRect):
        left=mainRectOrigin[0]-refRect[0]
        right=mainRectOrigin[0]+mainRect[0]
        up=mainRectOrigin[1]-refRect[1]
        down=mainRectOrigin[1]+mainRect[1]
        return left,right,up,down
    
    
    def traverseNFP(self,NFP,rect,img):
        width=NFP[1]-NFP[0]
        len=NFP[3]-NFP[2]
        i =0
        placed=False
        waitkey=50
        plus=10
        while(placed==False):
            while(i<width and placed==False):
                #image=img.copy()
                originRect=(NFP[0]+i,NFP[3])
                rightCorner=(NFP[0]+i+rect[0],NFP[3]+rect[1])
                if(originRect[0]>=self.originX and originRect[1]>=self.originY and originRect[0]+rect[0]<=(self.originX+self.width) and originRect[1]+rect[1]<=(self.originY+self.height) and self.placeCheck(rect,originRect)==True):
                    rect[2]=originRect[0]
                    rect[3]=originRect[1]
                    return(originRect,True)
                """cv2.rectangle(image, (originRect), (rightCorner), (0, 255, 0), thickness=4)
                #cv2.rectangle(image, (NFP[0],NFP[2]), (NFP[1],NFP[3]), (0, 255, 0), thickness=1)
                cv2.imshow('NFP', image)
                cv2.waitKey(waitkey)"""
                i=i+plus
            i=0
            while(i<len and placed==False):
                #image=img.copy()
                originRect=(NFP[1],NFP[2]+i)
                rightCorner=(NFP[1]+rect[0],NFP[2]+rect[1]+i)
                if(originRect[0]>=self.originX and originRect[1]>=self.originY and originRect[0]+rect[0]<=(self.originX+self.width) and originRect[1]+rect[1]<=(self.originY+self.height) and self.placeCheck(rect,originRect)==True):
                    rect[2]=originRect[0]
                    rect[3]=originRect[1]
                    return(originRect,True)
                """cv2.rectangle(image, (originRect), (rightCorner), (0, 255, 255), thickness=4)
                #cv2.rectangle(image, (NFP[0],NFP[2]), (NFP[1],NFP[3]), (0, 255, 0), thickness=1)
                cv2.imshow('NFP', image)
                cv2.waitKey(waitkey)"""
                i=i+plus
            i=0
            while(i<width and placed==False):
                #image=img.copy()
                originRect=(NFP[1]-i,NFP[2])
                rightCorner=(NFP[1]+rect[0]-i,NFP[2]+rect[1])
                if(originRect[0]>=self.originX and originRect[1]>=self.originY and originRect[0]+rect[0]<=(self.originX+self.width) and originRect[1]+rect[1]<=(self.originY+self.height) and self.placeCheck(rect,originRect)==True):
                    rect[2]=originRect[0]
                    rect[3]=originRect[1]
                    return(originRect,True)
                """cv2.rectangle(image, (originRect), (rightCorner), (255, 0, 0), thickness=4)
                #cv2.rectangle(image, (NFP[0],NFP[2]), (NFP[1],NFP[3]), (0, 255, 0), thickness=1)
                cv2.imshow('NFP', image)
                cv2.waitKey(waitkey)"""
                i=i+plus
            i=0
            while(i<len and placed==False):
                #image=img.copy()
                originRect=(NFP[0],NFP[2]+i)
                rightCorner=(NFP[0]+rect[0],NFP[2]+rect[1]+i)
                if(originRect[0]>=self.originX and originRect[1]>=self.originY and originRect[0]+rect[0]<=(self.originX+self.width) and originRect[1]+rect[1]<=(self.originY+self.height) and self.placeCheck(rect,originRect)==True):
                    rect[2]=originRect[0]
                    rect[3]=originRect[1]
                    return(originRect,True)
                """cv2.rectangle(image, (originRect), (rightCorner), (0, 0, 255), thickness=4)
                #cv2.rectangle(image, (NFP[0],NFP[2]), (NFP[1],NFP[3]), (0, 255, 0), thickness=1)
                cv2.imshow('NFP', image)
                cv2.waitKey(waitkey)"""
                i=i+plus
            placed=True
        
        return([-1,-1],False)
    
    def placeCheck(self,rect,originRect):
        i=0
        
        while(self.rectangles[i] != rect):
            
            left,right,up,down=self.calculateNFP([self.rectangles[i][2],self.rectangles[i][3]],[self.rectangles[i][0],self.rectangles[i][1]],[rect[0],rect[1]])
            if(originRect[0]>left and originRect[0]<right):
                if(originRect[1]>up and originRect[1]<down):
                    
                    #time.sleep(1)
                    return False
            i=i+1
        return True
    
    def placeRect(self,itrCounter,areas,plc,retRect,placedIndex):
        self.currentArea=0
        cnt=0
        #retRect=[]
       
        self.rectangles[0]=[self.rectangles[0][0],self.rectangles[0][1],self.originX,self.originY]


        retRect.append([self.rectangles[0][0],self.rectangles[0][1],0,0,self.rectangles[0][0],self.rectangles[0][1]])


        self.currentArea = self.currentArea + self.rectangles[0][0]*self.rectangles[0][1]
        plc.append(cnt)
        
        
        for i in self.rectangles:
            placedIndex.append(0)
        placedIndex[0]=1
        for I,i in enumerate(self.rectangles):
            #print("place",self.rectangles)
            if cnt>0:
                index=0
                bool=False
                rotated=False
                while(self.rectangles[index]!=i and bool==False):
                    j=self.rectangles[index]
                    left,right,up,down=self.calculateNFP([j[2],j[3]],[j[0],j[1]],[i[0],i[1]])
                    #print("xxxx->",j,i,left,right,up,down)
                    im=self.image.copy()
                    
                    placed,bool=self.traverseNFP([left,right,up,down],i,self.image)
                    
                    if(bool):
                        
                        retRect.append([i[0],i[1],placed[0]-self.originX,placed[1]-self.originY,placed[0]+i[0]-self.originX,placed[1]+i[1]-self.originY])
                        placedIndex[I]=1
                        #cv2.rectangle(self.image, (placed), (placed[0]+i[0],placed[1]+i[1]), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), thickness=-1)
                       
                        self.currentArea = self.currentArea + i[0]*i[1]
                        
                        """cv2.imshow('Placing', self.image)
                        cv2.waitKey(50)
                        cv2.destroyAllWindows()"""
                        plc.append(cnt)
                        index=index+1


                    elif(self.rectangles[index+1]==i and rotated==False):
                        tmp=self.rectangles[index+1][0]
                        self.rectangles[index+1][0]=self.rectangles[index+1][1]
                        self.rectangles[index+1][1]=tmp
                        rotated=True
                        index=0
                    else:
                        
                        index=index+1   
            cnt=cnt+1
        #print(itrCounter,self.currentArea)
        areas[itrCounter]=self.currentArea

         
    def optimize(self,iterNo):
        counter=0
        while(counter < iterNo ):
            self.rectangles=copy.deepcopy(self.baseRectangles)
            for i in self.rectangles:
                rnd=random.randint(1, 4)
                if rnd == 3 :
                    tmp=i[0]
                    i[0]=i[1]
                    i[1]=tmp
          
            self.image=self.baseimage.copy()
            self.placeRect(counter + 1)
            if(self.currentArea > self.maxArea):
                self.maxRectangles=copy.deepcopy(self.rectangles)
            counter=counter+1

        cv2.imshow("Final",self.image)
        cv2.waitKey(0)
        





def chngIndex(num):
    list=[]
    zero=0x00
    one=0x01
    cnt=0
    while(num ^ zero != 0):
        
        if(num & one == 0x01):
            list.append(cnt)
        cnt=cnt+1
        num=num>>1
    return list




if __name__ == '__main__':
    rectangles=[[70,120,-1,-1],[80,60,-1,-1],[30,120,-1,-1],[50,70,-1,-1],[50,50,-1,-1],[20,120,-1,-1],[110,20,-1,-1],[30,60,-1,-1],[90,20,-1,-1],[40,40,-1,-1],[30,50,-1,-1],[20,70,-1,-1],[20,60,-1,-1],[30,40,-1,-1],[40,20,-1,-1],[30,20,-1,-1]]
    rectangles2=[[40,10,-1,-1],[40,50,-1,-1],[90,40,-1,-1],[30,50,-1,-1],[30,90,-1,-1],[10,40,-1,-1],[50,30,-1,-1],[40,10,-1,-1],[50,50,-1,-1],[70,20,-1,-1],[90,30,-1,-1],[30,130,-1,-1],[20,80,-1,-1],[150,40,-1,-1],[50,40,-1,-1],[100,60,-1,-1],[70,20,-1,-1]]
    rectangles3=[[40,140,-1,-1],[50,20,-1,-1],[20,20,-1,-1],[90,70,-1,-1],[50,50,-1,-1],[20,50,-1,-1],[70,70,-1,-1],[30,50,-1,-1],[60,50,-1,-1],[30,20,-1,-1],[60,20,-1,-1],[40,60,-1,-1],[60,30,-1,-1],[100,30,-1,-1],[60,30,-1,-1],[100,30,-1,-1]]
    sort2=sorted(rectangles2,key= lambda rectangles2: rectangles2[0]*rectangles2[1],reverse=True)
    sort3=sorted(rectangles3,key= lambda rectangles3: rectangles3[0]*rectangles3[1],reverse=True)
    rectangles5=[[70,120,-1,-1],[30,120,-1,-1],[20,120,-1,-1],[30,60,-1,-1],[80,60,-1,-1],[110,20,-1,-1],[90,20,-1,-1],[20,60,-1,-1],[30,40,-1,-1],[40,20,-1,-1],[40,40,-1,-1],[30,20,-1,-1],[50,70,-1,-1],[50,50,-1,-1],[30,50,-1,-1],[20,70,-1,-1]]
    

    usingRect=rectangles5 
    no=0
    counter=0
    allRect=[]
    areas=[]
    #allRect.append(usingRect)
    """ first=Stock(usingRect,200,200,400,400,3)
    firstTh=threading.Thread(target=first.placeRect,args=(0,areas))
    firstTh.start()"""
    
    iterNo=1000
    #print(usingRect)
    while(counter < iterNo ):
        tmpRect1=copy.deepcopy(usingRect)
        tmpRect2=copy.deepcopy(usingRect)
        tmpRect3=copy.deepcopy(usingRect)
        tmpRect4=copy.deepcopy(usingRect)
        tmpRect5=copy.deepcopy(usingRect)

        #print("----{}----\n".format(counter))
        list1=chngIndex(counter)
        list2=chngIndex(counter + 1)
        list3=chngIndex(counter + 2)
        list4=chngIndex(counter + 3)
        list5=chngIndex(counter + 4)
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
        
        areas.append(0)
        areas.append(0)
        areas.append(0)
        areas.append(0)
        areas.append(0)

        
        
        th1X=Stock(tmpRect1,200,200,5,5,no)
        th2X=Stock(tmpRect2,200,200,5,5,no)
        th3X=Stock(tmpRect3,200,200,5,5,no)
        th4X=Stock(tmpRect4,200,200,5,5,no)
        th5X=Stock(tmpRect5,200,200,5,5,no)


        th1=threading.Thread(target=th1X.placeRect,args=(counter,areas,placedR1,retRect1))
        th2=threading.Thread(target=th2X.placeRect,args=(counter+1,areas,placedR2,retRect2))
        th3=threading.Thread(target=th3X.placeRect,args=(counter+2,areas,placedR3,retRect3))
        th4=threading.Thread(target=th4X.placeRect,args=(counter+3,areas,placedR4,retRect4))
        th5=threading.Thread(target=th5X.placeRect,args=(counter+4,areas,placedR5,retRect5))
        
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
        """print(placedR1,len(placedR1))
        print(placedR2,len(placedR2))
        print(placedR3,len(placedR3))
        print(placedR4,len(placedR4))
        print(placedR5,len(placedR5))"""

        counter=counter+5
        print("Areas=",areas)
        print("Tamamlandı")
