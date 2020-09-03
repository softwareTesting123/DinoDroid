
#import strand
import re
from xml.dom.minidom import Document
from xml.dom import minidom
from __builtin__ import True
import random
import numpy as np

def checkImportant(lastFeatureTuple, lastActionIndex, lastFeature):
    similarMatrix=lastFeatureTuple[2]
    
    if similarMatrix[lastActionIndex][0]>0:
        return "important is true"
        
    outPutStr=""
    
    
    lastRoot=lastFeature.root_Result
    className=lastRoot.getElementsByTagName("Classname")[0].firstChild.nodeValue
    
    outPutStr+=className
    
    oneRunableFeature=lastFeature.runableList[lastActionIndex]
    outPutStr+=oneRunableFeature.viewName
    outPutStr+=oneRunableFeature.ownId
    outPutStr+=oneRunableFeature.text
    outPutStr+=oneRunableFeature.index

    return outPutStr
    
    
    '''
    lastRootEasyoperate=lastRoot.getElementsByTagName("Easyoperate")[0]

    eleList=lastRootEasyoperate.childNodes
    
    eleLast=eleList[lastActionIndex]
    
    
    if eleLast.hasAttribute("tag")
    '''
def compareSimiar(beforeResult, newRoot, tag):
    
    sameTag=True
    similarTag=False    
    ###################3check the noListView
    checkListBefore=beforeResult.childNodes
    checkListNew=newRoot.childNodes
    
    beforeLen=len(checkListBefore)
    
    ##################store old list view
    beforeDict={}
    #idDict={}###this is just for the similar case, key is the new id, value is the old id.
    newIdtobeIdDict={}##this is just for the similar case, key is the new id, value is the old id.
    
    newListBol=False
    oldListBol=False
    
    #########################
    newDefaultBol=False
    oldDefaultBol=False
    
    noListnumBefore=0###summarize the no list and default number, in case of different number of the clickable event list
    for i in range(0,len(checkListBefore)):#############check the before
        beforeEvent=checkListBefore[i]
        tagStr=beforeEvent.getAttribute("tag")
        if tagStr.startswith("list") :
            beforeDict[tagStr]=beforeEvent.getAttribute("id")
            oldListBol=True
        elif  tagStr.startswith("default"):
            beforeDict[tagStr]=beforeEvent.getAttribute("id")
            oldDefaultBol=True
        else:
            noListnumBefore+=1
               
    
    #################compare with new
    noListnumNew=0
    firstListBol=True
    for i in range(0,len(checkListNew)):
        
        eventNewEle=checkListNew[i]
    
        tagNewStr=eventNewEle.getAttribute("tag").strip()
        
        if tagNewStr.startswith("normal"):
            noListnumNew+=1
            #############compare structure
            if i>=beforeLen or not checkListBefore[i].getAttribute("tag").strip()==tagNewStr.strip():
                sameTag=False
                similarTag=False
                return sameTag, similarTag, newIdtobeIdDict
            
            ############compare text
            oldText=checkListBefore[i].getAttribute("text").strip()
            newText=eventNewEle.getAttribute("text").strip()
            if not oldText==newText and ( bool(re.search('[a-zA-Z]', oldText) ) or bool ( re.search('[a-zA-Z]', newText)) ):
                sameTag=False
                similarTag=True
                '''
                similarTag=False###the other returns may have similarTag=false as output   #modify it 7.31.2020 for aka, different configure and play at same page
                return sameTag, similarTag, newIdtobeIdDict #modify it 7.31.2020 for aka before fix 64% after fix 82%
                '''
            else:
                newIdtobeIdDict[i]=i
            
        elif tagNewStr.startswith("special"):
            noListnumNew+=1
            #############compare structure
            if i>=beforeLen or not checkListBefore[i].getAttribute("tag").strip()==tagNewStr:
                sameTag=False
                similarTag=False
                return sameTag, similarTag,newIdtobeIdDict

            newIdtobeIdDict[i]=i
            #beIdtoNewIdDict[beforeDict[tagNewStr]]=[eventNewEle.getAttribute("id")]


        elif tagNewStr.startswith("list"):
            newListBol=True
            
            if firstListBol:#### if new is at first list and old is not. return all false
                firstListBol=False
                if i>=beforeLen or not checkListBefore[i].getAttribute("tag").startswith("list"):
                    sameTag=False
                    similarTag=False
                    return sameTag, similarTag,newIdtobeIdDict 
            
            #############compare structure
            if i>=beforeLen or not checkListBefore[i].getAttribute("tag").strip()==tagNewStr:###just check current and before is same or not at this event
                sameTag=False
                similarTag=True
            
                if tagNewStr in beforeDict:
                    newIdtobeIdDict[int(eventNewEle.getAttribute("id"))]=int(beforeDict[tagNewStr])
            else:
                newIdtobeIdDict[i]=i
                #beIdtoNewIdDict[beforeDict[tagNewStr]]=[eventNewEle.getAttribute("id")]

        elif tagNewStr.startswith("default"):       
            newDefaultBol=True     
            break
           
    if not len(checkListBefore)==len(checkListNew):
        sameTag=False
        
    if newDefaultBol^oldDefaultBol or newListBol^oldListBol:
        sameTag=False
        similarTag=False
        return sameTag, similarTag,newIdtobeIdDict
           
    if not noListnumNew==noListnumBefore:
        sameTag=False
        similarTag=False
        return sameTag, similarTag,newIdtobeIdDict
    return sameTag, similarTag,newIdtobeIdDict
    
    

def getSimilar(wholeRoot,newRoot):
    sameStr=""
    similarStrList=[]
    sameEvent=None
    similarEventList=[]
    
    newRootEasyoperate=newRoot.getElementsByTagName("Easyoperate")[0]
    
    for beforeResult in wholeRoot.childNodes:#beforeResult means histroy node
        '''
        if beforeResult.getAttribute("id")=="36":
            print("bingo")
        '''
        simiarCount=[0]
        beforeEasyoperate=beforeResult.getElementsByTagName("Easyoperate")[0]
        #newRoot=newRoot.getElementsByTagName("Easyoperate")[0]
        #compareResult=compareSimiar(beforeResult,newRoot,simiarCount, "normal")
        
        if beforeResult.getElementsByTagName("Classname")[0].firstChild.nodeValue==newRoot.getElementsByTagName("Classname")[0].firstChild.nodeValue:
            sameTag, similarTag, newIdtobeIdDict=compareSimiar(beforeEasyoperate,newRootEasyoperate,simiarCount)
        
        
            if sameTag==True:
                sameStr=beforeResult.getAttribute("sameEx")
                sameEvent=beforeResult
                similarStrList.append((beforeResult.getAttribute("similarEx"), newIdtobeIdDict))
            
            elif similarTag==True:
                similarEventList.append((beforeResult,newIdtobeIdDict))
                similarStrList.append((beforeResult.getAttribute("similarEx"), newIdtobeIdDict))
        
    sameResult=[]
    similarResult=[]
    
    
    ###########compute the runNum for the new one, it is easy to be understood in the coding but waste effienent
    newRunAbleNum=0
    checkListNew=newRootEasyoperate.childNodes
    for i in range(0,len(checkListNew)):#############check the before
        beforeEvent=checkListNew[i]
        tagStr=beforeEvent.getAttribute("tag")
        if tagStr.startswith("default"):
            break
        newRunAbleNum+=1
    
    
    
    #############string process from "1;2;3" to [1,2,3] pick the max value for all similar results
    #newRunAbleNum=len(newRootEasyoperate.childNodes)
    
    for index in range(0,newRunAbleNum):
        similarResult.append(0)
    
    
    if similarStrList:
        for oneSimilar,newIdtobeIdDict in similarStrList:####pick the maximum similarity
            itemList=oneSimilar.split(";")#
            
            for newIndex in range(0,len(similarResult)):
                if newIndex in newIdtobeIdDict:
                    oldIndex=newIdtobeIdDict[newIndex]
                    
                    oldSimVal=int(itemList[oldIndex])
                    '''
                    try:
                        oldSimVal=int(itemList[oldIndex])
                    except:
                        print("eeor")
                    '''
                    if similarResult[newIndex]<oldSimVal:
                        similarResult[newIndex]=oldSimVal
                        ###############
    
    if not sameStr=="":
        itemList=sameStr.split(";")
        for itemStr in itemList:
            sameResult.append(int(itemStr))
    
    
        
    return sameEvent,similarEventList,sameResult,similarResult
    
        
    '''
        if sameTag==True:#means similar or same
            if simiarCount[0]==0:#means just same
                sameStr=beforeResult.getAttribute("sameEx")
                sameEvent=beforeResult
                
                
            else:#means just similar
                #similarStrList.append(beforeResult.getAttribute("similarEx"))
                
                similarEventList.append(beforeResult)
            
            similarStrList.append(beforeResult.getAttribute("similarEx"))########similarEventList should update both same and similar, then the similar will be bigger than the same all the time
        
    
    sameResult=[]
    similarResult=[]
    
    
    
    #############string process from "1;2;3" to [1,2,3] pick the max value for all similar results
    
    if similarStrList:
    
        stepsNum=len(similarStrList[0].split(";"))
        
        
        for index in range(0,stepsNum):
            similarResult.append(0)
        
               
        for oneSimilar in similarStrList:
            itemList=oneSimilar.split(";")
            for index in range(0,stepsNum):
                if int(itemList[index])> similarResult[index]:
                    similarResult[index]=int(itemList[index])
    
    if not sameStr=="":
        itemList=sameStr.split(";")
        for itemStr in itemList:
            sameResult.append(int(itemStr))
    
        
        
    return sameEvent,similarEventList,sameResult,similarResult
    '''
def addToRecordRoot(recordRoot, root_Result,resultId,feature,featureStepNum,actionIndex,sameEvent, similarEventList, lastEventInRecord, restartTag, lastSimilarEleList):
    transferChanged=False
    
    root_Result.setAttribute("id",str(resultId))##########add an id
    resultId+=1
    
    #############similar
    similarHisStr=""
    for i in range(featureStepNum):
        if i==actionIndex:
            similarHisStr+=str(feature.similarResultList[i]+1)+";"
        else:
            similarHisStr+=str(feature.similarResultList[i])+";"
            
    ###########same
    sameHisStr=""
    for i in range(featureStepNum):
        if i==actionIndex:
            sameHisStr+=str(feature.sameResultList[i]+1)+";"
        else:
            sameHisStr+=str(feature.sameResultList[i])+";"
            
    
    #######
    similarHisStr=similarHisStr[:-1]#remove the last ;
    sameHisStr=sameHisStr[:-1]#remove the last ; 
    resultEventRecord=None
    
    if feature.sameExist:
        sameEvent.setAttribute("similarEx",similarHisStr)
        sameEvent.setAttribute("sameEx",sameHisStr)
        resultEventRecord=sameEvent
        
    else:
        root_Result.setAttribute("similarEx",similarHisStr)
        root_Result.setAttribute("sameEx",sameHisStr)##########add same
        
        recordRoot.appendChild(root_Result)
        resultEventRecord=root_Result

    selectedSimEleList=updateAllSimilar(similarEventList, actionIndex, resultEventRecord)#both similar  and transfer
    
   
    ####updateSimilarID
    thisResultId=resultEventRecord.getAttribute("id")
   
    if not feature.sameExist:
        updateSimilarID(similarEventList,thisResultId, resultEventRecord)
   
    ######################update last time event for transfer
        
   
    
    if lastEventInRecord:
        
        if lastEventInRecord.hasAttribute("transfer"):
            lastTransferId=lastEventInRecord.getAttribute("transfer")
            if not lastTransferId=="currentUnknown":
                if not lastTransferId==thisResultId:
                    transferChanged=True
        
        
        lastEventInRecord.setAttribute("transfer",thisResultId)
        '''
        if not restartTag:
            
            
            lastEventInRecord.setAttribute("transfer",thisResultId)
            
            #updateLastSimilar(lastSimilarEleList)
            
        else:
            lastEventInRecord.setAttribute("transfer","restart")
        
            
            #updateLastSimilar(lastSimilarEventList,)
        '''    
    for itemEle in lastSimilarEleList:
        itemEle.setAttribute("transfer",thisResultId)
        '''
        if not restartTag:
            itemEle.setAttribute("transfer",thisResultId)
            
            #updateLastSimilar(lastSimilarEleList)
        else:
            itemEle.setAttribute("transfer","restart")
        '''
    ######################record this time even
    selectedEvent=selectEvent(resultEventRecord,actionIndex)
    
    ######################
    if not selectedEvent.hasAttribute("transfer"):
        selectedEvent.setAttribute("transfer","currentUnknown")

    
    return selectedEvent, selectedSimEleList, thisResultId, transferChanged, resultEventRecord
    #print(similarHisStr)
    
'''
def findNeighborCount(recordRoot,root_Result,sameEvent, similarEventList, featureStepNum, neighborLen):
    #padding=100
    #edgePadding=50
    #vectorLen=100
    
    outPutLen=3
    outPutDict={}#key is the index, value is a list [[level1],[level2],[level3]]
    
    eleDict={}#key is resultId, value is ele
    recordEleList=recordRoot.childNodes
    
    for recordEle in recordEleList:
        idStr=recordEle.getAttribute("id")
        
        eleDict[idStr]=recordEle
    
    
    
    if sameEvent:
        ##############find the nearest 0
        
        similarStr=sameEvent.getAttribute("similarEx")
        #similarNumList=similarStr.split(";")
        
        BFSList=[]
        #vistiedSet=set()
        
        #vistiedSet.add(sameEvent)
        
        resultEleList=sameEvent.getElementsByTagName("Easyoperate")[0].childNodes


        ##################
        for index in range(len(resultEleList)):            
            #BFSList.append((resultEleList[index],resultEleList[index]))####first item is should step, second item is BFS current step
            if resultEleList[index].hasAttribute("transfer"):#if there is no transfer, we omit
                nextID=resultEleList[index].getAttribute("transfer")
                
                if not nextID=="restart":
                    if not nextID=="currentUnknown":
                        
                        nextEle=eleDict[nextID]
                        BFSList.append((1,index,nextEle, set([sameEvent])))###0 is the level of the tree
                        
        
        
        while len(BFSList)>0:
            (level,orignialIndex,currentEle, vistiedSet)=BFSList[0]
            
            if level>outPutLen:
                break
            
            
            
            BFSList=BFSList[1:]##############remove the first element
            
            curChildList=currentEle.getElementsByTagName("Easyoperate")[0].childNodes
            
            similarStr=currentEle.getAttribute("similarEx")
            
            similarList=similarStr.split(";")
            addList=[]
            for item in similarList:
                addList.append(int(item))
                
            if not orignialIndex in outPutDict:
                outPutDict[orignialIndex]=[]#[0]*neighborLen)
            
            if len(outPutDict[orignialIndex])<level:
                outPutDict[orignialIndex].append([0]*neighborLen)
            
            
            for item in similarList:
                itemInt=int(item)
                if itemInt>=neighborLen:
                    itemInt=neighborLen-1

                outPutDict[orignialIndex][level-1][itemInt]+=1

                
            #outPutDict[orignialIndex][level-1]+=addList
            
            for index in range(len(curChildList)):
                
                if curChildList[index].hasAttribute("transfer"):
                    nextID=curChildList[index].getAttribute("transfer")
                    
                    if not nextID=="restart":
                        if not nextID=="currentUnknown":
                    
                            nextEle=eleDict[nextID]
                            if not nextEle in vistiedSet:####it just give up to explore more
                                vistiedSet.add(nextEle)
                                BFSList.append((level+1, orignialIndex,nextEle, vistiedSet))### the len of BFS may be bigger then all pages, because of the first page
            

            
    #outPutList=[]#3 item represents 3 level, in every item there is a list to represent different event
    
    
    Nei1List=[]
    Nei2List=[]
    Nei3List=[]
    for index in range(featureStepNum):
        if index in outPutDict:
            lenIndex=len(outPutDict[index])
            if lenIndex>=1:
                Nei1List.append(outPutDict[index][0])
            else:
                Nei1List.append([0]*neighborLen)
                
            if lenIndex>=2:
                Nei2List.append(outPutDict[index][1])
            else:
                Nei2List.append([0]*neighborLen)
                
            if lenIndex>=3:
                Nei3List.append(outPutDict[index][2])
            else:
                Nei3List.append([0]*neighborLen)
            
        else:
            Nei1List.append([0]*neighborLen)
            Nei2List.append([0]*neighborLen)
            Nei3List.append([0]*neighborLen)
            
                        
    return [Nei1List,Nei2List,Nei3List]#similar branch may have multiple count, need to fix
    
    '''
def findNeighborCount(recordRoot,sameEvent, featureStepNum, neighborLen):
    #padding=100
    #edgePadding=50
    #vectorLen=100
    
    outPutLen=3
    outPutDict={}#key is the index, value is a list [[level1],[level2],[level3]]
    
    eleDict={}#key is resultId, value is ele
    recordEleList=recordRoot.childNodes
    
    for recordEle in recordEleList:
        idStr=recordEle.getAttribute("id")
        
        eleDict[idStr]=recordEle
    
    
    
    if sameEvent:
        ##############find the nearest 0
        
        similarStr=sameEvent.getAttribute("similarEx")
        #similarNumList=similarStr.split(";")
        
        BFSList=[]
        #vistiedSet=set()
        
        #vistiedSet.add(sameEvent)
        
        resultEleList=sameEvent.getElementsByTagName("Easyoperate")[0].childNodes
        sameID=sameEvent.getAttribute("id")


        ##################build visited set
        vistiedSet=set()
        
        
        #######
        ''''test for take the repeated current as neighbour
        for index in range(len(resultEleList)):
            
            if resultEleList[index].hasAttribute("simID"):
                for itemStr in resultEleList[index].getAttribute("simID").split(";"):
                    vistiedSet.add(itemStr)
            vistiedSet.add(sameID+"-"+str(index))
        '''
        
        ###build initial BFS list
        for index in range(len(resultEleList)):            
            if resultEleList[index].hasAttribute("transfer"):#if there is no transfer, we omit
                nextID=resultEleList[index].getAttribute("transfer")
                
                if not nextID=="restart":
                    if not nextID=="currentUnknown":
                        
                        nextEle=eleDict[nextID]
                        BFSList.append((1,index,nextEle, vistiedSet.copy()))###0 is the level of the tree
                
        
        
        while len(BFSList)>0:
            (level,orignialIndex,currentEle, vistiedSet)=BFSList[0]
            
            if level>outPutLen:
                break
            
            
            
            BFSList=BFSList[1:]##############remove the first element
            
            curChildList=currentEle.getElementsByTagName("Easyoperate")[0].childNodes
            curEleID=currentEle.getAttribute("id")
            
            similarStr=currentEle.getAttribute("similarEx")
            
            similarList=similarStr.split(";")
            
            if not orignialIndex in outPutDict:
                outPutDict[orignialIndex]=[]#[0]*neighborLen)
            
            if len(outPutDict[orignialIndex])<level:
                outPutDict[orignialIndex].append([0]*neighborLen)
            
            
            for index in range(len(curChildList)):
                
                if curChildList[index].getAttribute("tag").startswith("default"):
                    continue
                
                similarVal=int(similarList[index])
                
                curIndexID=curEleID+"-"+str(index)
                if not curIndexID in vistiedSet:
                    vistiedSet.add(curIndexID)
                    
                    if curChildList[index].hasAttribute("simID"):
                        for itemStr in curChildList[index].getAttribute("simID").split(";"):
                            vistiedSet.add(itemStr)
                            
                else:
                    continue#it is already visited
                
                if  similarVal>=neighborLen:
                    similarVal=neighborLen-1
                
                outPutDict[orignialIndex][level-1][similarVal]-=1
                
                
                
                if curChildList[index].hasAttribute("transfer"):
                    nextID=curChildList[index].getAttribute("transfer")
                    
                    if not nextID=="restart":
                        if not nextID=="currentUnknown":
                    
                            nextEle=eleDict[nextID]
                            BFSList.append((level+1, orignialIndex,nextEle, vistiedSet))### the len of BFS may be bigger then all pages, because of the first page
            
    
    
    Nei1List=[]
    Nei2List=[]
    Nei3List=[]
    for index in range(featureStepNum):
        if index in outPutDict:
            lenIndex=len(outPutDict[index])
            if lenIndex>=1:
                Nei1List.append(outPutDict[index][0])
            else:
                Nei1List.append([0]*neighborLen)
                
            if lenIndex>=2:
                Nei2List.append(outPutDict[index][1])
            else:
                Nei2List.append([0]*neighborLen)
                
            if lenIndex>=3:
                Nei3List.append(outPutDict[index][2])
            else:
                Nei3List.append([0]*neighborLen)
            
        else:
            Nei1List.append([0]*neighborLen)
            Nei2List.append([0]*neighborLen)
            Nei3List.append([0]*neighborLen)
    
    '''
    #############change feature test
    Nei1List=[]
    Nei2List=[]
    Nei3List=[]
    for index in range(featureStepNum):
        if index in outPutDict:
            lenIndex=len(outPutDict[index])
            if lenIndex>=1:
                #Nei1List.append(outPutDict[index][0])
                
                if outPutDict[index][0][0]<0:
                    Nei1List.append([-1]*neighborLen)
                else:
                    Nei1List.append([0]*neighborLen)
            else:
                Nei1List.append([0]*neighborLen)
                
            if lenIndex>=2:
                #Nei2List.append(outPutDict[index][1])
                if outPutDict[index][1][0]<0:
                    Nei2List.append([-1]*neighborLen)
                else:
                    Nei2List.append([0]*neighborLen)
                
            else:
                Nei2List.append([0]*neighborLen)
                
            if lenIndex>=3:
                #Nei3List.append(outPutDict[index][2])
                if outPutDict[index][2][0]<0:
                    Nei3List.append([-1]*neighborLen)
                else:
                    Nei3List.append([0]*neighborLen)
            else:
                Nei3List.append([0]*neighborLen)
            
        else:
            Nei1List.append([0]*neighborLen)
            Nei2List.append([0]*neighborLen)
            Nei3List.append([0]*neighborLen)
    '''
               
    return [Nei1List,Nei2List,Nei3List]#similar branch may have multiple count, need to fix
    
    
    
    
    
def findNeighbor(recordRoot,root_Result,sameEvent, similarEventList, featureStepNum):
    
    padding=100
    edgePadding=50
    vectorLen=100
    
    outPutLen=3
    outPutDict={}#key is the index, value is a list [[level1],[level2],[level3]]
    
    eleDict={}#key is resultId, value is ele
    recordEleList=recordRoot.childNodes
    
    for recordEle in recordEleList:
        idStr=recordEle.getAttribute("id")
        
        eleDict[idStr]=recordEle
    
    
    
    if sameEvent:
        ##############find the nearest 0
        
        similarStr=sameEvent.getAttribute("similarEx")
        #similarNumList=similarStr.split(";")
        
        BFSList=[]
        vistiedSet=set()
        
        vistiedSet.add(sameEvent)
        
        resultEleList=sameEvent.getElementsByTagName("Easyoperate")[0].childNodes


        ##################
        for index in range(len(resultEleList)):            
            #BFSList.append((resultEleList[index],resultEleList[index]))####first item is should step, second item is BFS current step
            if resultEleList[index].hasAttribute("transfer"):#if there is no transfer, we omit
                nextID=resultEleList[index].getAttribute("transfer")
                
                if not nextID=="restart":
                    if not nextID=="currentUnknown":
                        
                        nextEle=eleDict[nextID]
                        BFSList.append((1,index,nextEle))###0 is the level of the tree
                        
        
        
        while len(BFSList)>0:
            (level,orignialIndex,currentEle)=BFSList[0]
            
            if level>outPutLen:
                break
            
            
            BFSList=BFSList[1:]##############remove the first element
            
            curChildList=currentEle.getElementsByTagName("Easyoperate")[0].childNodes
            
            similarStr=currentEle.getAttribute("similarEx")
            
            similarList=similarStr.split(";")
            addList=[]
            for item in similarList:
                addList.append(int(item))
                
            if not orignialIndex in outPutDict:
                outPutDict[orignialIndex]=[]
            
            if len(outPutDict[orignialIndex])<level:
                outPutDict[orignialIndex].append([])
            
            ####add edge padding as 50
            if not len(outPutDict[orignialIndex][level-1])==0:
                outPutDict[orignialIndex][level-1]+=[edgePadding]

            
            outPutDict[orignialIndex][level-1]+=addList
            
            for index in range(len(curChildList)):
                
                if curChildList[index].hasAttribute("transfer"):
                    nextID=curChildList[index].getAttribute("transfer")
                    
                    if not nextID=="restart":
                        if not nextID=="currentUnknown":
                    
                            nextEle=eleDict[nextID]
                            if not nextEle in vistiedSet:####it just give up to explore more
                                vistiedSet.add(nextEle)
                                BFSList.append((level+1, orignialIndex,nextEle))### the len of BFS may be bigger then all pages, because of the first page
            
    
    for key in outPutDict:
        neiList=outPutDict[key]
        newNeiList=[]
        
        
        for index in range(len(neiList)):
            nei=neiList[index]
            if len(nei)>vectorLen:
                newNeiList.append(np.array(nei[:vectorLen]))
            else:
                newNeiList.append(np.pad(nei, (0,vectorLen-len(nei)), 'constant', constant_values= padding))
                
        outPutDict[key]=newNeiList
            
            
    outPutList=[]#3 item represents 3 level, in every item there is a list to represent different event
    
    
    Nei1List=[]
    Nei2List=[]
    Nei3List=[]
    for index in range(featureStepNum):
        if index in outPutDict:
            lenIndex=len(outPutDict[index])
            if lenIndex>=1:
                Nei1List.append(outPutDict[index][0])
            else:
                Nei1List.append([padding]*vectorLen)
                
            if lenIndex>=2:
                Nei2List.append(outPutDict[index][1])
            else:
                Nei2List.append([padding]*vectorLen)
                
            if lenIndex>=3:
                Nei3List.append(outPutDict[index][2])
            else:
                Nei3List.append([padding]*vectorLen)
            
        else:
            Nei1List.append([padding]*vectorLen)
            Nei2List.append([padding]*vectorLen)
            Nei3List.append([padding]*vectorLen)
            
                        
    return [Nei1List,Nei2List,Nei3List]
    
    
    
    
    
    
    
    
    
    
    
def findComplement(recordRoot,root_Result,sameEvent, similarEventList):
    
    #####there is no need to desigin a algorithm from restart, because every event has a trace to go restart
    
    
    eleDict={}#key is resultId, value is ele
    recordEleList=recordRoot.childNodes
    for recordEle in recordEleList:
        idStr=recordEle.getAttribute("id")
        
        eleDict[idStr]=recordEle
    
    
    
    if sameEvent:
        ##############find the nearest 0
        
        similarStr=sameEvent.getAttribute("similarEx")
        similarNumList=similarStr.split(";")
        
        for index in range(len(similarNumList)):
            if similarNumList[index]=="0":
                if index==None:
                    print("aa")
                
                print(similarStr)
                return index
            
        BFSList=[]
        vistiedSet=set()
        
        
        resultEleList=sameEvent.getElementsByTagName("Easyoperate")[0].childNodes
        for index in range(len(resultEleList)):
            
            #BFSList.append((resultEleList[index],resultEleList[index]))####first item is should step, second item is BFS current step
            if resultEleList[index].hasAttribute("transfer"):
                nextID=resultEleList[index].getAttribute("transfer")
                
                if not nextID=="restart":
                    if nextID=="currentUnknown":
                        return index
                    else:
                        nextEle=eleDict[nextID]
                        #BFSList.append((resultEleList[index],nextEle))####first item is should step, second item is BFS current step
                        BFSList.append((index,nextEle))
                        
                    
                    
                
                '''
                if not nextID=="restart" or not :
                    nextEle=eleDict[nextID]
                    #BFSList.append((resultEleList[index],nextEle))####first item is should step, second item is BFS current step
                    BFSList.append((index,nextEle))
                '''
            else:
                print("error it should not happen")
            
            
        ##BFS begin
        while len(BFSList)>0:
            (firstIndex,currentEle)=BFSList[0]
            BFSList=BFSList[1:]##############remove the first element
            
            curChildList=currentEle.getElementsByTagName("Easyoperate")[0].childNodes
            
            similarStr=currentEle.getAttribute("similarEx")
            if "0" in similarStr.split(";"):
                print(similarStr)
                return firstIndex
            
            for index in range(len(curChildList)):
                
                if curChildList[index].hasAttribute("transfer"):
                    nextID=curChildList[index].getAttribute("transfer")
                    
                    #if not nextID=="restart":####restart also has a transfer
                        
                    if nextID=="currentUnknown":
                        return firstIndex
                    
                    nextEle=eleDict[nextID]
                    if not nextEle in vistiedSet:
                        vistiedSet.add(nextEle)
                        BFSList.append((firstIndex,nextEle))### the len of BFS may be bigger then all pages, because of the first page
                    
                    
                else:
                    print("it should not happen")  #### it needs to robust
                    
                        
        
    else:
        ###############3choose random one to click
        index=random.choice(range(len(root_Result.getElementsByTagName("Easyoperate")[0].childNodes)))
        #index=random.choice(range(len(recordEleList)))
        return index
        print("there is no sameEvent")
    
    print("all is explored")
    return "all is explored"
    
def selectEvent(allEvent,actionIndex):
    
    runableEleList=allEvent.getElementsByTagName('runableID')
    
    for runableEle in runableEleList:
        if runableEle.getAttribute("id")==str(actionIndex):
            return runableEle
        
    return None
    

def updateSimilarID(similarEventList,resultId, resultEventRecord):
    
    curRootList=resultEventRecord.getElementsByTagName("Easyoperate")[0].childNodes
    
    
    for oneSimEvent, newIdtobeIdDict in similarEventList:
        simEleList=oneSimEvent.getElementsByTagName("Easyoperate")[0].childNodes

        for newIndex in newIdtobeIdDict:
            oldIndex=newIdtobeIdDict[newIndex]
            if  simEleList[oldIndex].hasAttribute("simID"):
                simIDStr=simEleList[oldIndex].getAttribute("simID")
                simIDStr+=";"+str(resultId)+"-"+str(newIndex)
                simEleList[oldIndex].setAttribute("simID",simIDStr)
            else:
                simEleList[oldIndex].setAttribute("simID",str(resultId)+"-"+str(newIndex))
                
            #####################
            oldEventId=oneSimEvent.getAttribute("id")
            oldEventIndex=oldIndex
            
            if curRootList[newIndex].hasAttribute("simID"):
                simIDStr=curRootList[newIndex].getAttribute("simID")
                simIDStr+=";"+str(oldEventId)+"-"+str(oldEventIndex)
                curRootList[newIndex].setAttribute("simID",simIDStr)
            else:
                curRootList[newIndex].setAttribute("simID",str(oldEventId)+"-"+str(oldEventIndex))

            


    
def updateAllSimilar(similarEventList, actionIndex, resultEventRecord):
    
    curRootList=resultEventRecord.getElementsByTagName("Easyoperate")[0].childNodes
    
    lastSimilarEleList=[]
    
    for oneSimEvent, newIdtobeIdDict in similarEventList:
        newStr=""
        oneSimliar=oneSimEvent.getAttribute("similarEx")
        itemList=oneSimliar.split(";")
        
        simEleList=oneSimEvent.getElementsByTagName("Easyoperate")[0].childNodes

        ##############update current transfer
        for index in range(len(curRootList)):
            if index in newIdtobeIdDict:
                oldIndex=newIdtobeIdDict[index]
                if simEleList[oldIndex].hasAttribute("transfer"):
                    transStr=simEleList[oldIndex].getAttribute("transfer")
                    curRootList[index].setAttribute("transfer",transStr)

        #############update before
        for i in range(0,len(itemList)):
            
            if actionIndex in newIdtobeIdDict and i==newIdtobeIdDict[actionIndex]:#sometimes current event is longer than before
                newStr+=str(int(itemList[i])+1)+";"
                ####
                lastSimilarEleList.append(simEleList[i])
            else:
                newStr+=str(int(itemList[i]))+";"
                    
        newStr=newStr[:-1]
        oneSimEvent.setAttribute("similarEx",newStr)
        #print("getAttribute:   "+oneSimEvent.getAttribute("similarEx"))
    return lastSimilarEleList
    
def oldupdateAllSimilar_copy(similarEventList, similarHisStr):
    for oneSimEvent in similarEventList:
        oneSimEvent.setAttribute("similarEx",similarHisStr)
        #print("getAttribute:   "+oneSimEvent.getAttribute("similarEx"))
        
        
                
def computeRewardSimilar(feature):
    ############################similarity reward
    if not feature.similarExist and not feature.sameExist:
        return 10
    else:
        return -5
        
        
        
        
        