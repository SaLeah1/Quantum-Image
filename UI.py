# 255 is white
# #ffffff is white

from tkinter import *
import random
import math

grays = ["#ffffff","#f6f6f6","#ececec","#e3e3e3",
         "#dadada","#d1d1d1","#c8c8c8","#bfbfbf",
         "#b6b6b6","#aeaeae","#a5a5a5","#9c9c9c",
         "#949494","#8c8c8c","#838383","#7b7b7b",
         "#737373","#6b6b6b","#636363","#5b5b5b",
         "#535353","#4c4c4c","#444444","#3d3d3d",
         "#363636","#2f2f2f","#282828","#212121",
         "#1b1b1b","#141414","#0c0c0c","#000000"]
grays.reverse()

class mainWindow:

    root = None
    canvas = None
    fishBot = None

    pxHold = []
    pxZones = []
    pxColors = []
    pxSquareSize = 100
    xOffset = 250
    yOffset = 50

    colorSpaceHold = []
    colorSpaceZones = []
    colorSpaceColors = []
    colorSquareSize = 50
    colorView = None
    selectedColor = "#ffffff"
    cxOffset = 25
    cyOffset = 50

    def __init__(self) -> None:
        self.fishBot = fishReader()
        return
    
    def initWindow(self):
        self.root = Tk()
        self.root.title(self.fishBot.getFishQuote())
        self.root.geometry("1000x600")

        self.canvas = Canvas(self.root, width=1000, height=600)

        self.root.bind("<Button-1>",self.lMouseClick)

    def drawUpPxSpace(self):
        for y in range(5):
            for x in range(5):
                self.pxZones.append((self.xOffset+(x*self.pxSquareSize),self.yOffset+(y*self.pxSquareSize),self.xOffset+100+(x*self.pxSquareSize),self.yOffset+100+(y*self.pxSquareSize)))
                self.pxColors.append("#000000")
                hold = self.canvas.create_rectangle(self.xOffset+(x*self.pxSquareSize),self.yOffset+(y*self.pxSquareSize),self.xOffset+100+(x*self.pxSquareSize),self.yOffset+100+(y*self.pxSquareSize),fill="black", outline="gray")
                self.pxHold.append(hold)
        self.canvas.pack()
    
    def drawUpColorSpace(self):
        colorSpaceCounter = 0
        for y in range(8):
            for x in range(4):
                self.colorSpaceZones.append((self.cxOffset+(x*self.colorSquareSize),self.cyOffset+(y*self.colorSquareSize),self.cxOffset+self.colorSquareSize+(x*self.colorSquareSize),self.cyOffset+self.colorSquareSize+(y*self.colorSquareSize)))
                self.colorSpaceColors.append(grays[colorSpaceCounter])
                hold = self.canvas.create_rectangle(self.cxOffset+(x*self.colorSquareSize),self.cyOffset+(y*self.colorSquareSize),self.cxOffset+self.colorSquareSize+(x*self.colorSquareSize),self.cyOffset+self.colorSquareSize+(y*self.colorSquareSize),fill=grays[colorSpaceCounter],outline="gray")
                self.colorSpaceHold.append(hold)
                colorSpaceCounter += 1
        self.canvas.pack()
        self.colorView = self.canvas.create_rectangle(self.cxOffset+((x-2.5)*self.colorSquareSize),self.cyOffset+(1.5)*self.colorSquareSize+(y*self.colorSquareSize),self.cxOffset+self.colorSquareSize+((x-0.5)*self.colorSquareSize),self.cyOffset+(3.5)*self.colorSquareSize+(y*self.colorSquareSize),fill = self.selectedColor, outline = "gray")

    def setPxColor(self, pxID):
        pxInfo = self.pxZones[pxID]
        print("create px#%d with info: %d %d %d %d"%(pxID,pxInfo[0],pxInfo[1],pxInfo[2],pxInfo[3]))
        self.canvas.itemconfig(self.pxHold[pxID], fill = self.selectedColor)
        self.pxColors[pxID] = self.selectedColor

    def updateColorView(self):
        self.canvas.itemconfig(self.colorView, fill = self.selectedColor)

    def startWindow(self):
        self.root.mainloop()

    # !! Bind Event Calls
    def lMouseClick(self, event):
        print("Left Mouse Click At %d , %d"%(event.x,event.y))
        # check if in drawing zone
        if event.x>self.xOffset and event.x<self.xOffset+(5*self.pxSquareSize) and event.y>self.yOffset and event.y<self.yOffset+(5*self.pxSquareSize):
            xCoord = math.floor((event.x-self.xOffset)/self.pxSquareSize)
            yCoord = math.floor((event.y-self.yOffset)/self.pxSquareSize)
            pxID = (5*yCoord)+xCoord
            print("%d: %d, %d"%(pxID,xCoord,yCoord))
            self.setPxColor(pxID)
        # check if in color space
        if event.x>self.cxOffset and event.x<self.cxOffset+(4*self.colorSquareSize) and event.y>self.cyOffset and event.y<self.cyOffset+(8*self.colorSquareSize):
            xCoord = math.floor((event.x-self.cxOffset)/self.colorSquareSize)
            yCoord = math.floor((event.y-self.cyOffset)/self.colorSquareSize)
            colorID = (4*yCoord)+xCoord
            self.selectedColor = self.colorSpaceColors[colorID]
            self.updateColorView()
            print("%d: %d, %d"%(colorID,xCoord,yCoord))
        
    # !! Pass Calls
    def getColorArray(self):
        return self.pxColors()


# !! other non-class non-bind functions

def gVal2hex(gVal):
    return f'#{gVal:02x}{gVal:02x}{gVal:02x}'

class fishReader:

    fishQuotes = []

    def __init__(self) -> None:
        file = open("auxFiles\FishTime.txt","r", encoding="utf-8")
        for fishQuote in file:
            self.fishQuotes.append(fishQuote)

    def getFishQuote(self):
        return random.choice(self.fishQuotes)
    
#~~~~~

c = mainWindow()
c.initWindow()
c.drawUpPxSpace()
c.drawUpColorSpace()
c.startWindow()