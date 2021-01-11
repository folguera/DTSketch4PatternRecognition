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
nTrueMuons = 2
nNoise     = 0

reMatchHits  = True
doLaterality = True
agingPercentage = 0.42
minHits     = 2

#Loads the patterns
fig,ax = plt.subplots(1)
MB1patterns = pickle.load(open("MBTrainTraining.pck","r"))
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
usedHits = []
chosenPatterns  = []
testingPatterns = []

#First try to separate them:
h1L = filter(lambda x: x[0] == 1, allHits)
h2L = filter(lambda x: x[0] == 2, allHits)
h3L = filter(lambda x: x[0] == 3, allHits)
h4L = filter(lambda x: x[0] == 4, allHits)
h5L = filter(lambda x: x[0] == 5, allHits)
h6L = filter(lambda x: x[0] == 6, allHits)
h7L = filter(lambda x: x[0] == 7, allHits)
h8L = filter(lambda x: x[0] == 8, allHits)

testPatterns = []

print "START: ", allHits

for h1 in h1L:
    for h2 in h8L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                ##print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                ##print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for p in testPatterns:
    #If maximal length, pick the pattern and delete hits
    layers = [h[0] for h in p[0]]
    layers = list(dict.fromkeys(layers))
    if len(layers) >= 8:
        chosenPatterns.append(copy.deepcopy(p))
        allHits = filter(lambda x: not(x in p[0]), allHits)
        for pp in testPatterns:
            if True:
                pp[0] = filter(lambda x: x in allHits, pp[0])

print "8 Hits: ", allHits, len(chosenPatterns)

h1L = filter(lambda x: x[0] == 1, allHits)
h2L = filter(lambda x: x[0] == 2, allHits)
h3L = filter(lambda x: x[0] == 3, allHits)
h4L = filter(lambda x: x[0] == 4, allHits)
h5L = filter(lambda x: x[0] == 5, allHits)
h6L = filter(lambda x: x[0] == 6, allHits)
h7L = filter(lambda x: x[0] == 7, allHits)
h8L = filter(lambda x: x[0] == 8, allHits)

for h1 in h1L:
    for h2 in h7L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for h1 in h2L:
    for h2 in h8L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for p in testPatterns:
    #If maximal length, pick the pattern and delete hits
    layers = [h[0] for h in p[0]]
    layers = list(dict.fromkeys(layers))
    if len(layers) >= 7:
        chosenPatterns.append(copy.deepcopy(p))
        allHits = filter(lambda x: not(x in p[0]), allHits)
        for pp in testPatterns:
            if True:
                pp[0] = filter(lambda x: x in allHits, pp[0])


print "7 Hits: ", allHits, len(chosenPatterns)


h1L = filter(lambda x: x[0] == 1, allHits)
h2L = filter(lambda x: x[0] == 2, allHits)
h3L = filter(lambda x: x[0] == 3, allHits)
h4L = filter(lambda x: x[0] == 4, allHits)
h5L = filter(lambda x: x[0] == 5, allHits)
h6L = filter(lambda x: x[0] == 6, allHits)
h7L = filter(lambda x: x[0] == 7, allHits)
h8L = filter(lambda x: x[0] == 8, allHits)

for h1 in h1L:
    for h2 in h6L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for h2 in h2L:
    for h2 in h7L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for h1 in h3L:
    for h2 in h8L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for p in testPatterns:
    #If maximal length, pick the pattern and delete hits
    layers = [h[0] for h in p[0]]
    layers = list(dict.fromkeys(layers))
    if len(layers) >= 6:
        chosenPatterns.append(copy.deepcopy(p))
        allHits = filter(lambda x: not(x in p[0]), allHits)
        for pp in testPatterns:
            if True:
                pp[0] = filter(lambda x: x in allHits, pp[0])

print "6 Hits: ", allHits, len(chosenPatterns)


h1L = filter(lambda x: x[0] == 1, allHits)
h2L = filter(lambda x: x[0] == 2, allHits)
h3L = filter(lambda x: x[0] == 3, allHits)
h4L = filter(lambda x: x[0] == 4, allHits)
h5L = filter(lambda x: x[0] == 5, allHits)
h6L = filter(lambda x: x[0] == 6, allHits)
h7L = filter(lambda x: x[0] == 7, allHits)
h8L = filter(lambda x: x[0] == 8, allHits)

for h1 in h1L:
    for h2 in h5L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for h1 in h2L:
    for h2 in h6L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for h1 in h3L:
    for h2 in h7L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for h1 in h4L:
    for h2 in h8L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])


for p in testPatterns:
    #If maximal length, pick the pattern and delete hits
    layers = [h[0] for h in p[0]]
    layers = list(dict.fromkeys(layers))
    if len(layers) >= 5:
        chosenPatterns.append(copy.deepcopy(p))
        allHits = filter(lambda x: not(x in p[0]), allHits)
        for pp in testPatterns:
            if True:
                pp[0] = filter(lambda x: x in allHits, pp[0])

print "5 Hits: ", allHits, len(chosenPatterns)


h1L = filter(lambda x: x[0] == 1, allHits)
h2L = filter(lambda x: x[0] == 2, allHits)
h3L = filter(lambda x: x[0] == 3, allHits)
h4L = filter(lambda x: x[0] == 4, allHits)
h5L = filter(lambda x: x[0] == 5, allHits)
h6L = filter(lambda x: x[0] == 6, allHits)
h7L = filter(lambda x: x[0] == 7, allHits)
h8L = filter(lambda x: x[0] == 8, allHits)

for h1 in h2L:
    for h2 in h5L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for h1 in h3L:
    for h2 in h6L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for h1 in h4L:
    for h2 in h7L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])


for p in testPatterns:
    #If maximal length, pick the pattern and delete hits
    layers = [h[0] for h in p[0]]
    layers = list(dict.fromkeys(layers))
    if len(layers) >= 4:
        chosenPatterns.append(copy.deepcopy(p))
        allHits = filter(lambda x: not(x in p[0]), allHits)
        for pp in testPatterns:
            if True:
                pp[0] = filter(lambda x: x in allHits, pp[0])

print "4 Hits: ", allHits, len(chosenPatterns)





h1L = filter(lambda x: x[0] == 1, allHits)
h2L = filter(lambda x: x[0] == 2, allHits)
h3L = filter(lambda x: x[0] == 3, allHits)
h4L = filter(lambda x: x[0] == 4, allHits)
h5L = filter(lambda x: x[0] == 5, allHits)
h6L = filter(lambda x: x[0] == 6, allHits)
h7L = filter(lambda x: x[0] == 7, allHits)
h8L = filter(lambda x: x[0] == 8, allHits)

for h1 in h3L:
    for h2 in h5L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])

for h1 in h4L:
    for h2 in h6L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])


for p in testPatterns:
    #If maximal length, pick the pattern and delete hits
    layers = [h[0] for h in p[0]]
    layers = list(dict.fromkeys(layers))
    if len(layers) >= 4:
        chosenPatterns.append(copy.deepcopy(p))
        allHits = filter(lambda x: not(x in p[0]), allHits)
        for pp in testPatterns:
            if True:
                pp[0] = filter(lambda x: x in allHits, pp[0])

print "4 Hits: ", allHits, len(chosenPatterns)



h1L = filter(lambda x: x[0] == 1, allHits)
h2L = filter(lambda x: x[0] == 2, allHits)
h3L = filter(lambda x: x[0] == 3, allHits)
h4L = filter(lambda x: x[0] == 4, allHits)
h5L = filter(lambda x: x[0] == 5, allHits)
h6L = filter(lambda x: x[0] == 6, allHits)
h7L = filter(lambda x: x[0] == 7, allHits)
h8L = filter(lambda x: x[0] == 8, allHits)

for h1 in h4L:
    for h2 in h5L:
        testSeed = [h1[0]-1, h2[0]-1 , abs(h1[1]-h2[1])]
        reverse = 1 if h2[1] > h1[1] else -1
        for p in MB1patterns:
            #print p.seeds, testSeed
            if p.seeds == testSeed:
                #print "FOUND"
                hitsinP = filter(lambda x: x in p.recoHits(h1[1], reverse), allHits)
                #print hitsinP
                testPatterns.append( [hitsinP, p, h1[1],reverse])


for p in testPatterns:
    #If maximal length, pick the pattern and delete hits
    layers = [h[0] for h in p[0]]
    layers = list(dict.fromkeys(layers))
    if len(layers) >= 4:
        chosenPatterns.append(copy.deepcopy(p))
        allHits = filter(lambda x: not(x in p[0]), allHits)
        for pp in testPatterns:
            if True:
                pp[0] = filter(lambda x: x in allHits, pp[0])



#print chosenPatterns
print "4 Hits: ", allHits, len(chosenPatterns)


#Now try to match extra hits to existing chosen patterns (+/- 1 cell tolerance)
print "=========================================================="
print "=========================================================="
print "=========================================================="
print "=========================================================="

chosenPatterns.sort(key = lambda x: len(x[0]))

if reMatchHits == True:
  for a in allHits:
    for c in chosenPatterns:
        print a, c[1].recoHits(c[2], c[3])

        if a in c[1].recoHits(c[2], c[3]) or  a in c[1].recoHits(c[2]+1, c[3]) or a in c[1].recoHits(c[2]-1, c[3]):
            c[0].append(a)



colors = ["b", "y", "k", "c", "m"] 
for c in chosenPatterns:
    if len(c[0]) < minHits: continue
    print c
    print c[0]
    print c[1].hits
    print c[2]
    patches  = []
    Lpatches = []
    for hit in c[0]:
        laterality = 0
        #Check if laterality info is available
        expectedHits = c[1].genHits(c[2], c[3])
        for e in expectedHits:
            if hit == e[:2]:
                laterality = e[2]
        #print (MB1.layers[hit[0]-1].DTlist[hit[1]].xmin, MB1.layers[hit[0]-1].DTlist[hit[1]].ymin), MB1.layers[hit[0]-1].DTlist[hit[1]].width, MB1.layers[hit[0]-1].DTlist[hit[1]].height
        patches.append(mpatches.Rectangle((MB1.layers[hit[0]-1].DTlist[hit[1]].xmin, MB1.layers[hit[0]-1].DTlist[hit[1]].ymin), MB1.layers[hit[0]-1].DTlist[hit[1]].width, MB1.layers[hit[0]-1].DTlist[hit[1]].height))       

        if laterality == -1 and doLaterality:
            Lpatches.append(mpatches.Rectangle((MB1.layers[hit[0]-1].DTlist[hit[1]].xmin, MB1.layers[hit[0]-1].DTlist[hit[1]].ymin), MB1.layers[hit[0]-1].DTlist[hit[1]].width/2., MB1.layers[hit[0]-1].DTlist[hit[1]].height)) 

        if laterality ==  1 and doLaterality:
            Lpatches.append(mpatches.Rectangle((MB1.layers[hit[0]-1].DTlist[hit[1]].xmin + MB1.layers[hit[0]-1].DTlist[hit[1]].width/2., MB1.layers[hit[0]-1].DTlist[hit[1]].ymin), MB1.layers[hit[0]-1].DTlist[hit[1]].width/2., MB1.layers[hit[0]-1].DTlist[hit[1]].height)) 
      
    collection = PatchCollection(patches, facecolors = colors[-1], alpha=0.35)
    Lcollection = PatchCollection(Lpatches, facecolors = colors[-1], alpha=0.65)
    ax.add_collection(collection)
    ax.add_collection(Lcollection)
    colors = colors[1:] + colors[0:1]
 
#Plot it

plt.show()

