---
title: Decrypting DJI Spark Drone Log Files
excerpt: DJI Spark Drones have a feature that allows them to transfer files to a computer. Some of these appear to be "black box" encrypted log files. By running and reversing the drone's firmware inside of QEMU, the encryption keys and methods can be determined.
categories: [Hacking, Drones]
tags: reverse-engineering forensics
author: clark
---

DJI Spark drones come with a companion application used to transfer files between the drone and the computer. Some mysterious log files can be transferred using application. However, they appear to be encrypted for some reason. transferred DJI Spark Drone's log files look something like this after being transferred to a computer.

![Image](https://starwarsfan2099.github.io/public/2020-1-25/Pic_1.png){:.shadow}{:.center}{: width="1185" height="551" }

The first step in figuring out how to decrypt the DJI Spark drone encrypted files is to analyze the firmware used by the drone. The firmware downloads for the Spark drone can be gotten from cache files in the DJI software after it has been used to update the drone, or it can be downloaded from DJI’s servers using [DankDroneDownloader](https://github.com/cs2000/DankDroneDownloader). This tool can be used to download multiple versions of the firmware used on several different drones, including the Spark. Once the firmware is downloaded, you can extract the `.tar` file or `.bin` (still `.tar`, just renamed) depending on the firmware version. This will produce several `.sig` files. After extracting and exploring many `.sig` files, the main system layout and executables can be extracted. Looking for anything that could provide ftp support, the BusyBox executable was found in/   `system/xbin`. [BusyBox](https://www.busybox.net/) is an open source tool containing many Linux tools and commands into one executable designed for embedded Linux systems. BusyBox does not contain any sort of encryption in its ftp source, so DJI must have added their own. 


The system and BusyBox files can be extracted from the firmware `.sig` files by first searching them for BusyBox using `grep busybox wm* -r`. If grep finds the BusyBox in one of the files, the file system can be extracted with Binwalk, for example `binwalk -e wmɩɩ0_0ɯ0ɨ.pro.fw.sig`. The next step was to figure out the encryption method. The binary could be reversed, but the binary includes a lot of functions to work through, so I chose to use a virtual environment to run BusyBox and inspect it from there. To get BusyBox running, I ran it in an Arm chroot with Qemu. I installed qemu-user-static with `sudo apt-get install qemu-user-static then told it to build the chroot with sudo qemu-debootstrap --arch armhf jessie eabi-chroot`. That installs and sets up an environment in a folder called `eabi-chroot`. To get BusyBox running, I copied the BusyBox binary into the root of the `eadi-chroot`. I also created a folder `ftp` in the root as well, as BusyBox looks for this folder when starting the ftp environment. Inside the `ftp` folder, I placed a `test.txt` file used to test if ftp was working or not. BusyBox can then be launched with `sudo chroot eabi-chroot`, then running `./busybox tcpsvd -vE 0.0.0.0 21 ./busybox ftpd -wv /tmp/` to get the ftp server running.

![Image](https://starwarsfan2099.github.io/public/2020-1-25/Pic_2.png){:.shadow}{:.center}{: width="1177" height="363" }

Image 2. BusyBox FTP server running in Qemu. I then connected to the ftp server with the username `nouser` and requested a file.

![Image](https://starwarsfan2099.github.io/public/2020-1-25/Pic_3.png){:.shadow}{:.center}{: width="735" height="489" }

Image 2. FTP server successfully transferring files. `GDB` and `radare2` were attached to the process and `Ghidra` was used for static analysis to locate the file transfer functions. Now that a file has been requested, I used the debuggers and `Ghidra` to determine that the key wasplaced into memory. I used several different tools to look at the process memory for possible encryption keys or signatures, finally landing on [AES finder](https://github.com/mmozeiko/aes-finder) and discovering it used AES encryption. The tool revealed DJI used an AES-128 bit encryption and it pulled the key from memory, but it did not find the IV. Now that the encryption and the AES key is known, it is significantly easier to look for specific encryption functions in the binary by searching for the AES key. Following the function where the AES key is used, it leads to the IV and later the packing used.

![Image](https://starwarsfan2099.github.io/public/2020-1-25/Pic_4.png){:.shadow}{:.center}{: width="776" height="109" }

Image 4. AES IV located inside the BusyBox binary shown with `Ghidra`. Knowing the AES key, the IV, and the packing, it is trivial to write asmall Python script to decrypt the files:


```python
# Created by Andrew Clark on 7/30/19
import sys, os 
from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder 
key = "YP1Nag7ZR&Dj\x00\x00\x00\x00" 
iv  = "0123456789abcdef" 
aes = AES.new(key, AES.MODE_CBC, iv)

if len(sys.argv) < 2:
    print "Usage: decrypt.py FILE"
    exit()
 else:
    if os.path.isfile(sys.argv[1]):                 
        print "Opening and decrypting file..."                 
        encryptedFile = open(sys.argv[1], 'rb').read()            
        decryptedFile = aes.decrypt(encryptedFile)
        encoding = PKCS7Encoder()
        decodedFile = encoding.decode(decryptedFile)
        outputFile = open(sys.argv[1] + ".decrypted", 'w+')
        outputFile.write(decodedFile)
        outputFile.close()
        print "Done. \nDecrypted file was written to %s" % sys.argv[1] + ".decrypted"
    else:
        print "Could not open file."
```


The IV did not change across drone versions, but the AES key did twice, the most recent versions all have the same key though. Knowing
the IV, it is now easiest to get the AES key for future versions by checking in a disassembler if the IV string is present and locating the AES
key in that same function. Or simply searching for the following bytes will produce the AES function: `06 30 9f e7 03 30 90 e7 02 00 53 e3 09 00 00 0a`.

In the end, the log files look like this:

![Image](https://starwarsfan2099.github.io/public/2020-1-25/Pic_5.png){:.shadow}{:.center}{: width="1084" height="597" }

The process outline for decrypting the drone data was as follows:
- Obtain drone filesystem.
    - Done by searching for open source DJI Drone firmware downloading tools.
- Determine how to extract drone firmware.
    - Completed by examining headers and using binwalk to extract the filesystem.
- Determine what part of the firmware deals with log files.
    - Firmware was examined to determine what software ran on the drone.
        - After BusyBox was determined to be running on the drone, it's source code was analyzed to find file transfer and logging functions.
- Attempt to run drone software in a visualized environment for debugging.
    - I researched QEMU and visualizing embedded systems, trying various configurations to get BusyBox running.
- Debug BusyBox to determine encryption.
    - GDB and Radare were used to debug and determine when the data was encrypted.
        - Ghidra was used to disassemble the BusyBox binary and locate the file transfer functions with help from the debuggers.
            - It was discovered that the key was put into memory, so open source tools were tested against the BusyBox process memory tp pull a key from memory.
- Write a script to decrypt logs.
    - Knowing the key, the encryption could be determined and Ghidra was used to find the encryption functions to obtain the IV and packing type.
        - A Python script was written with open source libraries to decrypt the files with the appropriate key, IV, encryption, and packing.
- Allow for easier obtaining of keys for future drone versions.
    - A unique byte pattern in the encryption function referencing the key and IV was found allowing for disassembler to search for the pattern and immediately obtain references to the key and IV. 