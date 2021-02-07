# DinoDroid

DinoDroid is a softare tool to automatically test android crashes.

# Source Code Download

[Source Code and Tool](https://drive.google.com/file/d/1gCszF_CN7SUcq6_fWkU6t5Oz3TRRRNTk/view?usp=sharing) are ready. Please check the readme in the downloaded folder.

# Run DinoDroid Using a VirtualBox Image

## Pre-requirements for VirtualBox Image

- Prepare a desktop computer with the following recommended configuration: 32GB memory, 8 kernels cpu, more than 30 GB free disk.
- Download [7 GB VirtualBox image](https://drive.google.com/file/d/1-TkJZyVm9raFH5dvVLmHQYMDDC8_0aNc/view?usp=sharing). The root password of this image is `test_xxx`. There is a [Demo video](https://youtu.be/XP1sAaau8OQ) for using VM.
- Use VirtualBox(we use 5.1.38) to import the VirtualBox image.


## Run DinoDroid

1. Open the virtualbox image.
2. Start an android emulator. Wait (for minutes) until it is totally launched.

```sh
   emulator -avd testAVD -wipe-data
```
Use eclipse to lanuch emulator is another option. See [Demo video](https://youtu.be/XP1sAaau8OQ).

3. Enter the Artifact folder, in which we have 64 Apps in dataset.

```sh
   cd ~/DinoDroid-release/
```

5. Clean all the things in /Result.

```sh
   rm -r /Result/*
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

# Pre-requirements of Tool

We have tested the tool on ubuntu 16.04.

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

## A detailed instruction about how to configure environment.


