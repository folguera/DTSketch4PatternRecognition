import numpy as np
import matplotlib.pyplot as plt

globalDTwidth  = 4.2
globalDTheight = 1.3
SLgap = 29 - globalDTheight*8

nDTMB1 = 47
nDTMB2 = 59
nDTMB3 = 73
nDTMB4 = 102

class Muon(object):
    def __init__(self, x0,y0, m):
        self.x0 = x0
        self.y0 = y0
        self.m  = m
        self.cellHits  = []
        self.semicells = []
        self.color = "r-"

    def getY(self, x, ydef):
        if self.m == 100000: 
            return (abs(x - self.x0) < 0.05*globalDTwidth)*ydef + (abs(x - self.x0) > 0.05*globalDTwidth)*10000000000  

        return self.m*(x-self.x0) + self.y0
    def plot(self, xmin = 0., xmax= 600):
        xr = np.linspace(xmin, xmax, 10000)
        plt.plot(xr, self.getY(xr, 0.), self.color)    

    def printHits(self):
        for l in self.cellHits:
            print  l.parent.idx, l.idx

    def getPattern(self):
        self.pattern = []
        for i in range(len(self.cellHits)):
            self.pattern.append([self.cellHits[i].parent.idx, self.cellHits[i].idx, self.semicells[i]])
        return self.pattern

    def getRecoPattern(self):
        self.recopattern = []
        for i in range(len(self.cellHits)):
            self.recopattern.append([self.cellHits[i].parent.idx, self.cellHits[i].idx])
        return self.recopattern

class DT(object):
    def __init__(self,x,y,height,width, parent=0, idx=-1):
        self.xmin = x
        self.ymin = y
        self.height = height
        self.width  = width
        self.idx    = idx
        self.parent = parent
        self.muons  = []
        self.isMIn   = False

    def plot(self, doSemi = True):
        if self.isMIn:
            color = "g-"
        else:
            color = "k-"
        plt.plot([self.xmin, self.xmin + self.width], [self.ymin, self.ymin], color)
        plt.plot([self.xmin, self.xmin + self.width], [self.ymin + self.height, self.ymin + self.height], color)
        plt.plot([self.xmin, self.xmin], [self.ymin, self.ymin+ self.height], color)
        plt.plot([self.xmin + self.width, self.xmin + self.width], [self.ymin, self.ymin+ self.height], color)
        if doSemi:
            plt.plot([self.xmin + 0.5*self.width, self.xmin + 0.5*self.width], [self.ymin, self.ymin+ self.height], "k--")
    def isIn(self, muon):
        semicellIzq = False
        semicellDer = False
        #print "First Checks"
        if max(muon.getY(self.xmin, self.ymin + self.height/2.), muon.getY(self.xmin + self.width, self.ymin + self.height/2.)) < self.ymin or min(muon.getY(self.xmin, self.ymin + self.height/2.), muon.getY(self.xmin + self.width, self.ymin + self.height/2.)) > (self.ymin + self.height) and not(muon.m == 100000): return  
        xr = np.linspace(self.xmin, self.xmin + self.width,100)
        #print "All in"
        yr = muon.getY(xr, self.ymin + self.height/2.)
        self.isMIn = any(np.array([ y >= self.ymin-0.01*self.height and y <= self.ymin+self.height*1.01 for y in yr]))
        xr = np.linspace(self.xmin, self.xmin + self.width/2.,100)
        #print "SemiIzq"
        yr = muon.getY(xr, self.ymin + self.height/2.)
        semicellIzq = any(np.array([ y >= self.ymin and y <= self.ymin+self.height for y in yr]))
        xr = np.linspace(self.xmin+ self.width/2., self.xmin + self.width,100)
        #print "SemiDer"
        yr = muon.getY(xr, self.ymin + self.height/2.)
        semicellDer = any(np.array([ y >= self.ymin and y <= self.ymin+self.height for y in yr]))
        
        if self.isMIn: 
            self.muons.append(muon)
            muon.cellHits.append(self)
            if semicellIzq and semicellDer:
                muon.semicells.append(0.)
            elif semicellIzq:
                muon.semicells.append(-1.)
            elif semicellDer:
                muon.semicells.append(1.)

    def center(self):
        return self.xmin + self.width/2., self.ymin + self.height/2.

class Layer(object):  
    def __init__(self,xoff,yoff,nDTs, along = "X", parent=0, idx=-1, offset=0):
        self.xmin = xoff
        self.ymin = yoff
        self.nDTs = nDTs
        self.along = along
        self.offset = offset
        self.createDTs(nDTs)
        self.parent = parent
        self.idx = idx

    def createDTs(self, nDT, height=globalDTheight, width = globalDTwidth):
        x = self.xmin
        y = self.ymin
        self.DTlist = []
        for i in range(nDT):
            self.DTlist.append(DT(x,y,height, width, self, idx=i-self.offset))
            if self.along == "X":
                x += width
            else:
                y += height            

        if self.along == "X":
                y += height
        else:
                x += width
        self.width = x - self.xmin
        self.height = y - self.ymin

    def plot(self):
        for d in self.DTlist: d.plot()

class MB(object):
    def __init__(self, layers):
        self.layers = layers
    def plot(self):
        for l in self.layers: l.plot()
    def checkIn(self, muon):
        for l in self.layers:
            for d in l.DTlist:
                d.isIn(muon)
      

#We need to add "Fake" cells behind/after for the training
l1 = Layer(0,0,nDTMB1, idx=1)
l2 = Layer(0.5*globalDTwidth,globalDTheight,nDTMB1, idx=2)
l3 = Layer(0,2*globalDTheight,nDTMB1, idx=3)
l4 = Layer(0.5*globalDTwidth,3*globalDTheight,nDTMB1, idx=4)
ll1 = Layer(0,4*globalDTheight + SLgap,nDTMB1, idx=5)
ll2 = Layer(0.5*globalDTwidth,5*globalDTheight + SLgap,nDTMB1, idx=6)
ll3 = Layer(0,6*globalDTheight + SLgap,nDTMB1, idx=7)
ll4 = Layer(0.5*globalDTwidth,7*globalDTheight + SLgap,nDTMB1, idx=8)

MB1 = MB([l1,l2,l3,l4,ll1,ll2,ll3,ll4])

##### Extra things ####
l1 = Layer(0,0,nDTMB2)
l2 = Layer(0.5*globalDTwidth,globalDTheight,nDTMB2)
l3 = Layer(0,2*globalDTheight,nDTMB2)
l4 = Layer(0.5*globalDTwidth,3*globalDTheight,nDTMB2)
ll1 = Layer(0,4*globalDTheight + SLgap,nDTMB2)
ll2 = Layer(0.5*globalDTwidth,5*globalDTheight + SLgap,nDTMB2)
ll3 = Layer(0,6*globalDTheight + SLgap,nDTMB2)
ll4 = Layer(0.5*globalDTwidth,7*globalDTheight + SLgap,nDTMB2)

MB2 = MB([l1,l2,l3,l4,ll1,ll2,ll3,ll4])

l1 = Layer(0,0,nDTMB3)
l2 = Layer(0.5*globalDTwidth,globalDTheight,nDTMB3)
l3 = Layer(0,2*globalDTheight,nDTMB3)
l4 = Layer(0.5*globalDTwidth,3*globalDTheight,nDTMB3)
ll1 = Layer(0,4*globalDTheight + SLgap,nDTMB3)
ll2 = Layer(0.5*globalDTwidth,5*globalDTheight + SLgap,nDTMB3)
ll3 = Layer(0,6*globalDTheight + SLgap,nDTMB3)
ll4 = Layer(0.5*globalDTwidth,7*globalDTheight + SLgap,nDTMB3)

MB3 = MB([l1,l2,l3,l4,ll1,ll2,ll3,ll4])

l1 = Layer(0,0,nDTMB4)
l2 = Layer(0.5*globalDTwidth,globalDTheight,nDTMB4)
l3 = Layer(0,2*globalDTheight,nDTMB4)
l4 = Layer(0.5*globalDTwidth,3*globalDTheight,nDTMB4)
ll1 = Layer(0,4*globalDTheight + SLgap,nDTMB4)
ll2 = Layer(0.5*globalDTwidth,5*globalDTheight + SLgap,nDTMB4)
ll3 = Layer(0,6*globalDTheight + SLgap,nDTMB4)
ll4 = Layer(0.5*globalDTwidth,7*globalDTheight + SLgap,nDTMB4)

MB4 = MB([l1,l2,l3,l4,ll1,ll2,ll3,ll4])

