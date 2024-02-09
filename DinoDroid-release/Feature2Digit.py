import numpy as np
import re


def textFeature2Digit(feature,word2Idx):
    
    numList=[]
    eventNum=len(feature.runableList)
    
    for index in range(eventNum):
        textInOne=feature.runableList[index].text
        
        wordList=re.findall(r"[\w']+|[.,!?;]", textInOne.lower())
        
        oneRunArray=np.array([])
        
        maxVal=6 #how many word in a sentence
        count=0
        for word in wordList:
            if count<maxVal:
                count+=1
            else:
                break
            
            
            if word.lower() in word2Idx:
                oneRunArray=np.append(oneRunArray,word2Idx[word])
            elif word.lower()=="dividebysen":
                oneRunArray=np.append(oneRunArray,word2Idx["dividebysen"])
            else:
                oneRunArray=np.append(oneRunArray,word2Idx["UNKNOWN_TOKEN"])
                
        
        if len(oneRunArray)<maxVal:
            for i in range(maxVal-len(oneRunArray)):
                oneRunArray=np.append(oneRunArray,word2Idx["PADDING_TOKEN"])
                
        numList.append(oneRunArray)
        
    return np.array(numList)
        
        #oneRunList[0]
def sameFeatureExtract(feature):
    sameResultList=feature.sameResultList
    similarResultList=feature.similarResultList
    
    extendSize=10
    
    sameMatrix=[]
    similarMatrix=[]
    
    for sameItem in sameResultList:
        #sameMatrix.append(np.full(extendSize, sameItem))
        sameMatrix.append(np.full(extendSize, sameItem))
        
    for similarItem in similarResultList:
        #similarMatrix.append(np.full(extendSize, similarItem))
        similarMatrix.append(np.full(extendSize, similarItem))
        
    return np.array(sameMatrix), np.array(similarMatrix)
        
    
    
    
    