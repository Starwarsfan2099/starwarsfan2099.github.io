---
title: Magnet Weekly CTF 9 - Memory Images...
excerpt: Solution to the Magnet Forensics CTF 9th week challenge. This week's challenges revolve around a new memory dump image for the month of December.
categories: [CTF, Magnet 2020]
tags: magnet-ctf ctf forensics
author: clark
---

### Memory Image?

A new month, a new image to work with in the Magnet CTF. This month's image is a Windows memory dump. It can be found [here on Google Drive](https://drive.google.com/drive/folders/1iCxOKhfoHvxoBRNXJlm2VBiAVgDD_p5d). For the challenges, at least this week, the go to tool will be [Volatility](https://www.volatilityfoundation.org/). A good command reference can be found [here](https://github.com/volatilityfoundation/volatility/wiki/Command-Reference). First, we need to find what system this memory dump is taken from. Volatility needs to know this in order to properly perform commands due to differences between Windows versions in memory management. The best way to do this is to use the `imageinfo` command. Commands can be passed to volatility along with a file specified by `-f`, like this: `volatility -f memdump.mem imageinfo`. 

```
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/starwarsfan2099/Magnet CTF/memdump.mem)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf80002c2a120L
          Number of Processors : 2
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80002c2c000L
                KPCR for CPU 1 : 0xfffff88002f00000L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2020-04-20 23:23:26 UTC+0000
     Image local date and time : 2020-04-20 19:23:26 -0400
```

The first two suggested profiles are WIndows 7, so we'll go with the first one, `Win7SP1x64` as the profile for the rest of the commands. 
{:.success}

### Challenge 9 Part 1 – 25pts

> The user had a conversation with themselves about changing their password. What was the password they were contemplating changing too. Provide the answer as a text string.

Interesting. Maybe the user did so in a file we could pull from memory? Or a process? We can search for opened files with `volatility -f memdump.mem --profile=Win7SP1x64 filescan` and then grep the output for a file extension we're looking for. Unfortunately, no suspicious files or any of interest were found, only some text log files were in the memory. Searching through running process with the `plist` command yields some interesting results though. 

```
Volatility Foundation Volatility Framework 2.6
Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0xfffffa8030e57b00 System                    4      0    108      572 ------      0 2020-04-20 22:44:37 UTC+0000                                 
0xfffffa8032005aa0 smss.exe                280      4      2       30 ------      0 2020-04-20 22:44:37 UTC+0000                                 
0xfffffa8032f05b00 csrss.exe               364    352      9      532      0      0 2020-04-20 22:44:38 UTC+0000                                 
0xfffffa803254d580 wininit.exe             408    352      3       76      0      0 2020-04-20 22:44:38 UTC+0000                                 
0xfffffa8032a29350 csrss.exe               440    416     11      534      1      0 2020-04-20 22:44:38 UTC+0000                                 
0xfffffa803317e8e0 services.exe            472    408      7      241      0      0 2020-04-20 22:44:38 UTC+0000                                 
0xfffffa8033197060 winlogon.exe            508    416      5      117      1      0 2020-04-20 22:44:38 UTC+0000                                 
0xfffffa80331a7b00 lsass.exe               536    408      7      648      0      0 2020-04-20 22:44:38 UTC+0000                                 
0xfffffa80331adb00 lsm.exe                 544    408     10      211      0      0 2020-04-20 22:44:38 UTC+0000                                 
0xfffffa8033227b00 svchost.exe             660    472     11      378      0      0 2020-04-20 22:44:38 UTC+0000                                 
0xfffffa803325c060 vmacthlp.exe            728    472      3       66      0      0 2020-04-20 22:44:38 UTC+0000                                 
0xfffffa8033266060 svchost.exe             772    472     10      336      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa80332b0b00 svchost.exe             860    472     21      514      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa80332fa5f0 svchost.exe             936    472     20      460      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa80333379b0 svchost.exe             980    472     15      655      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa803333db00 svchost.exe             112    472     44     1260      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa8033424860 svchost.exe            1160    472     21      668      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa803343eb00 spoolsv.exe            1304    472     13      287      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa80334d8b00 svchost.exe            1332    472     19      346      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa803357c5f0 svchost.exe            1444    472     10      146      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa80335e7720 VGAuthService.         1520    472      3       86      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa803364a060 vmtoolsd.exe           1576    472     10      289      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa80335edb00 wlms.exe               1636    472      4       46      0      0 2020-04-20 22:44:39 UTC+0000                                 
0xfffffa8033735060 sppsvc.exe             1952    472      4      170      0      0 2020-04-20 22:44:40 UTC+0000                                 
0xfffffa803362c060 svchost.exe            2032    472      6      105      0      0 2020-04-20 22:44:40 UTC+0000                                 
0xfffffa803376e060 svchost.exe            1080    472      7      101      0      0 2020-04-20 22:44:40 UTC+0000                                 
0xfffffa803379eb00 WmiPrvSE.exe           2108    660     12      221      0      0 2020-04-20 22:44:40 UTC+0000                                 
0xfffffa80338145f0 dllhost.exe            2216    472     13      195      0      0 2020-04-20 22:44:40 UTC+0000                                 
0xfffffa803386db00 msdtc.exe              2324    472     12      148      0      0 2020-04-20 22:44:40 UTC+0000                                 
0xfffffa803365b060 svchost.exe            2944    472      9      136      0      0 2020-04-20 22:46:40 UTC+0000                                 
0xfffffa80310b3b00 svchost.exe             360    472     13      361      0      0 2020-04-20 22:46:40 UTC+0000                                 
0xfffffa8031090060 SearchIndexer.         2580    472     13      694      0      0 2020-04-20 22:46:41 UTC+0000                                 
0xfffffa80316f9060 taskhost.exe           1396    472     10      223      1      0 2020-04-20 23:16:53 UTC+0000                                 
0xfffffa8031ea9940 dwm.exe                2852    936      3       82      1      0 2020-04-20 23:16:53 UTC+0000                                 
0xfffffa80317ff060 explorer.exe           2672   2148     31     1018      1      0 2020-04-20 23:16:53 UTC+0000                                 
0xfffffa803140c5f0 WerFault.exe           2164   2508      5      133      1      0 2020-04-20 23:16:54 UTC+0000                                 
0xfffffa8031e80b00 vmtoolsd.exe           2928   2672      9      178      1      0 2020-04-20 23:16:54 UTC+0000                                 
0xfffffa80324e1940 audiodg.exe            1728    860      5      136      0      0 2020-04-20 23:16:54 UTC+0000                                 
0xfffffa803165eb00 slack.exe              2208   2412     28      553      1      0 2020-04-20 23:16:54 UTC+0000                                 
0xfffffa8031ed3710 slack.exe              2728   2208      9      213      1      0 2020-04-20 23:16:59 UTC+0000                                 
0xfffffa8031471b00 slack.exe              1172   2208      7      135      1      0 2020-04-20 23:17:00 UTC+0000                                 
0xfffffa8031688b00 slack.exe              2812   2208     15      325      1      0 2020-04-20 23:17:00 UTC+0000                                 
0xfffffa80338cdb00 slack.exe              2848   2208     14      276      1      0 2020-04-20 23:17:00 UTC+0000                                 
0xfffffa803177bb00 WINWORD.EXE            3180   2672     15      698      1      0 2020-04-20 23:17:06 UTC+0000                                 
0xfffffa8031e2c2c0 chrome.exe             3384   2672     30     1039      1      0 2020-04-20 23:17:07 UTC+0000                                 
0xfffffa8032429060 chrome.exe             3392   3384      7       95      1      0 2020-04-20 23:17:07 UTC+0000                                 
0xfffffa803258cb00 wuauclt.exe            3464    112      3       94      1      0 2020-04-20 23:17:08 UTC+0000                                 
0xfffffa80324ca5c0 chrome.exe             3492   3384      2       56      1      0 2020-04-20 23:17:09 UTC+0000                                 
0xfffffa8033234a80 chrome.exe             3596   3384      9      211      1      0 2020-04-20 23:17:09 UTC+0000                                 
0xfffffa803259db00 chrome.exe             3604   3384     15      329      1      0 2020-04-20 23:17:09 UTC+0000                                 
0xfffffa803271bb00 chrome.exe             3748   3384     12      155      1      0 2020-04-20 23:17:10 UTC+0000                                 
0xfffffa803271db00 chrome.exe             3756   3384     12      166      1      0 2020-04-20 23:17:10 UTC+0000                                 
0xfffffa80333d6060 WmiPrvSE.exe           3440    660     13      332      0      0 2020-04-20 23:17:13 UTC+0000                                 
0xfffffa8033806b00 chrome.exe             4196   3384      8      106      1      0 2020-04-20 23:17:15 UTC+0000                                 
0xfffffa80337d8b00 chrome.exe             4236   3384     13      245      1      0 2020-04-20 23:17:15 UTC+0000                                 
0xfffffa80310b1780 chrome.exe             4404   3384     13      218      1      0 2020-04-20 23:17:19 UTC+0000                                 
0xfffffa80327dcb00 chrome.exe             4600   3384     13      225      1      0 2020-04-20 23:17:32 UTC+0000                                 
0xfffffa8032c66060 iexplore.exe           2984   2672     14      514      1      0 2020-04-20 23:18:35 UTC+0000                                 
0xfffffa8031d34a40 iexplore.exe           4480   2984     18      566      1      1 2020-04-20 23:18:35 UTC+0000                                 
0xfffffa8031ac2b00 FTK Imager.exe         4332   2672     12      421      1      1 2020-04-20 23:19:17 UTC+0000                                 
0xfffffa80326c94e0 WmiApSrv.exe           1092    472      4      106      0      0 2020-04-20 23:19:22 UTC+0000                                 
0xfffffa8033474b00 SearchProtocol         4056   2580      7      317      0      0 2020-04-20 23:23:19 UTC+0000                                 
0xfffffa80321b8690 SearchFilterHo         1996   2580      6       88      0      0 2020-04-20 23:23:19 UTC+0000                                 
0xfffffa8031af5060 chrome.exe             2188   3384     14      480 ------      0 2020-04-20 23:24:22 UTC+0000                                 
0xfffffa8032150b00 chrome.exe             4484   3384     16      184 ------      0 2020-04-20 23:24:22 UTC+0000
```

Slack, Word, and Chrome are all open and in the memory image and could allow the user to talk to himself to some degree. The `memdump` command can be used to dump the process memory. It needs the PID and a file output directory passed to it. There are a lot of Chrome process open, so we'll just start with Slack and Word. For example:

```
> volatility -f memdump.mem --profile=Win7SP1x64 memdump --dump-dir=./ -p 2208
Volatility Foundation Volatility Framework 2.6
************************************************************************
Writing slack.exe [  2208] to 2208.dmp
```

Nothing of interest was found in the Slack dump. However, searching the Word process:

```
> strings 3180.dmp | grep -B 4 -A 4 "password"
1dBm
C:\Windows\fonts
1FCo
bjbj
Hmmm mmaybe I should change my password to: 
wow_this_is_an_uncrackable_password
Great idea warren
Thank you warren
re so smart warren
I know I am Warren
--
march
past
Passy
...
```

And with that, we have Warren talking to himself and revealing the password and solution to this challenge: `wow_this_is_an_uncrackable_password`. 
{:.success}

### Challenge 9 Part 2 – 15pts

> What is the md5 hash of the file which you recovered the password from?

Well, it would appear that the password is in fact in a file stored in memory. We still need to find it, the password found for part 1 was stored in the process memory. Knowing it was done in Word helps narrow it down. Using the `filescan` command earlier revealed no `.doc` or `.docx` files are found. However, we didn't search for temporary word files - `.asd` files. 

```
> volatility -f memdump.mem --profile=Win7SP1x64 filescan | grep asd
Volatility Foundation Volatility Framework 2.6
0x000000013d5eeb30      9      1 R--r-d \Device\HarddiskVolume1\ProgramData\Microsoft\Windows Defender\Definition Updates\{35F875EC-FE8D-4284-8D65-EB27CF6805EF}\mpasdlta.vdm
0x000000013e6de810      1      1 RW-r-- \Device\HarddiskVolume1\Users\Warren\AppData\Roaming\Microsoft\Word\AutoRecovery save of Document1.asd
0x000000013fa62580      7      0 R--rwd \Device\HarddiskVolume1\Windows\System32\rasdlg.dll
```

Ah, a Word autosave file is in memory. It can be dumped using the `dumpfiles` command.

```
> volatility -f memdump.mem --profile=Win7SP1x64 dumpfiles -Q 0x000000013e6de810 --dump-dir=./
Volatility Foundation Volatility Framework 2.6
DataSectionObject 0x13e6de810   None   \Device\HarddiskVolume1\Users\Warren\AppData\Roaming\Microsoft\Word\AutoRecovery save of Document1.asd
```

The file is now saved to `file.None.0xfffffa803316f710.dat` in the working directory. And finally, using `md5sum` presents us with the hash `af1c3038dca8c7387e47226b88ea6e23`. This is the correct solution to the challenge. 
{:.success}

### Challenge 9 Part 3 - 15pts

> What is the birth object ID for the file which contained the password?

This one took some searching, but it turns out the `mftparser` command can provide this information. 

```
> volatility -f memdump.mem --profile=Win7SP1x64 mftparser | grep -A 10 -B 10 "asd"
Volatility Foundation Volatility Framework 2.6
2020-04-20 23:22:36 UTC+0000 2020-04-20 23:22:36 UTC+0000   2020-04-20 23:22:36 UTC+0000   2020-04-20 23:22:36 UTC+0000   Archive & Content not indexed

$FILE_NAME
Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
2020-04-20 23:22:36 UTC+0000 2020-04-20 23:22:36 UTC+0000   2020-04-20 23:22:36 UTC+0000   2020-04-20 23:22:36 UTC+0000   Users\Warren\AppData\Roaming\MICROS~1\Word\AUTORE~1.ASD

$FILE_NAME
Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
2020-04-20 23:22:36 UTC+0000 2020-04-20 23:22:36 UTC+0000   2020-04-20 23:22:36 UTC+0000   2020-04-20 23:22:36 UTC+0000   Users\Warren\AppData\Roaming\MICROS~1\Word\AutoRecovery save of Document1.asd

$DATA


$OBJECT_ID
Object ID: 40000000-0000-0000-0060-000000000000
Birth Volume ID: 005a0000-0000-0000-0056-000000000000
Birth Object ID: 31013058-7f31-01c8-6b08-210191061101
Birth Domain ID: f81101e8-3101-3d66-f800-000000000000

--
```

The birth object id and solution is `31013058-7f31-01c8-6b08-210191061101`. 
{:.success}

### Challenge 9 Part 4 – 20pts

> What is the name of the user and their unique identifier which you can attribute the creation of the file document to? Format: #### (Name)

Unique identifier probably refers to a users SID. Thankfully, there is also a built in command, `getsids`, to recover SID's for processes. Then we can grep the output for the process we want - `WINWORD.exe`.

```
> volatility -f memdump.mem --profile=Win7SP1x64 getsids | grep WINWORD
Volatility Foundation Volatility Framework 2.6
WINWORD.EXE (3180): S-1-5-21-4288132831-552422005-3632184702-1000 (Warren)
WINWORD.EXE (3180): S-1-5-21-4288132831-552422005-3632184702-513 (Domain Users)
WINWORD.EXE (3180): S-1-1-0 (Everyone)
...
```

Obviously, the one we want is for Warren. Using the last 4 digits, the RID, and the name in the format required by the challenge, we get the solution - `1000 (Warren)`. 
{:.success}

### Challenge 9 Part 5 – 25pts

> What is the version of software used to create the file containing the password? Format ## (Whole version number, don’t worry about decimals)

Now we need the Word version used to create the `.asd` file. This can be found by greping the file for *assemblyIdentity processorArchitecture*. 

```
> strings 3180.dmp | grep "assemblyIdentity processorArchitecture"
	<assemblyIdentity processorArchitecture="*" type="win32" name="mso" version="15.0.0.0" />	
	<assemblyIdentity processorArchitecture="AMD64" type="win32" name="winword" version="15.0.0.0"/>
	<assemblyIdentity processorArchitecture="*" type="win32" name="vbeui" version="7.1.0.0" />
	<assemblyIdentity processorArchitecture="*" type="win32" name="mso" version="15.0.0.0" />	
	<assemblyIdentity processorArchitecture="AMD64" type="win32" name="wwlib" version="15.0.0.0"/>
	<assemblyIdentity processorArchitecture="*" type="win32" name="oart" version="15.0.0.0" />
```

The Word version used to create the file and the solution to the challenge is `15`. 
{:.success}

### Challenge 9 Part 6 – 20pts

> What is the virtual memory address offset where the password string is located in the memory image? Format: 0x########

The [strings section](https://github.com/volatilityfoundation/volatility/wiki/Command-Reference#strings) of the command reference gives how to find this. First we need to use the `strings` tool to get the decimal offset (`-td`) of the string and then output that and the string to a file.

```
> strings -td memdump.mem | grep "wow_this_is_an_uncrackable_password" > strings.txt
```

Then we can import the file into the `strings` plugin in Volatility to get the virtual memory address. 

```
> volatility -f memdump.mem --profile=Win7SP1x64 strings -s strings.txt
Volatility Foundation Volatility Framework 2.6
183577133 [3180:02180a2d] wow_this_is_an_uncrackable_password
```

The solution to this challenge is `0x02180a2d`.
{:.success}

### Challenge 9 Part 7 – 20pts

> What is the physical memory address offset where the password string is located in the memory image? Format: 0x#######

Well, the physical offset is the decimal offset we needed in the last question to find the virtual address. We just need to convert it to hex.

```
> cat strings.txt 
183577133 wow_this_is_an_uncrackable_password
> printf '0x%x\n' 183577133
0xaf12a2d
```

The solution and physical address offset in hex is `0xaf12a2d`. 
{:.success}