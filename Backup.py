#!/usr/bin/python3

# This is a small Python script which allows you to
# backup your files temporary and after you turn off
# your unix-based system, everything you just coppied
# wil be deletd cause they're placed on '/tmp/' directory.
# So don't worry about the SPACE

import os
import datetime
import shutil

target_dir = "/tmp/backup" + os.getcwd().split('/')[-1] + '_' + datetime.datetime.now().strftime('%b-%d_%H:%M:%S')

if not os.path.exists(target_dir):
    os.mkdir(target_dir)

currentPath = os.getcwd()
size = len(os.listdir(currentPath))
for i, item in enumerate(os.listdir(currentPath)):
    if (i+1) % size//5 == 0:
        print(str((i+1) * 100 // size) + "% has been copied...")
    s = os.path.join(currentPath, item)
    d = os.path.join(target_dir, item)
    if os.path.isdir(s):
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)

print("Now you have a copy of this directory at:\n" + target_dir)