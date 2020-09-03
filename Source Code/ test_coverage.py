# should do this to clean the history data


#adb shell rm -r sdcard/coverage.ec

# adb -s emulator-5554 shell rm -r sdcard/*
import commands
import ENV
import os

port="5554"

apkList=[]

for folderName in os.listdir("/SPACE/test/"):
        
        for i in range(0,3):#for the test
            sourceCodePath="/SPACE/test/"+folderName+"/bin/"
            apkFile,coverageEm,packageName,activityName=ENV.compileApkEmma(sourceCodePath, commands, os)
        
            apkList.append((apkFile,coverageEm,packageName,activityName,sourceCodePath))
        break#for the test

apkItem=apkList[0]

apkName=apkItem[0]
coverageEm=apkItem[1]
packageName=apkItem[2]
activityName=apkItem[3]
sourceCodePath=apkItem[4]


######################################coverage data
lineCoverage=0
methodCoverage=0
classCoverage=0

coverageData=[lineCoverage,methodCoverage,classCoverage]#class is not the activity coverage
reward=ENV.computeRewardCoverage(commands, port, sourceCodePath, coverageData)


'''
###############clean coverage.ec
path="/SPACE/reforce-project/dataset/notrun/SpriteText/bin/"

#path="/SPACE/test/com.hectorone.multismssender_13_src/bin/"
port="5554"
cmd="rm -r ./coverage.ec"
print(commands.getstatusoutput(cmd))
cmd="rm -r ./emmaOutput.txt"
print(commands.getstatusoutput(cmd))

##############
cmd1="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb shell am broadcast -a edu.gatech.m3.emma.COLLECT_COVERAGE"
print(commands.getstatusoutput(cmd1))
#########################
cmd2="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb pull /mnt/sdcard/coverage.ec ./coverage.ec"
print(commands.getstatusoutput(cmd2))
########################
cmd3="java -cp /home/yu/adt-bundle-linux-x86_64-20140702/sdk/tools/lib/emma.jar emma report -r txt -in "+ path  +"coverage.em,./coverage.ec -Dreport.txt.out.file=./emmaOutput.txt"
print(commands.getstatusoutput(cmd3))
'''

#coverages/ella_coverage.py:        os.system("adb -s " + device + " shell pm clear " + package_name + " > " + std_out_file)
