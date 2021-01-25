import numpy as np
import matplotlib.pyplot as plt
from stationsObjects import*
import copy
import pickle
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

#Global parameters
np.random.seed(4318937)
#np.random.seed(1)
nTrueMuons = 4
nNoise     = 0

reMatchHits  = True
doLaterality = True
agingPercentage = 1
minHits     = 2

#Loads the patterns
fig,ax = plt.subplots(1)
MB1.plot()
plt.axis([0,200,-5,30])

#Now test a set of hits


#Generate true muons and its resulting set of patterns
allHits = []
trueHits = []
trueMuons = []

for n in range(nTrueMuons):
    
    mm          = Muon(np.random.rand()*200,0., 1./((np.random.rand())))
    MB1.checkIn(mm)
    trueHits += mm.getRecoPattern()
    mm.color="g--"
    mm.plot()
    trueMuons.append(mm)

#And now generate a couple of points with random noise
noiseHits = []
for n in range(nNoise):
    noiseHits.append([int(np.ceil(np.random.rand()*8)), int(np.floor(np.random.rand()*47))])

for t in trueHits:
    if np.random.rand() > agingPercentage: continue
    plt.plot(MB1.layers[t[0]-1].DTlist[t[1]].center()[0], MB1.layers[t[0]-1].DTlist[t[1]].center()[1], "gx",markersize=12,linewidth=4)
    allHits.append(t)

for n in noiseHits:
    if n in trueHits: continue
    plt.plot(MB1.layers[n[0]-1].DTlist[n[1]].center()[0], MB1.layers[n[0]-1].DTlist[n[1]].center()[1], "rx",markersize=12,linewidth=4)
    allHits.append(n)    


#Now do the magic

#First sort all hits according to the layer
allHits.sort(key= lambda x: x[0])

#First try to separate them:
print "START: ", allHits


#Now try to match extra hits to existing chosen patterns (+/- 1 cell tolerance)
print "=========================================================="
print "=========================================================="
print "=========================================================="
print "=========================================================="

 
#Plot it

plt.show()

