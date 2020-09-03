
import commands

for i in range(1000):
    #cmd="python /SPACE/stoat/Stoat-master/Stoat/trigger/"+"tester.py -s i4nc4mp.myLock -p random"
    cmd="python /SPACE/stoat/Stoat-master/Stoat/trigger/tester.py -s emulator-5554 -f /SPACE/test/i4nc4mp.myLock_28_src/bin/MainPreferenceActivity-debug.apk -p random"
    aa=commands.getstatusoutput(cmd)
    print(aa)