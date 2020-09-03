'''
Created on Jun 12, 2017

@author: yu
'''
#from uiautomator import device as d
from uiautomator import Device
import time
import sys
import pickle

from xml.dom.minidom import Document
from xml.dom import minidom
import commands
import os
import Trans
import codecs
import Similar
import Feature2Digit
import ENV
import numpy as np
import shutil

import time
import psutil
import gc

import objgraph

###############################

###############################
import DQNAgentDdqnNei as DQNAgent
#import DQNAgentNei as DQNAgent

import Feature

import threading
##################
from gensim.models import Word2Vec


def func(batch_size, featureListLen, Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList, agent, finishTag, sameBefore, iterCount, iteTime, recordNameCrash):
    print("lock acquire")
    lock.acquire()
    agent.replay(batch_size, featureListLen, Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList, sameBefore, iterCount, iteTime, recordNameCrash)
    finishTag[0]=1
    print("lock release")
    lock.release()

def main():
    
    keepBeforeRecord=False
    restartEmul=True
    reinstallApp=True
    test=False    ####for debug
    paral=False
    train=True   ####half and half
    #model.save("keras_mode.h5")
    
    
    #port='5554'
    #cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -d"
    #logText=commands.getstatusoutput(cmd)
    #################
    
    batch_size = 30
    init_step=5
    ############inital
    apkList=[]
    
    
    for folderName in os.listdir("/SPACE/reforce-project/dataset/train/unfinished"):
        
            sourceCodePath="/SPACE/reforce-project/dataset/train/unfinished/"+folderName+"/bin/"
            source="/SPACE/reforce-project/dataset/train/unfinished/"+folderName
            destination="/SPACE/reforce-project/dataset/train/finished/"+folderName
            
            apkFile,coverageEm,packageName,activityName=ENV.compileApkEmma(sourceCodePath, commands, os)
        
            apkList.append((apkFile,coverageEm,packageName,activityName,sourceCodePath, source, destination))  
    
    
    port='5554'
    #d = Device('emulator-'+port)
    #time.sleep(4)
    address='.'
    '''
    packageName="bander.notepad"
    activityName="bander.notepad.NoteList"
    apkName="notepad_debug.apk"
    '''
    ##############agent
    
    ###word embeding
    word2VecModel= Word2Vec.load('yumodel').wv
    
    wordVectorLen=400#this is yumodel's len size
    
    neighborLen=10 #this is neighbor list's length
    
    word2Idx, wordEmbeddings=DQNAgent.build_embed( word2VecModel,wordVectorLen)
    
        
    
   
    
    ###############start app
    #cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell am start -S -n "+packageName+"/"+activityName
    #commands.getstatusoutput(cmd)
    
    #avaiableAnotherList=["com.android.documentsui"]

    
    ##############
    apkCount=0
    
    #agent = DQNAgent.DQNAgentClass( wordEmbeddings, neighborLen)############need to modification

    matrixDict={}

    
    for apkItem in apkList:
        if not train:#test
            shutil.copyfile("./model/keras_model_half.h5", "./model/keras_model.h5")
        
        
        crashID=0
        eventNum=[0]
        
        
        importantButton=[]
        
        
        for iteTime in range(0,3):
            countReward=0
            #psutil.virtual_memory()
            '''
            outputFile = open("./testRecords/trainRecord"+str(iteTime)+".txt", 'a')
            outputFile.write("memory: "+str(psutil.virtual_memory())+"\n")
            outputFile.write("#####################"+"\n")
            outputFile.close()
            '''
            gc.collect()
            '''
            outputFile = open("./testRecords/trainRecord"+str(iteTime)+".txt", 'a')
            outputFile.write("memory: "+str(psutil.virtual_memory())+"\n")
            outputFile.write("#####################"+"\n")
            #outputFile.write(str(objgraph.show_growth())+"\n")
            

            outputFile.close()
            '''
                        
            agent = DQNAgent.DQNAgentClass( wordEmbeddings, neighborLen, matrixDict)############need to modification

            
        
            recordMiddleList=[]
            #simiarMap={}
            
        
        
        
            agent.memory={}###### brent's suggestion
            ############################3
            
            
            resultId=0
            lastResultId=-1000#### check the same page
            ############generate a record root in every apk
            recordDoc=Document()
            recordRoot=recordDoc.createElement("recdrodRoot")
            
            
            ###test
            if keepBeforeRecord:
                doc=minidom.parse(address+'/middleResults/record.xml')
                recordRoot=doc.documentElement
            ###test end
            
            doc_write =Document()
            doc_write.appendChild(recordRoot)  
            with codecs.open(address+"/middleResults/record.xml","wb","utf-8") as out:
                doc_write.writexml(out)
            out.close()
            
            if restartEmul:
                ENV.restartAndroidEumlator(port,commands) #        for the text close
                
            outputFile = open("./testRecords/trainRecord"+str(iteTime)+".txt", 'a')
            outputFile.write("memory: "+str(psutil.virtual_memory())+"\n")
            outputFile.write("#####################"+"\n")
            outputFile.close()
            
            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb shell dumpsys window displays | grep 'init'"
            tupleLine=commands.getstatusoutput(cmd)
            while(True):
            
                try:
                
                    heightAndWeight=tupleLine[1].strip().split(" ")[0].split("=")[1]
                    height=int(heightAndWeight.split("x")[1])
                    weight=int(heightAndWeight.split("x")[0])
                    
                    
                    break
                except:
                    
                    print("waitForEmu")
                    continue
            
            
            ####################install apk
            
            
            
            apkName=apkItem[0]
            coverageEm=apkItem[1]
            packageName=apkItem[2]
            activityName=apkItem[3]
            sourceCodePath=apkItem[4]
            source=apkItem[5]
            destination=apkItem[6]
            
            recordNameCrash=source.rsplit("/",1)[1]

        
            d = Device('emulator-'+port)
            if reinstallApp:
                cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" uninstall "+packageName
                commands.getstatusoutput(cmd) 
            
                cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" install "+apkName
                commands.getstatusoutput(cmd) 
            
        
            specChar=False
            
            actionIndex=None
            feature=None
            lastFeature=None
            lastActionIndex=None
            appCloseTag=False
            lastFeatureTuple=None
            crashTag=False
            logHistory=""
            
            
            ######################################coverage data
            lineCoverage=0
            methodCoverage=0
            classCoverage=0
            
            coverageData=[lineCoverage,methodCoverage,classCoverage]#class is not the activity coverage
            
            
            ####################clean sdcard
            ENV.cleanSd(commands, port)
            
            
            start = time.time()
            
            apkCount+=1
            
            lastEventInRecord=None
            lastSimilarEleList=[]
            restartTag=False
            
            finishTag=[1]
            
            crashedIntentStr="init"
            
            coverageRecord=[]
            
            for iterCount in range(10000):
                              
                
                coverageRecord.append(coverageData[0])
                
                
                
                print(matrixDict)
                #menuTag=False
                #adb -s emulator-5556 shell rm -r sdcard/*
                print("apkCount:"+str(apkCount))
                
                
                ####################3every apk only train 2 hours
                end=time.time()
                if end-start>1200:#1200:
                    break
                
                
                print("iterCount:"+str(iterCount))
                print("currentReward"+str(countReward))
                
                if not iterCount==0:#it is the first time
                    ##################clean
                    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -c"
                    commands.getstatusoutput(cmd)
                    #ENV.step(actionIndex, d, feature, commands, address, port, apkName, packageName, activityName,specChar, eventNum)
                    
                    try:
                        #run
                        ENV.step(actionIndex, d, feature, commands, address, port, apkName, packageName, activityName,specChar, eventNum)
                    except:
                        d.press.back()
                        eventNum[0]=eventNum[0]+1
                        print("except to click back")
                    
                    '''
                    if len(crashedIntentStr)>3:
                        print("bingo")
                    '''
                    #send a random intent
                    intentIter=False
                    selectedStr=""
                    if iterCount % 10==0:
                        selectedStr=""
                        #cmd="python /SPACE/stoat/Stoat-master/Stoat/trigger/tester.py -s emulator-5554 -f "+apkName+" -p random " + "-c "+crashedIntentStr
                        cmd="python /home/yu/workspace2/rf-android/trigger/tester.py -s emulator-5554 -f "+apkName+" -p random " + "-c "+crashedIntentStr
                        intent=commands.getstatusoutput(cmd)
                        
                        intentStr=intent[1]
                        if "tagAAA" in intentStr:
                            a=intentStr.index("tagAAA")
                            b=intentStr.index("endAAA")
                            
                            selectedStr=intentStr[a+7:b]
                            
                        print(intentStr)
                        
                        outputFile = open("./trainResult/"+recordNameCrash+"_intent_"+".txt", 'a')
                        
                        outputFile.write("intentStr: "+intentStr+"\n")
                        outputFile.write("crashedIntentStr: "+str(crashedIntentStr)+"\n")
                        outputFile.close()
                        
                        
                        
                        intentIter=True
                        
                        
                    
                    #################check crash
                    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -d"
                    logText=commands.getstatusoutput(cmd)
                    logText=logText[1]
                    
                    if "FATAL" in logText or "fatal" in logText:
                        if intentIter and selectedStr:
                           crashedIntentStr+=selectedStr+"***"
                        
                    
                    
                        #logText=
                        crashID+=1
                        ENV.writeCrash(logText, recordNameCrash ,crashID, eventNum)
                    
                        logBoolean,newLogAdd, specOut=ENV.checkBefore(logText,logHistory)
                        if specOut==True and specChar==False:
                            specChar=True
                        if not logBoolean:
                        
                            crashTag=True
                            #ENV.writeCrash(logText,iterCount)
                            logHistory+=newLogAdd
                            eventNum[0]=eventNum[0]+1
                            className=ENV.restartApp(port,commands, packageName, activityName)
                            print("catch a crash and restart app")
                            
                        else:
                            crashTag=False
                            className=ENV.restartApp(port,commands, packageName, activityName)
                            eventNum[0]=eventNum[0]+1
                            print("catch a crash and restart app")
                    else:
                        crashTag=False
                    
                
                
                
                cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window windows | grep -E 'mFocusedApp'"
                tupleLine=commands.getstatusoutput(cmd)
                className=str(tupleLine).split(" ")[-2]
                
                if not packageName in tupleLine[1] and not "com.android" in tupleLine[1] or "com.android.launcher" in tupleLine[1]:

                    appCloseTag=True
                    className=ENV.restartApp(port,commands, packageName, activityName)
                    restartTag=True
                    eventNum[0]=eventNum[0]+1

                    
                else:
                    appCloseTag=False
                    
                
                root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
                            
                
                if notEmpty==False:
                    if loading==1:
                        for iterTimes in range(0,20):
                            if notEmpty==False:####may be dump at a middle page
                                time.sleep(0.4)
                                root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
                                print("dumped a empty and loading page, so repeat dump"+str(iterTimes))
                            else:
                                break
                    else:                            
                        #permitOtherApp="anypackageisok"
                        #otherRoot_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, permitOtherApp, className, commands, port)
                        
                        
                        ENV.expOtherApp(d,height,weight)####just random find one to click
                        eventNum[0]=eventNum[0]+10

                        for iterTimes in range(0,5):
                            
                            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window windows | grep -E 'mFocusedApp'"
                            tupleLine=commands.getstatusoutput(cmd)
                            
                            if not packageName in tupleLine[1]:
                                print(iterTimes)
                                d.press.back()
                                d.wait.update()
                                time.sleep(0.5)
                            else:
                                className=str(tupleLine).split(" ")[-2]
                                break
                            
                            if iterTimes==4:
                                print("restart")
                                className=ENV.restartApp(port,commands, packageName, activityName)
                                eventNum[0]=eventNum[0]+1

                                restartTag=True
                                break
                        root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
    
                ##########################remove
                os.remove(address+'/middleResults/result.xml')
                
                
                #Similar.findComplement(recordRoot,root_Result,sameEvent, similarEventList)
                
                
                #######################compare similarity
                sameEvent, similarEventList, sameResultListMiddle,similarResultListMiddle=Similar.getSimilar(recordRoot,root_Result)
                
                ######################extract feature
                feature=Feature.FeatureClass(root_Result,sameResultListMiddle, similarResultListMiddle, sameEvent, similarEventList)
                
                
                
                featureStepNum=len(feature.runableList)
                
                
                textFeatue=Feature2Digit.textFeature2Digit(feature,word2Idx)####just encode to the word ID
                sameFeature,similarFeature=Feature2Digit.sameFeatureExtract(feature)
                
                
                
                #neighborFeatureList=Similar.findNeighbor(recordRoot,root_Result,sameEvent, similarEventList, featureStepNum)
                neighborFeatureList=Similar.findNeighborCount(recordRoot,sameEvent, featureStepNum, neighborLen)
                ###########################
                
                
                
                
                featureTuple=(textFeatue,sameFeature,similarFeature, neighborFeatureList)#########generate feature for machine learning input
                
                ######################run model
                #actionIndex, timeCost=agent.actMatrix(featureTuple, iterCount, test)
                actionIndex, timeCost=agent.act(featureTuple, iterCount, test)
                #dest = shutil.move(source, destination)#  for the test
                #actionIndex=np.argmax(action)
                #actionIndex=3
                print("actionIndex: "+str(actionIndex))
                ##########################recordRoot
                if sameEvent and sameEvent.getAttribute("id")==lastResultId: 
                    sameBefore=True
                else:
                    sameBefore=False
                
                #Similar.addToRecordRoot(recordRoot, root_Result,resultId,feature,featureStepNum,actionIndex,sameEvent, similarEventList)
                                
                ####
                
                lastEventInRecord, lastSimilarEleList, lastResultId, transferChanged, resultEventRecord=Similar.addToRecordRoot(recordRoot, root_Result,resultId,feature,featureStepNum,actionIndex,sameEvent, similarEventList, lastEventInRecord, restartTag, lastSimilarEleList)
                ############################record into file
                doc_write =Document()
                doc_write.appendChild(recordRoot)  
                with codecs.open(address+"/middleResults/record.xml","wb","utf-8") as out:
                    doc_write.writexml(out)
                out.close()
                ############################################
                
                
                
                
                
                
                ########################add page ID
                resultId+=1
                
                ##################run
                #className=ENV.step(actionIndex, d, feature, commands, address, port)
                
                
                
                ##################memorize and update model, this part can be implemented parallel with run
                if iterCount==0:#it is the first time
                    lastFeature=feature
                    lastActionIndex=actionIndex 
                    
                else:
                    ####################updateLast FeatureTuple
                    
                    #lastNeighborFeatureList=Similar.findNeighborCount(recordRoot,lastResultEventRecord, lastFeatureStepNum, neighborLen)
                    #lastFeatureTuple=(lastFeatureTuple[0],lastFeatureTuple[1],lastFeatureTuple[2],lastNeighborFeatureList)
                    
                    
                    
                    
                    #######333test reward
                    '''
                    lastSimArray=np.array(lastFeatureTuple[2])[:,0]
                    
                    if lastSimArray[lastActionIndex]==0:
                        reward=5
                    else:
                        reward=-2
                    '''
                    ##################################
                    
                    #reward=Similar.computeRewardSimilar(feature)not good
                    
                    #test reward
                    #reward=
                    #ENV.computeRewardCoverage(commands, port, sourceCodePath, coverageData)
                    reward=ENV.computeRewardCoverage(commands, port, sourceCodePath, coverageData)
                    '''
                    if reward==5:
                        importStr=Similar.checkImportant(lastFeatureTuple, lastActionIndex, lastFeature)
                    '''
                        
                    
                    '''
                    if crashTag:#######good catch
                        #reward=10
                        reward=5
                    '''
                    
                    countReward+=reward
                    
                    if not transferChanged:
                        agent.memorize(lastFeatureTuple, lastActionIndex, reward, featureTuple)
                        
                        
                        testLastTuple=(lastFeatureTuple, lastActionIndex, reward, featureTuple)
                        #################train DQN

                    
                    
                    
                        if iterCount > 0:
                            
                            if paral:
                            
                                while True:
                                    if finishTag[0]==1:
                                        finishTag=[0]
                                        break
                                t = threading.Thread(target=func, args=(batch_size, len(lastFeature.runableList),Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList, agent, finishTag, sameBefore, iterCount, iteTime, recordNameCrash)) 
                                t.start()
                            else:
                                
                                func(batch_size, len(lastFeature.runableList),Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList, agent, finishTag, sameBefore,iterCount, iteTime, recordNameCrash)
                    else:
                        print("transferChanged")
                        
                        #t.isAlive()
                        
                        #agent.replay(batch_size, len(lastFeature.runableList),Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList)
                        
                    
                lastFeature=feature
                lastFeatureTuple=featureTuple
                lastActionIndex=actionIndex
                #lastResultEventRecord=resultEventRecord
                #lastFeatureStepNum=featureStepNum


                
            ###
            while True:
                if finishTag[0]==1:
                    finishTag=[0]
                    break
            
            #np.save("./model/memory.npy",agent.memory)
            pickle.dump( agent.memory, open( "./model/memory.p", "wb" ) )
            # favorite_color = pickle.load( open( "save.p", "rb" ) )
            
            agent.save("./model/keras_model.h5")
            
            recordName=source.rsplit("/",1)[1]
            shutil.move("./emmaOutput.txt", "./trainResult/"+recordName+"_coverage_"+str(iteTime)+".txt")
            shutil.move("./middleResults/record.xml", "./trainResult/"+recordName+"_record_"+str(iteTime)+".xml")
            
            shutil.move("./coverage.ec", "./trainResult/"+recordName+"_emma_"+str(iteTime)+".ec")

            
            outputFile = open("./experimentRecord.txt", 'a')
            outputFile.write("\n")
            outputFile.write("coverage:"+str(coverageData[0])+"\n")
            outputFile.write("testCoverage:"+str(countReward)+"\n")
            outputFile.write("iterate:"+str(iteTime)+"\n")
            outputFile.close()
            #for covData in coverageRecord:
            
            outputFile = open("/SPACE/reforce-project/dataset/train/result/"+recordName+"_coverage_"+str(iteTime)+".txt", 'a')
            
            for covData in coverageRecord:
                outputFile.write(str(covData)+"\n")
            outputFile.close()  
            
            
            outputFile = open("./trainResult/"+recordName+"_eventNum_"+str(iteTime)+".txt", 'a')
            outputFile.write(str(str(eventNum[0]))+"\n")
            outputFile.close()
            
            ##test
            '''
            outputFile = open("/SPACE/reforce-project/dataset/train/result/"+recordName+"_middle_"+str(iteTime)+".txt", 'a')
            
            
            
            for line in recordMiddleList:
                outputFile.write(str(line)+"\n")
            outputFile.close()
            '''
            agent.save("/SPACE/reforce-project/dataset/train/result/"+recordName+"_model_"+str(iteTime)+".h5")            
            agent.clean()
            
            
            #del agent
            #gc.collect()
            
        dest = shutil.move(source, destination)#  for the test
    
if __name__ == '__main__':
    lock=threading.Lock()
    main()         