---
title: iOS Restrictions Code Cracking
excerpt: Diving into recovering a forgotten iOS device's restrictions passcode and writing a tool to do so automatically. 
categories: [Hacking, iOS]
tags: forensics programming
author: clark
---

## Background

This is a tool I wrote three years ago, but had to use again recently. So, I thought I would make a write up about it. Growing up in a family of 7 and being the one most interested in technology meant I became tech support for my family. As the oldest sibling, I would teach my siblings how to use computers, phones, and iPods. I would also help my parents with handling my sibling's technology. One day, my mother came to me asking if I could get a forgotten passcode for her off my youngest sibling's iPod. Surprisingly though, it wasn't the device passcode - it was the passcode to the restrictions.

## iOS Restrictions Passcode

Apple allows restrictions to be set up on their devices. The primary use of these is for parental control - such as disabling installing apps or disabling 18+ music downloads. The restrictions require a separate password be set for access to the restrictions control page. If this code is forgotten, there is no way to recover it. Typically, the device would have to be reset. I didn't exactly want to reset the device, so my goal was to find or crack the restrictions passcode.

### Where to find it?

That's what I wanted to find out. First, lets grab a jailbroken device and browse around the file system. Since the passcode is entered directly into a page in settings, we can start there looking for a base64 encoded passcode or something simple. Under `/var/mobile/Library/Preferences` is a property list file called `com.apple.restrictionspassword.plist`. Hm. `restrictionspassword`? Sounds interesting. This file contains a single dictionary, with two data keys: `RestrictionsPasswordKey` and `RestrictionsPasswordSalt`. It looks like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>RestrictionsPasswordKey</key>
	<data>
	+ELsJPG2ko6AHAK3KZe/uooMFR8=
	</data>
	<key>RestrictionsPasswordSalt</key>
	<data>
	R9C4DA==
	</data>
</dict>
</plist>
```

Hm. The `=` and `==` characters at the end of the hash and salt are dead give aways of base64 encoding. Decoding it gives us: `f8 42 ec 24 f1 b6 92 8e 80 1c 02 b7 29 97 bf ba 8a 0c 15 1f` That's not much, it's not even mostly printable characters. It is exactly 160 bits long though. What else is 160 bits long? A few hashing functions: 

- SHA-1
- SHA-0
- FSB-160
- HAS-160
- HAVAL-160
- RIPEMD-160
- Tiger-160

So this is very likely a hash of some sort. But what algorithm? Thankfully, someone on the [hashcat](https://hashcat.net/forum/thread-2892.html) forums had this same question, and another user answered.  


![Start Screen](https://starwarsfan2099.github.io/public/2021-08-03/post.jpg){:.shadow}{:.center}


So, this user states that the hashing algorithm is `pbkdf2-hmac-sha1 ((Password-Based Key Derivation Function 2)`. He also explains how he figured out it is iterations of the algorithm. This will be useful later. Since this is a hashing function it needed to be bruteforced. Thankfully, the iOS restrictions only allow for a four digit code to be set as the passcode. So the keyspace is only 0000-9999 which seemed easy enough to bruteforce.

### How to get the file though?

First we have a problem though. My sibling's iPod was not jailbroken. So how do we get to this file? Hmmmmm. With some Googling, we can learn the restrictions passcode is placed back on the device after a backup and restore. This meant the file or at least the hash and salt definitely is copied to the computer during a backup. This seems like a good way to find the file. 

So, I made a backup of the iPod and my iPhone with a restrictions set in case there were changes across devices or versions in how the hash and salt is copied over. Backups were made using iTunes. On Windows, backups are stored at `C:\Users\<user>\AppData\Roaming\Apple Computer\MobileSync\Backup`. On Mac, they are stored under `/Library/Application Support/MobileSync/Backup/`. In this folder are the different backups, even if it doesn't look like it at first.  


![Backup List](https://starwarsfan2099.github.io/public/2021-08-03/list.JPG){:.shadow}{:.center}


Inside the folders that are a backup of a device, there is an `Info.plist` file that eventually contains the device name and information.

```xml
...
<key>Build Version</key>
	<string>18C66</string>
	<key>Device Name</key>
	<string>iPod touch</string>
	<key>Display Name</key>
	<string>iPod touch</string>
	<key>GUID</key>
	<string>REDACTED</string>
	<key>Installed Applications</key>
	<array>
		<string>com.fingersoft.hillclimbracing2</string>
		<string>com.fboweb.MyRadar</string>
	</array>
	<key>Last Backup Date</key>
	<date>2021-02-09T20:26:38Z</date>
	<key>Product Name</key>
	<string>iPod touch</string>
	<key>Product Type</key>
	<string>iPod9,1</string>
	<key>Product Version</key>
	<string>11.3.1</string>
	<key>Serial Number</key>
	<string>REDACTED</string>
	<key>Target Identifier</key>
	<string>REDACTED</string>
	<key>Target Type</key>
	<string>Device</string>
	<key>Unique Identifier</key>
	<string>REDACTED</string>
	<key>iTunes Files</key>
	<dict>
...
 ```

Now we know which folder pertains to which devices! Next, I searched my iPhone backup for the hash I found in the `.plist` file that I knew was somewhere in the backup. I searched for files that had `restrictionspassword` in the file name or `+ELsJPG2ko6AHAK3KZe/uooMFR8=` in the file contents.

This results in a file having the hash! It was in a file named `398bc9c2aeeab4cb0c12ada0f52eea12cf14f40b`. However, looking for this file in the iPod backup yielded no results. But, with a quick search for the file name, it was found at `39\398bc9c2aeeab4cb0c12ada0f52eea12cf14f40b`. Now, I had the hash and salt for the iPod!

### Bruteforcing the hash

We can use Python to bruteforce the hash. First, we need a python implementation of `pbkdf2-hmac-sha1`. Luckily, there is already one in the Python module `passlib` - a python hashing library. It needs to be installed with `pip install hashlib`. We will also need to import `b64decode()` from the `base64` module. Now we can write a simple function to bruteforce the passcode. It should:

- base64 decode the hash and salt
- loop over passcode iterations 0000 to 9999
- hash each passcode with `pbkdf2()` from passlib
- pass `pbkdf2()` the current passcode, salt, and rounds (`1000` from earlier)
- compare the hash to the one provided
- if they match, the current passcode iteration is the restrictions passcode
- if they don't, continue looping and iterating

With that basic outline, we get the following simple code:

```python
from passlib.utils.pbkdf2 import pbkdf2
from base64 import b64decode

def crackRestrictionsKey(base64Hash, base64Salt):
    secret = b64decode(base64Hash)
    salt = b64decode(base64Salt)
    for i in range(10000):
        key = "%04d" % i
        out = pbkdf2(key, salt, 1000)
        if out == secret:
            print "[+] Passcode: %s" % key
```

Now we can run the function with our hash and salt: `crackRestrictions("+ELsJPG2ko6AHAK3KZe/uooMFR8=", "R9C4DA==")`. And we get the passcode - `[+] Passcode: 2589`!! With this information, the restrictions on my brother's iPod could be adjusted without the need for resetting the device. This might have happened a few more times. So, I just wrote a whole python script to automatically parse the backups and do everything on both Windows and Mac. It can be found [here](https://github.com/Starwarsfan2099/iOS-Restriction-Key-Cracker/blob/master/KeyCracker.py). Happy hacking!