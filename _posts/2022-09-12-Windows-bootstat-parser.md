---
title: Windows `bootstat.dat` Forensic Parser
excerpt: Quick post to go over a Python parser for the Windows binary boot log. 
tags: programming forensics
author: rms
published: false
---

## Grzegorz Tworek's PSBits

{:refdef: style="text-align: center;"}
![Tweet](../public/2022-09-12/tweet.JPG){:.shadow}
{: refdef}

Grzegorz Tworek, also known as [0gtweet](https://twitter.com/0gtweet), posted this [link to a PowerShell script](https://github.com/gtworek/PSBits/blob/master/DFIR/Extract-BootTimes.ps1) a few days ago. I thought is was interesting, because I had never heard of this file, much less it being parsed for possible forensic measures. He'd already written a PowerShell script, but I wanted to make a small Python Parser since I'm not very familiar with PowerShell and wanted to learn more about the `bootstat.dat` file.

## Python Parser

Let's look at the first bit of the PowerShell code:

{% highlight powershell linenos %}
$bootstatFilename = "C:\Windows\bootstat.dat"

# Remove to make it less noisy
$DebugPreference = "Continue"

if (!(Test-Path -Path $bootstatFilename))
{
    Write-Host """$bootstatFilename"" doesn't exist. Exiting." -ForegroundColor Red
    return
}

$bytes = Get-Content $bootstatFilename -Encoding Byte -ReadCount 0

if ($bytes.Count -ne (0x10000 + 0x800))
{
    Write-Host "Unsupported file size. Exiting." -ForegroundColor Red
    return
}
{% endhighlight %}

In this code, firstly a variable titled `bootstatFilename` is defined as `C:\Windows\bootstat.dat`. This is the binary log file we want to parse. `$DebugPreference = "Continue"` is a line that allows the debug output to be printed. We want to print out everything, so we can ignore that. Next is a simple check to make sure the file exists. After that, `bytes` is defined and stores the value returned by `Get-Content $bootstatFilename -Encoding Byte -ReadCount 0`. This gets the bytes from the file. Finally, `if ($bytes.Count -ne (0x10000 + 0x800))` is used to make sure the file length (in bytes) is not equal to `0x10000 + 0x800`. `0x800` is the header size defined later, but I'm not sure where the `0x10000` comes from. Anyway, we can start replicating in Python now.

{% highlight python linenos %}
#!/usr/bin/env python3

import struct # Struct is our friend
import uuid   # Format the GUID
from os import SEEK_END

f = open('C:\\Windows\\bootstat.dat', 'rb')

# Make sure the file is a supported length
header_size = 0x800
f.seek(0, SEEK_END)
if f.tell() != (0x10000 + header_size):
    print('Unsupported file size.')
    exit()
{% endhighlight %} 

First we start out with the python shebang line, then some imports that are needed for later. Then we define `f` and open the `bootstat.dat` file in read-only binary mode with `'rb'`. Then we define the header size. Next, we seek to the end of the file with `os.SEEK_END`. This gives us the ability to get the number of bytes in the file on the next line with `f.tell()`. The the file size comparison is performed and exits if the condition is not met. 

Now let's look at the next bit of Powershell code.

{% highlight powershell linenos %}
function Array2Ulong([byte[]]$b)
{
    [uint32]$f =     ([uint32]$b[3] -shl 24) `
                -bor ([uint32]$b[2] -shl 16) `
                -bor ([uint32]$b[1] -shl  8) `
                -bor ([uint32]$b[0])
    return $f
}

function Array2Uint64([byte[]]$b)
{
    [uint64]$f =     ([uint64]$b[7] -shl 56) `
                -bor ([uint64]$b[6] -shl 48) `
                -bor ([uint64]$b[5] -shl 40) `
                -bor ([uint64]$b[4] -shl 32) `
                -bor ([uint64]$b[3] -shl 24) `
                -bor ([uint64]$b[2] -shl 16) `
                -bor ([uint64]$b[1] -shl  8) `
                -bor ([uint64]$b[0])
    return $f
}

function TimeFields2String([byte[]]$b)
{
    return '{0:d4}-{1:d2}-{2:d2} {3:d2}:{4:d2}:{5:d2}' -f `
    ([uint32]$b[1]*256+[uint32]$b[0]), $b[2], $b[4], $b[6], $b[8], $b[10]
}
{% endhighlight %} 

Here we have three functions: `Array2Ulong`, `Array2Uint64`, and `TimeFields2String`. Just by the function name and it's arguments (bytes), we can tell the first two functions unpack bytes to either a 32-bit unsigned long or 64 bit unsigned integer data type. We can easily do this in Python using the [struct](https://docs.python.org/3/library/struct.html) module. So, we don't need to create functions in Python for those. The `TimeFields2String` is also nearly able to be directly replicated in Python. 

{% highlight python linenos %}
# Format time into a human readable string
def format_time(b):
    return '%s-%02d-%02d %02d:%02d:%02d' % (b[1]*256+b[0], b[2], b[4], b[6], b[8], b[10])
{% endhighlight %} 

Next, the Powershell script defines some more variables:

{% highlight powershell linenos %}
$headerSize = 0x800 #theoretically in some cases can be 0, but let's assume it's 0x800.

$eventLevels = @{
 0 = "BSD_EVENT_LEVEL_SUCCESS"
 1 = "BSD_EVENT_LEVEL_INFORMATION"
 2 = "BSD_EVENT_LEVEL_WARNING"
 3 = "BSD_EVENT_LEVEL_ERROR"
}

#let me know if other values are required
$eventCodes = @{
    0 = "BSD_EVENT_END_OF_LOG"
    1 = "BSD_EVENT_INITIALIZED"
    49 = "BSD_OSLOADER_EVENT_LAUNCH_OS"
    80 = "BSD_BOOT_LOADER_LOG_ENTRY"
}

#let me know if other values are required
$applicationTypes = @{
3 = "BCD_APPLICATION_TYPE_WINDOWS_BOOT_LOADER"
}
{% endhighlight %} 

`eventLevels`, `eventCodes`, and `applicationTypes` are defined along with the header size we already defined in the Python script. 