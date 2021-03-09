import numpy as nmp
import time


startTime=time.clock()

global globalMaxSPLA
global globalMaxLAHSA
inputfile = open("input.txt")
beds=int(inputfile.readline())
parkings=int(inputfile.readline())
lahsaAppNum=int(inputfile.readline())
lahsa=nmp.zeros((7,), dtype=int)
lahsaDict={}
for i in range(lahsaAppNum):
        x=int(inputfile.readline())
        lahsaDict[x]=True
splaAppNum=int(inputfile.readline())
spla=nmp.zeros((7,), dtype=int)
splaDict={}
for i in range(splaAppNum):
        x=int(inputfile.readline())
        splaDict[x]=True
totalApp=int(inputfile.readline())

splaComp={}
lahsaComp={}
bothComp={}
bothCompSPLA={}
bothCompLAHSA={}
allApp={}
allAppIDs={}
j=0

globalMaxSPLA=-1
globalMaxLAHSA=-1
#record current values

for i in range(totalApp):
        currApp=inputfile.readline()
        currApp=currApp.rstrip()
        currid=int(currApp[:5])
        if currid in lahsaDict:
                for i in range(7):
                        lahsa[i]+=int(currApp[i+13])
        elif currid in splaDict:
                for i in range(7):
                        spla[i]+=int(currApp[i+13])
        else:
                allApp[j]=currApp
                j+=1
                
   
#check which candidate qualifies for which
for q in range(j):
        currApp=allApp[q]
        flag1=True
        flag2=True
        inSPLA=False
        inLAHSA=False
        for i in range(7):
                y=spla[i]+int(currApp[i+13])
                if y>parkings:
                        flag1=False
                        break
        for i in range(7):
                y=lahsa[i]+int(currApp[i+13])
                if y>beds:
                        flag2=False
                        break
        sumDays=0
        for i in range(7):
                sumDays+=int(currApp[i+13])
        inSPLA=False
        inLAHSA=False
        if currApp[10]=='N' and currApp[11]=='Y' and currApp[12]=='Y' and flag1==True:
                splaComp[currApp[:5]]=sumDays
                allAppIDs[currApp[:5]]=currApp[-7:]
                inSPLA=True
        if currApp[9]=='N' and currApp[5]=='F' and (int(currApp[6:-11]))>17 and flag2==True: 
                lahsaComp[currApp[:5]]=sumDays
                allAppIDs[currApp[:5]]=currApp[-7:]
                inLAHSA=True
        if inSPLA and inLAHSA:
                bothCompSPLA[currApp[:5]]=sumDays
                bothCompLAHSA[currApp[:5]]=sumDays

#------------------------------------------------SPLA------------------------------------------
def initialCall(splaComp,lahsaComp,bothCompSPLA,bothCompLAHSA,spla,lahsa):
        maxToReturn=-1
        if not splaComp:
                bestID=-1
        nodesToReconsider={}
        global globalMaxSPLA
        reversedBothCompSPLA = {}
        reversedSplaComp={}
        if bothCompSPLA:
                for x, y in bothCompSPLA.iteritems():
                        reversedBothCompSPLA.setdefault(y, []).append(x)
        for x, y in splaComp.iteritems():
                reversedSplaComp.setdefault(y, []).append(x)
        
        while splaComp: ### need to continue
                flag=False
                inBothCompSPLA=False
                if bothCompSPLA:
                        val=max(bothCompSPLA.values())
                        selected=min(reversedBothCompSPLA[val])
                        reversedBothCompSPLA[val].remove(selected)
                        reversedSplaComp[val].remove(selected)
                        ntr=bothCompSPLA[selected]
                        del bothCompSPLA[selected]
                        del splaComp[selected]
                        inBothCompSPLA=True
                else:
                        val=max(splaComp.values())
                        selected=min(reversedSplaComp[val])
                        reversedSplaComp[val].remove(selected)
                        ntr=splaComp[selected]
                        del splaComp[selected]
                
                        
                cont=False
                for i in range(7):
                        if spla[i]==parkings and int(allAppIDs[selected][i])==1:
                                cont=True
                                break
                if cont:
                        continue

                currApp=allAppIDs[selected]
                mySplaSum=0
                for i in range(7):
                        spla[i]+=int(currApp[i])
                        mySplaSum+=spla[i]
                if splaComp and globalMaxSPLA>(mySplaSum+(max(splaComp.values())*len(splaComp))):
                                break
                        
                if selected in lahsaComp:
                        v=lahsaComp[selected]
                        del lahsaComp[selected]
                        del bothCompLAHSA[selected]
                        flag=True

                #Find full days      
                fullDays={}
                for i in range(7):
                        if spla[i]==parkings:
                                fullDays[i]=True

                #merge two to reconsider other nodes
                bothCompSPLAMod=dict(bothCompSPLA.items()+nodesToReconsider.items())
                splaCompMod=dict(splaComp.items()+nodesToReconsider.items())
                splaCompMod2=splaCompMod.copy() # is copy nesessary here?
                #remove incompatible ones:
                for i in fullDays: #I'm only checking days that are full.
                        for key in splaCompMod2:
                                if key in splaCompMod and int(allAppIDs[key][i])==1:
                                        del splaCompMod[key]
                                        if key in bothCompSPLAMod:
                                                del bothCompSPLAMod[key]
                splaSum,lahsaSum=myRecCall(1,splaCompMod,lahsaComp.copy(),bothCompSPLAMod,bothCompLAHSA.copy(),spla.copy(),lahsa,False)
                if flag:
                        lahsaComp[selected]=v
                        bothCompLAHSA[selected]=v
                        
                for i in range(7):
                        spla[i]-=int(currApp[i])

                if splaSum>maxToReturn:
                        maxToReturn=splaSum
                        bestID=selected
                elif splaSum==maxToReturn:
                        if int(bestID)>int(selected):
                                bestID=selected
                nodesToReconsider[selected]=ntr
        return bestID
#---------------------------------END-OF-INITIAL-CALL------------------------------
def myRecCall(depth,splaComp,lahsaComp,bothCompSPLA,bothCompLAHSA,spla,lahsa,isSPLA):
        #Stopping condition
        global globalMaxLAHSA
        global globalMaxSPLA
        bestID=100000
        if not splaComp and not lahsaComp:
                splaSum=0
                lahsaSum=0
                
                for i in range(7):
                        splaSum+=spla[i]
                for j in range(7):
                        lahsaSum+=lahsa[j]

                if globalMaxSPLA<splaSum:
                        globalMaxSPLA=splaSum
                if globalMaxLAHSA<lahsaSum:
                        globalMaxLAHSA=lahsaSum
                return splaSum,lahsaSum

        maxToReturn=-1
        nodesToReconsider={}
        if (isSPLA and splaComp) or (not isSPLA and not lahsaComp) : ##what if spla is done?
                reversedBothCompSPLA = {}
                reversedSplaComp={}
                if bothCompSPLA:
                        for x, y in bothCompSPLA.iteritems():
                                reversedBothCompSPLA.setdefault(y, []).append(x)
                for x, y in splaComp.iteritems():
                        reversedSplaComp.setdefault(y, []).append(x)
                while splaComp:
                        flag=False
                        inBothCompSPLA=False

                        if bothCompSPLA:
                                val=max(bothCompSPLA.values())
                                selected=min(reversedBothCompSPLA[val])
                                reversedBothCompSPLA[val].remove(selected)
                                reversedSplaComp[val].remove(selected)
                                ntr=bothCompSPLA[selected]
                                del bothCompSPLA[selected]
                                del splaComp[selected]
                                inBothCompSPLA=True
                        else:
                                val=max(splaComp.values())
                                selected=min(reversedSplaComp[val])
                                reversedSplaComp[val].remove(selected)
                                ntr=splaComp[selected]
                                del splaComp[selected]


                        #is this step nessesary? yeah...for 
                        cont=False
                        for i in range(7):
                                if spla[i]==parkings and int(allAppIDs[selected][i])==1:
                                        cont=True
                                        break
                        if cont:
                                continue

                        currApp=allAppIDs[selected]
                        mySplaSum=0
                        for i in range(7):
                                spla[i]+=int(currApp[i])
                                mySplaSum+=spla[i]
                        if splaComp and globalMaxSPLA>(mySplaSum+(max(splaComp.values())*len(splaComp))):
                                        break

                        #remove temporarily from lahsa candidates
                        if selected in lahsaComp:
                                v=lahsaComp[selected]
                                del lahsaComp[selected]
                                del bothCompLAHSA[selected]
                                flag=True


                        #Find full days      
                        fullDays={}
                        for i in range(7):
                                if spla[i]==parkings:
                                        fullDays[i]=True

                        #merge two to reconsider other nodes
                        bothCompSPLAMod=dict(bothCompSPLA.items()+nodesToReconsider.items())
                        splaCompMod=dict(splaComp.items()+nodesToReconsider.items())
                        splaCompMod2=splaCompMod.copy() # is copy nesessary here?

                        #remove incompatible ones:
                        for i in fullDays: #I'm only checking days that are full.
                                for key in splaCompMod2:
                                        if key in splaCompMod and int(allAppIDs[key][i])==1:
                                                del splaCompMod[key]
                                                if key in bothCompSPLAMod:
                                                        del bothCompSPLAMod[key]

                        splaSum,lahsaSum=myRecCall(depth+1,splaCompMod,lahsaComp.copy(),bothCompSPLAMod,bothCompLAHSA.copy(),spla.copy(),lahsa,False)
                        
                        if flag:
                                bothCompLAHSA[selected]=v ##//why not just put =ntr? next line too?
                                lahsaComp[selected]=v

                        
                        for i in range(7):
                                spla[i]-=int(currApp[i])

                        if splaSum>maxToReturn:
                                maxToReturn=splaSum
                                lahsaToReturn=lahsaSum
                                bestID=selected
                        elif splaSum==maxToReturn:
                                if int(bestID)>int(selected):
                                        bestID=selected
                                        lahsaToReturn=lahsaSum
                                
                        nodesToReconsider[selected]=ntr
                if maxToReturn==-1:
                        lahsaToReturn=-1
                return maxToReturn, lahsaToReturn
#------------------------------------------Lahsa------------------------------------------------
        else:##what is lahsa is done?
                reversedBothCompLAHSA = {}
                reversedLahsaComp={}
                if bothCompLAHSA:
                        for x, y in bothCompLAHSA.iteritems():
                                reversedBothCompLAHSA.setdefault(y, []).append(x)
                for x, y in lahsaComp.iteritems():
                        reversedLahsaComp.setdefault(y, []).append(x)
                while lahsaComp:
                        flag=False
                        inBothCompLAHSA=False
                        if bothCompLAHSA:
                                val=max(bothCompLAHSA.values())
                                selected=min(reversedBothCompLAHSA[val])
                                reversedBothCompLAHSA[val].remove(selected)
                                reversedLahsaComp[val].remove(selected)
                                ntr=bothCompLAHSA[selected]
                                del bothCompLAHSA[selected]
                                del lahsaComp[selected]
                                inBothCompLAHSA=True
                        else:
                                val=max(lahsaComp.values())
                                selected=min(reversedLahsaComp[val])
                                reversedLahsaComp[val].remove(selected)
                                ntr=lahsaComp[selected]
                                del lahsaComp[selected]
   
                        #is this step nessesary?
                        cont=False
                        for i in range(7):
                                if lahsa[i]==beds and int(allAppIDs[selected][i])==1:
                                        cont=True
                                        break
                        if cont:
                                continue
                        currApp=allAppIDs[selected]
                        myLahsaSum=0
                        for i in range(7):
                                lahsa[i]+=int(currApp[i])
                                myLahsaSum+=lahsa[i]
                        if lahsaComp and globalMaxLAHSA>(myLahsaSum+(max(lahsaComp.values())*len(lahsaComp))):
                                        break
                       
                        #remove temporarily from lahsa candidates
                        if selected in splaComp:
                                v=splaComp[selected]
                                del splaComp[selected]
                                del bothCompSPLA[selected]
                                flag=True

                        #Find full days      
                        fullDays={}
                        for i in range(7):
                                if lahsa[i]==beds:
                                        fullDays[i]=True

                        #merge two to reconsider other nodes
                        lahsaCompMod=dict(lahsaComp.items()+nodesToReconsider.items())
                        bothCompLAHSAMod=dict(bothCompLAHSA.items()+nodesToReconsider.items())
                        lahsaCompMod2=lahsaCompMod.copy() # is copy nesessary here?
                        #remove incompatible ones:
                        for i in fullDays: #I'm only checking days that are full.
                                for key in lahsaCompMod2:
                                        if key in lahsaCompMod and int(allAppIDs[key][i])==1:
                                                del lahsaCompMod[key]
                                                if key in bothCompLAHSAMod:
                                                        del bothCompLAHSAMod[key]

                        splaSum,lahsaSum=myRecCall(depth+1,splaComp.copy(),lahsaCompMod,bothCompSPLA.copy(),bothCompLAHSAMod,spla,lahsa.copy(),True)
                        if flag:
                                splaComp[selected]=v
                                bothCompSPLA[selected]=v
                        
                        for i in range(7):
                                lahsa[i]-=int(currApp[i])

                        if lahsaSum>maxToReturn:
                                maxToReturn=lahsaSum
                                splaToReturn=splaSum
                                bestID=selected
                        elif lahsaSum==maxToReturn:
                                if int(bestID)>int(selected):
                                        bestID=selected
                                        splaToReturn=splaSum
                                
                        nodesToReconsider[selected]=ntr
                if maxToReturn==-1:
                        splaToReturn=-1
                return splaToReturn, maxToReturn

        
x=initialCall(splaComp,lahsaComp,bothCompSPLA, bothCompLAHSA,spla,lahsa)


outputfile = open("output.txt","w")
outputfile.write(x)
outputfile.close()
