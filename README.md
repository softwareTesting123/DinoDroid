# DinoDroid

DinoDroid is a software tool to automatically test android crashes.

A Quick YouTube Demo of DinoDroid: https://youtu.be/SQwg9Sgcjl0

# Source Code Download

[Source Code and Tool](https://drive.google.com/file/d/1gCszF_CN7SUcq6_fWkU6t5Oz3TRRRNTk/view?usp=sharing) are ready. Please check the readme in the downloaded folder or check `Run DinoDroid` below.

# Run DinoDroid Using a VirtualBox Image

## Pre-requirements for VirtualBox Image

- Prepare a desktop computer with the following recommended configuration: 32GB memory, 8 kernels cpu, more than 30 GB free disk.
- Download [7 GB VirtualBox image](https://drive.google.com/file/d/1-TkJZyVm9raFH5dvVLmHQYMDDC8_0aNc/view?usp=sharing). The root password of this image is `test_xxx`. There is a [Demo video](https://youtu.be/XP1sAaau8OQ) for using VM.
- Use VirtualBox(we use 5.1.38) to import the VirtualBox image.


## Run DinoDroid

1. Open the virtualbox image.
2. Start an android emulator. Wait (for minutes) until it is totally launched. Notice that we disable the automated launch of the emulator in this image because it is so slow. 

   Use eclipse to launch emulator see [Demo video](https://youtu.be/XP1sAaau8OQ).

3. Enter the Artifact folder, in which we have 64 Apps in dataset.

```sh
   cd ~/DinoDroid-release/
```

5. Clean all the things in /Result.

```sh
   rm -r /Result/*
```

6. Clean all the existing models in /Model (or DinoDroid will continue to train the existing model).

```sh
   rm /Model/keras_model_half.h5
   rm /Model/keras_model.h5
```

4. Run Training (Every app in dataset/unfinished costs 1 hour).

```sh
   python RunTrain.py
```

5. Clean all the things in /Result.

```sh
   rm -r /Result/*
```


6. Run Testing (Every app in dataset/unfinished costs 1 hour).

```sh
   python RunTest.py
```

7. See Coverage and Crash Results

```sh
   cd ~/DinoDroid-release/Result
```

Notice that the emulator in VirtualBox is much slower than a physical machine. So it can only be used to be a demo or guidance for configuration.

# Dataset

Dataset is at https://drive.google.com/file/d/18CiCNq04uKsKUqjKialc15OFDVE0JRa_/view?usp=sharing

All of apps in the dataset are from [AndroTest](http://bear.cc.gatech.edu/~shauvik/androtest/).

# Pre-requirements of Tool

We have tested DinoDroid on ubuntu 16.04 and Android 4.4.2.

## Library Versions:

python 2.7

apt-get install libgl1-mesa-dev

python -m pip install –user pip==19.1.1

python -m pip install –user genism==3.8.0

python -m pip install –user scipy==1.2.1

python -m pip install –user numpy==1.16.4

python -m pip install –user keras==2.2.4

python -m pip install -user tensorflow==1.5.0

python -m pip install -user uiautomator==1.0.2

python -m pip install --user objgraph

python -m pip install –-user psutil


You can build the execution environment following this [instruction](https://drive.google.com/file/d/15-MAENDHUPBoxGG6SnSZLITUIlMZyHpx/view?usp=sharing).

## Need to configure android path in setting

```sh
Adb Path:/home/xxx/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb
AVD Name:testAVD
AVD Emulator Path:/home/xxx/adt-bundle-linux-x86_64-20140702/sdk/tools/emulator
AAPT Path:/home/xxx/adt-bundle-linux-x86_64-20140702/sdk/build-tools/23.0.3/aapt
Emma Path:/home/xxx/adt-bundle-linux-x86_64-20140702/sdk/tools/lib/emma.jar
Time(Sec):3600
```


# Description of Result Files Generated By DinoDroid:

## Coverage Results

The coverage results in /Result:

```sh

XXX_coverage_0.txt

XXX_coverage_1.txt

XXX_coverage_2.txt

```

XXX is the app source code folder name

## Crash Results

The crash results in /Result:

```sh

XXX_crash_0.txt

XXX_crash_1.txt

...

XXX_crash_ith.txt

```

XXX is the app source code folder name

## Samples

Every sample in the training and testing will be recorded in /Result:

```sh

xxx_trainRecord_              means the current sample 

xxx_trainRecordOther_         means the sample in memory


```

Users may use them to understand how our model works.

## Event Flow Graph in /Result

```sh

/Result/xxx_record_0.xml

/Result/xxx_record_1.xml

/Result/xxx_record_2.xml

```

XXX is the app source code folder name

## Trained Model in /model (Generate after the train)

```sh

keras_model_half.h5

```

Two trained models (train 32 apps for each) can be used directly to and run testing by copying one of them into /model.

One is [here](https://drive.google.com/file/d/1GzWX9OeAC4vnuMyHA6eBq3yOSShhRoFX/view?usp=sharing). 

The other one is [here](https://drive.google.com/file/d/1WMe_ViO0H5jA29-Lz66pwwUTK8jYw_Md/view?usp=sharing).


