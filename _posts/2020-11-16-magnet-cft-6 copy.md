---
title: Magnet Weekly CTF 6 - The Elephant in the Room
excerpt: Solution to the Magnet Forensics CTF 6th week challenge. This week's challenge continues to utilize the Linux Hadoop images for some interesting challenges.
tags: magnet-ctf ctf forensics
author: rms
---

### Catch up time

Unfortunately, due to massive amounts of homework in college, I had to place the Magnet CTF on hold for week 5. This means I had to play catch up for the week 6 challenges. During week 5, Magnet announced they would be using a new image. Out with the phone image and in with the Linux Hadoop image! Actually three images. They can all be downloaded [here](https://archive.org/download/Case2-HDFS). Most of the time was spent learning how to mount the images properly and learn about Hadoop clusters. Once over the hurdle of mounting them and getting the general idea of how Hadoop clusters work, this challenge wasn't to bad.

### The first challenge

> Hadoop is a complex framework from Apache used to perform distributed processing of large data sets. Like most frameworks, it relies on many dependencies to run smoothly. Fortunately, it’s designed to install all of these dependencies automatically. On the secondary nodes (not the MAIN node) your colleague recollects seeing one particular dependency failed to install correctly. Your task is to find the specific error code that led to this failed dependency installation. [Flag is numeric]

Quite possibly the longest question yet. In summary, we need to find the error code for a dependency that failed to install correctly. These images utilize apt for handling dependencies, so lets check the apt logs first.

The apt logs can be found in `/var/log/apt/`. Two logs are present here: `history.log` and `term.log`. First lets check `history.log`. Using the command `cat history.log | grep -C 10 "Error"` shows that there are several error codes in the file. 

```
Start-Date: 2017-11-08  01:23:15
Commandline: apt-get install oracle-java8-installer
Requested-By: hadoop (1000)
Install: oracle-java8-set-default:amd64 (8u151-1~webupd8~0, automatic), oracle-java8-installer:amd64 (8u151-1~webupd8~0)
Error: Sub-process /usr/bin/dpkg returned an error code (1)
End-Date: 2017-11-08  01:28:31

Start-Date: 2017-11-08  01:28:55
Commandline: apt-get install -f
Requested-By: hadoop (1000)
Error: Sub-process /usr/bin/dpkg returned an error code (1)
End-Date: 2017-11-08  01:29:12
```

Immediately, we see there  is the error code `1`. However, this is repeated several times in the file for other non-dependency items. So lets check further. We can see that java failed to install correctly several times. Hm. Lets check the `term.log` for the failed install. Same command, different file: `cat term.log | grep -C 10 "Error"`. A snippet of the output is shown below.

```
HTTP request sent, awaiting response... 302 Moved Temporarily
Location: http://download.oracle.com/otn-pub/java/jdk/7u80-b15/jdk-7u80-linux-x64.tar.gz?AuthParam=1510098741_f9941383709eb00c84f24bce765baa81 [following]
--2017-11-08 01:50:20--  http://download.oracle.com/otn-pub/java/jdk/7u80-b15/jdk-7u80-linux-x64.tar.gz?AuthParam=1510098741_f9941383709eb00c84f24bce765baa81
Connecting to download.oracle.com (download.oracle.com)|151.248.100.43|:80... connected.
HTTP request sent, awaiting response... 404 Not Found
2017-11-08 01:50:22 ERROR 404: Not Found.

download failed
Oracle JDK 7 is NOT installed.
dpkg: error processing package oracle-java7-installer (--configure):
 subprocess installed post-installation script returned error exit status 1
Errors were encountered while processing:
 oracle-java7-installer
Log ended: 2017-11-08  01:50:22
```

We can see that it errored out several times with error `404`. Entering that as the solution shows that it is indeed the correct answer!

### The second challenge

Surprise! Another challenge appears after the first one is solved. This one is worth 50 points.

> Don’t panic about the failed dependency installation. A very closely related dependency was installed successfully at some point, which should do the trick. Where did it land? In that folder, compared to its binary neighbors nearby, this particular file seems rather an ELFant. Using the error code from your first task, search for symbols beginning with the same number (HINT: leading 0’s don’t count). There are three in particular whose name share a common word between them. What is the word?

Another long question. In summary, the question asks us to find a closely related dependency to the one that failed earlier(`Oracle JDK 7`). Then it wants us to find a common word in the symbols that begin with the error code (`404`) of an ELF file in that folder. Phew. An ELF (Executable and Linkable Format) file is the standard executable file format for Linux based systems. 

After a bit of searching, it is easily found that JDK 1.8.0 was eventually installed on the system at `/usr/local/jdk1.8.0_151/`. The question says there are binary neighbors near by, so it's probably safe to assume it means the `/usr/local/jdk1.8.0_151/bin` directory where the executables are stored. There are actually a total of 42 ELF files stored in that directory. 

No problem though, we can use `readelf` to show the symbols for all the files in the directory and use grep to parse the output for `404`. This command looks like `readelf --symbols usr/local/jdk1.8.0_151/bin/* | grep 404`. This returns the following output:

```
readelf: Error: Not an ELF file - it has the wrong magic bytes at the start
readelf: Error: Not an ELF file - it has the wrong magic bytes at the start
readelf: Error: Not an ELF file - it has the wrong magic bytes at the start
readelf: Error: Not an ELF file - it has the wrong magic bytes at the start
   269: 0000000000618404     0 NOTYPE  LOCAL  HIDDEN    19 __init_array_end
   270: 0000000000618404     0 NOTYPE  LOCAL  HIDDEN    19 __init_array_start
   404: 0000000000412c1d    16 FUNC    GLOBAL DEFAULT   14 gtk2_open
readelf: Error: Not an ELF file - it has the wrong magic bytes at the start
    49: 0000000000404358     0 OBJECT  LOCAL  DEFAULT   16 __FRAME_END__
readelf: Error: Not an ELF file - it has the wrong magic bytes at the start
readelf: Error: Not an ELF file - it has the wrong magic bytes at the start
    21: 0000000000404260  1098 FUNC    LOCAL  DEFAULT   15 deflate_fast
    22: 00000000004046b0  1367 FUNC    LOCAL  DEFAULT   15 deflate_stored
   246: 0000000000404c10  4477 FUNC    GLOBAL DEFAULT   15 deflate
   404: 0000000000410f60   175 FUNC    GLOBAL DEFAULT   15 _ZN8unpacker20re[...]
```

If you look closely, you can see that there are several that have a shared word - `deflate_fast` `deflate_stored` and `deflate`. Entering `deflate` as the answer shows it is the correct solution. These symbols came specifically from the `unpack200` binary in that folder. I'm not sure if there was a way to find that specific binary, but nevertheless the challenge is solved.