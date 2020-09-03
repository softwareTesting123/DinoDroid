
#import strand
import re
from xml.dom.minidom import Document
from xml.dom import minidom
from __builtin__ import True
import ENV
import os
import Trans
import time
import Feature
import Similar
import codecs

def run(recordRoot, apkCount, countReward, port, commands, d, address, apkName, packageName, specChar, activityName, logHistory, height, weight, resultId, sourceCodePath, coverageData):
    actionIndex=None
    feature=None
    lastFeature=None
    lastActionIndex=None
    appCloseTag=False
    lastFeatureTuple=None
    crashTag=False
    logHistory=""
    totalPredictTime=0
    
    ####################clean sdcard
    ENV.cleanSd(commands, port)###change to only rm coverage.ec
    
    
    start = time.time()
    
    apkCount+=1
    
    lastEventInRecord=None
    lastSimilarEleList=[]
    
    for iterCount in range(10000):
        restartTag=False
        #menuTag=False
        #adb -s emulator-5556 shell rm -r sdcard/*
        print("apkCount:"+str(apkCount))
        
        
        ####################3every apk only train 2 hours
        
        
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
            if iterCount % 10==0:
                cmd="python /SPACE/stoat/Stoat-master/Stoat/trigger/tester.py -s emulator-5554 -f /SPACE/test/QuickSettings/bin/ShowSettingsActivity-debug.apk -p random"
                intent=commands.getstatusoutput(cmd)
                print(intent)
            
            '''
            cmd="python /SPACE/stoat/Stoat-master/Stoat/trigger/tester.py -s emulator-5554 -f /SPACE/test/QuickSettings/bin/ShowSettingsActivity-debug.apk -p random"
            intent=commands.getstatusoutput(cmd)
            print(intent)
            '''
            
            
            
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
                        restartTag=True
                        break
                root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
    

        ##########################remove
        os.remove(address+'/middleResults/result.xml')
        
        #######################compare similarity
        sameEvent, similarEventList, sameResultListMiddle,similarResultListMiddle=Similar.getSimilar(recordRoot,root_Result)
        
        ##########find the nearest 0
        ######idea record the restart
        ######check the nearest 0 from restart and from the current
        
        actionIndex=Similar.findComplement(recordRoot,root_Result,sameEvent, similarEventList)
        
        if actionIndex=="all is explored":
            #print("aa")
            return None
        
        
        
        
        
        ######################extract feature
        feature=Feature.FeatureClass(root_Result,sameResultListMiddle, similarResultListMiddle, sameEvent, similarEventList)
        
        featureStepNum=len(feature.runableList)

        #actionIndex=13

        #########
        lastEventInRecord, lastSimilarEleList=Similar.addToRecordRoot(recordRoot, root_Result,resultId,feature,featureStepNum,actionIndex,sameEvent, similarEventList, lastEventInRecord, restartTag, lastSimilarEleList)

        resultId+=1
        
        #
        if iterCount==0:#it is the first time
            lastFeature=feature
            lastActionIndex=actionIndex 
            
        else:
            #reward=Similar.computeRewardSimilar(feature)
            
            reward=ENV.computeRewardCoverage(commands, port, sourceCodePath, coverageData)
            print(reward)
        
        
        
        ############################record into file
        doc_write =Document()
        doc_write.appendChild(recordRoot)  
        with codecs.open(address+"/middleResults/record.xml","wb","utf-8") as out:
            doc_write.writexml(out)
        out.close()
        
        
        
        