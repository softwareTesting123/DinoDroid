'''
Created on Jun 12, 2017

@author: yu
'''
#from uiautomator import device as d
from uiautomator import Device
import time
import sys

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
import Complement

import time
###############################

###############################
#import DQNAgent
import Feature

import DQNAgentDDQN as DQNAgent


##################
from gensim.models import Word2Vec
from docutils.writers import null


def main():
    
    
    #model.save("keras_mode.h5") I may need to make a thing to let train and action to parallel
    
    
    #port='5554'
    #cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -d"
    #logText=commands.getstatusoutput(cmd)
    
    countReward=0
    #################
    
    batch_size = 30
    init_step=5
    ############inital
    apkList=[]
    
    
    for folderName in os.listdir("/SPACE/test/"):
        
        for i in range(0,6):#for the test
            sourceCodePath="/SPACE/test/"+folderName+"/bin/"
            apkFile,coverageEm,packageName,activityName=ENV.compileApkEmma(sourceCodePath, commands, os)
        
            apkList.append((apkFile,coverageEm,packageName,activityName,sourceCodePath))
        break#for the test
    
    
    
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
    
    word2Idx, wordEmbeddings=DQNAgent.build_embed( word2VecModel,wordVectorLen)
    
        
    
   
    
    ###############start app
    #cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell am start -S -n "+packageName+"/"+activityName
    #commands.getstatusoutput(cmd)
    
    
    #avaiableAnotherList=["com.android.documentsui"]
    
    ##############
    apkCount=0
    
    for apkItem in apkList:
        agent = DQNAgent.DQNAgentClass( wordEmbeddings)############need to modification
        agent.memory={}
        ############################3
        
        
        resultId=0
        ############generate a record root in every apk
        recordDoc=Document()
        recordRoot=recordDoc.createElement("recdrodRoot")
        
        ###test
        #doc=minidom.parse(address+'/middleResults/record.xml')
        #recordRoot=doc.documentElement
        ###test end
        
        
        doc_write =Document()
        doc_write.appendChild(recordRoot)  
        with codecs.open(address+"/middleResults/record.xml","wb","utf-8") as out:
            doc_write.writexml(out)
        out.close()
        
        
        
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb shell dumpsys window displays | grep 'init'"
        tupleLine=commands.getstatusoutput(cmd)
        heightAndWeight=tupleLine[1].strip().split(" ")[0].split("=")[1]
        height=int(heightAndWeight.split("x")[1])
        weight=int(heightAndWeight.split("x")[0])
        
        
        
        ####################install apk
        
        
        
        apkName=apkItem[0]
        coverageEm=apkItem[1]
        packageName=apkItem[2]
        activityName=apkItem[3]
        sourceCodePath=apkItem[4]
    
    
        #ENV.restartAndroidEumlator(port,commands)         for the text close
        d = Device('emulator-'+port)
        
        '''
        ##take screen shot
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb shell screencap -p /sdcard/screencap.png"
        commands.getstatusoutput(cmd)
        '''
        
        
        #test
        
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" uninstall "+packageName
        commands.getstatusoutput(cmd) 
    
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" install "+apkName
        commands.getstatusoutput(cmd) 
        
        
        
        
        
        actionIndex=None
        feature=None
        lastFeature=None
        lastActionIndex=None
        appCloseTag=False
        lastFeatureTuple=None
        crashTag=False
        logHistory=""
        totalPredictTime=0
        
        ######################################coverage data
        lineCoverage=0
        methodCoverage=0
        classCoverage=0
        
        specChar=False
        
        coverageData=[lineCoverage,methodCoverage,classCoverage]#class is not the activity coverage
        
        totalTimeForTrain=0
        
        ####################clean sdcard
        ENV.cleanSd(commands, port)###change to only rm coverage.ec
        
        
        start = time.time()
        
        apkCount+=1
        
        lastEventInRecord=None
        lastSimilarEleList=[]
        #restartTag=True
        resultId=1
        Complement.run(recordRoot, apkCount, countReward, port, commands, d, address, apkName, packageName, specChar, activityName, logHistory, height, weight, resultId,sourceCodePath, coverageData)

        for iterCount in range(10000):
            
            resultId=1000
            
            print("Complement done")
            
            restartTag=False
            #menuTag=False
            #adb -s emulator-5556 shell rm -r sdcard/*
            print("apkCount:"+str(apkCount))
            
            
            ####################3every apk only train 2 hours
            end=time.time()
            if end-start>1800:
                break
            
            
            print("iterCount:"+str(iterCount))
            print("currentReward"+str(countReward))
            
            
            if not iterCount==0:#it is the first time
                
                ##################clean
                cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -c"
                commands.getstatusoutput(cmd)
                
                #run
                print("actionIndexForTest: "+str(actionIndex))
                ENV.step(actionIndex, d, feature, commands, address, port, apkName, packageName, activityName, specChar)                
                
                #################check crash
                cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -d"
                logText=commands.getstatusoutput(cmd)
                logText=logText[1]
                
                
                
                
                #send a random intent
                cmd="python /SPACE/stoat/Stoat-master/Stoat/trigger/tester.py -s emulator-5554 -f /SPACE/test/i4nc4mp.myLock_28_src/bin/MainPreferenceActivity-debug.apk -p random"
                aa=commands.getstatusoutput(cmd)
                print(aa)
                
                
                
                
                if "FATAL" in logText or "fatal" in logText:
                    
                    logBoolean,newLogAdd, specOut=ENV.checkBefore(logText,logHistory)
                    if specOut==True and specChar==False:
                        specChar=True
                    if not logBoolean:
                    
                        crashTag=True
                        ENV.writeCrash(logText,iterCount)
                        logHistory+=newLogAdd
                        className=ENV.restartApp(port,commands, packageName, activityName)
                        print("catch a crash and restart app")
                    else:
                        crashTag=False
                        className=ENV.restartApp(port,commands, packageName, activityName)
                        print("catch a crash and restart app")
                        
                        #lasteventInRecord=None
                    restartTag=True

                        
                else:
                    crashTag=False
            
            
            
            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window windows | grep -E 'mFocusedApp'"
            tupleLine=commands.getstatusoutput(cmd)
            className=str(tupleLine).split(" ")[-2]
    
    
            #avaiableAnotherSet
            #if not packageName in tupleLine[1] and not any((s in tupleLine[1]) for s in avaiableAnotherList):
            if not packageName in tupleLine[1] and not "com.android" in tupleLine[1] or "com.android.launcher" in tupleLine[1]:

                appCloseTag=True
                className=ENV.restartApp(port,commands, packageName, activityName)
                restartTag=True
                
            else:
                appCloseTag=False
                
            #################check menu
            #menuTag=ENV.checkMenu(commands, port)
            
            
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
                        
                    for iterTimes in range(0,5):
                        
                        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window windows | grep -E 'mFocusedApp'"
                        tupleLine=commands.getstatusoutput(cmd)
                        
                        if not packageName in tupleLine[1]:
                            d.wait.update()
                            time.sleep(0.5)
                            d.press.back()
                        else:
                            className=str(tupleLine).split(" ")[-2]
                            break
                        
                        if iterTimes==4:
                            print("restart")
                            className=ENV.restartApp(port,commands, packageName, activityName)
                            restartTag=True
                    root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
        
    
            ##########################remove
            os.remove(address+'/middleResults/result.xml')
            
            #######################compare similarity
            sameEvent, similarEventList, sameResultListMiddle,similarResultListMiddle=Similar.getSimilar(recordRoot,root_Result)
            
            ######################extract feature
            feature=Feature.FeatureClass(root_Result,sameResultListMiddle, similarResultListMiddle, sameEvent, similarEventList)
            
            
            
            featureStepNum=len(feature.runableList)
            
            
            textFeatue=Feature2Digit.textFeature2Digit(feature,word2Idx)####just encode to the word ID
            sameFeature,similarFeature=Feature2Digit.sameFeatureExtract(feature)
            
            featureTuple=(textFeatue,sameFeature,similarFeature)#########generate feature for machine learning input
            
            ######################run model
            actionIndex,predictTime=agent.act(featureTuple, iterCount)
            totalPredictTime+=predictTime
            #actionIndex=np.argmax(action)
            
            print("actionIndex: "+str(actionIndex))
            ##########################recordRoot
            lastEventInRecord, lastSimilarEleList=Similar.addToRecordRoot(recordRoot, root_Result,resultId,feature,featureStepNum,actionIndex,sameEvent, similarEventList, lastEventInRecord, restartTag, lastSimilarEleList)
            ############################record into file
            doc_write =Document()
            doc_write.appendChild(recordRoot)  
            with codecs.open(address+"/middleResults/record.xml","wb","utf-8") as out:
                doc_write.writexml(out)
            out.close()
            
            ########################add page ID
            resultId+=1
            
            ##################run
            #className=ENV.step(actionIndex, d, feature, commands, address, port)
            
            
            
            ##################memorize and update model, this part can be implemented parallel with run
            if iterCount==0:#it is the first time
                lastFeature=feature
                lastActionIndex=actionIndex 
                
            else:
                #reward=Similar.computeRewardSimilar(feature)
                
                reward=ENV.computeRewardCoverage(commands, port, sourceCodePath, coverageData)
                
                
                
                
                
                
                if crashTag:#######good catch
                    reward=5
                
                
                countReward+=reward
                
                #reward=-0.5
                agent.memorize(lastFeatureTuple, lastActionIndex, reward, featureTuple)
                
                testLastTuple=(lastFeatureTuple, lastActionIndex, reward, featureTuple)
                #################train DQN
                if iterCount > 0:
                    recordMiddleList=[]
                    #loss, trainTimeCost=agent.replay(batch_size, len(lastFeature.runableList),Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList)
                    #totalTimeForTrain+=trainTimeCost
                    print("str: "+str(recordMiddleList))
                
            lastFeature=feature
            lastFeatureTuple=featureTuple
            lastActionIndex=actionIndex
            
        agent.save("./model/keras_model.h5")
        
        outputFile = open("./experimentRecord.txt", 'a')
        outputFile.write("\n")
        outputFile.write("coverage: "+str(coverageData[0])+"\n")
        outputFile.write("itercount: "+str(iterCount)+"\n")
        outputFile.write("totalTimeForTrain: "+str(totalTimeForTrain)+"\n")
        outputFile.write("totalPredictTime: "+str(totalPredictTime)+"\n")
        outputFile.close()
    
if __name__ == '__main__':
    main()         