# DinoDroid

DinoDroid is a tool that can automatically test android bugs.

[Source Code and Tool](https://drive.google.com/file/d/1gCszF_CN7SUcq6_fWkU6t5Oz3TRRRNTk/view?usp=sharing) are ready. Please check the readme in the downloaded folder.

Prepare a desktop computer with the following recommended configuration: 32GB memory, 8 kernels cpu, more than 50 GB free disk.

Download 7 GB [VirtualBox image](https://drive.google.com/file/d/1-TkJZyVm9raFH5dvVLmHQYMDDC8_0aNc/view?usp=sharing). The root password of this image is test_xxx. There is a [Demo video](https://youtu.be/XP1sAaau8OQ) for using VM.

Use VirtualBox(we use 5.1.38) to import the VirtualBox image.

The emulator in VirtualBox is much slower than a physical machine. So it can only be used to be a demo or guidance for configuration.

I will write detailed instructions and polish the readme before the end of Feb 8, 2021.

## Dataset

Dataset is at https://drive.google.com/file/d/18CiCNq04uKsKUqjKialc15OFDVE0JRa_/view?usp=sharing

## Pre-requirements

It needs keras, uiautomator, and gensim to run.

The Operating system is ubuntu 16.04

library Versions:

apt-get install libgl1-mesa-dev

python 2.7

python -m pip install –user pip==19.1.1

python -m pip install –user genism==3.8.0

python -m pip install –user scipy==1.2.1

python -m pip install –user numpy==1.16.4

python -m pip install –user keras==2.2.4

python -m pip install -user tensorflow==1.5.0

python -m pip install -user uiautomator==1.0.2

python -m pip install --user objgraph

python -m pip install –-user psutil


