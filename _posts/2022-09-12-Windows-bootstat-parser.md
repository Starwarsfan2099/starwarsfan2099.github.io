---
title: Windows `bootstat.dat` Forensic Parser
excerpt: Quick post to go over a Python parser for the Windows binary boot log. 
tags: programming forensics
author: rms
published: False
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

`eventLevels`, `eventCodes`, and `applicationTypes` are defined along with the header size we already defined in the Python script. We can easily define these in the Python script using dictionaries. 

{% highlight python linenos %}
eventLevels = { 0:'BSD_EVENT_LEVEL_SUCCESS',
                1:'BSD_EVENT_LEVEL_INFORMATION',
                2:'BSD_EVENT_LEVEL_WARNING',
                3:'BSD_EVENT_LEVEL_ERROR'
}

eventCodes = {  0:'BSD_EVENT_END_OF_LOG',
                1:'BSD_EVENT_INITIALIZED',
                49:'BSD_OSLOADER_EVENT_LAUNCH_OS',
                80:'BSD_BOOT_LOADER_LOG_ENTRY'
}

applicationTypes = {3:'BCD_APPLICATION_TYPE_WINDOWS_BOOT_LOADER'}
{% endhighlight %} 

Now we can start getting into the good stuff in the PowerShell script.

{% highlight powershell linenos %}
$currentPos = $headerSize
$version = Array2Ulong($bytes[$currentPos..($currentPos+3)])
$currentPos +=4

if ($version -ne 4)
{
    Write-Host "Unsupported version: $version. Exiting." -ForegroundColor Red
    return
}

$BootLogStart = Array2Ulong($bytes[$currentPos..($currentPos+3)])
$currentPos +=4
$BootLogSize = Array2Ulong($bytes[$currentPos..($currentPos+3)])
$currentPos +=4
$NextBootLogEntry = Array2Ulong($bytes[$currentPos..($currentPos+3)])
$currentPos +=4
$FirstBootLogEntry = Array2Ulong($bytes[$currentPos..($currentPos+3)])

Write-Debug ("BootLogSize: " + ('0x{0:X}' -f $BootLogSize))
Write-Debug ("BootLogStart: " + ('0x{0:X4}' -f $BootLogStart))
Write-Debug ("FirstBootLogEntry: " + ('0x{0:X4}' -f $FirstBootLogEntry))
Write-Debug ("NextBootLogEntry: " + ('0x{0:X4}' -f $NextBootLogEntry))
{% endhighlight %} 

First, the script defines a new variable called `currentPos` and sets it to the header size (`0x800`). Next, `version` is defined as `Array2Ulong($bytes[$currentPos..($currentPos+3)])`. This is unpacking the bytes at `currentPos + 3` as an unsigned long datatype. The Python equivalent of this is `struct.unpack('<L', f.read(4))`. `struct.unpack()` returns a tuple contains the unpacked data. Passing the function `<L` as the first argument tells it to unpack the data as little-endian unsigned long. The PowerShell script goes on to check if the version is not equal to `4` (`if ($version -ne 4)`), then create three more variables and print them to the screen. 

Let's replicate in Python. 

{% highlight python linenos %}
# Get some info
f.seek(header_size)
version, = struct.unpack('<L', f.read(4))

if version != 4:
    print('Unsupported version.')
    exit()

boot_log_start, = struct.unpack('<L', f.read(4))
boot_log_size, = struct.unpack('<L', f.read(4))
next_boot_log_entry, = struct.unpack('<L', f.read(4))
first_boot_log_entry, = struct.unpack('<L', f.read(4))

print('Version:', version)
print('BootLogStart: 0x%04x' % boot_log_start)
print('BootLogSize: 0x%04x' % boot_log_size)
print('NextBootLogEntry: 0x%04x' % next_boot_log_entry)
print('FirstBootLogEntry: 0x%04x' % first_boot_log_entry)
{% endhighlight %} 

 Just like in the PowerShell script, we need to get the `bootstat.dat` version from the `header_size` offset.  Since `struct.unpack()` takes a bytes argument, we can just use `f.read()` as the second argument. We don't necessarily need to keep track of the current position like in the PowerShell script to pass to functions. So we can just use `f.seek(header_size)` and then `f.read(NUMBER)` will read the next `NUMBER` of bytes after that position. So, to get the version after `f.seek(header_size)`, we can use `version, = struct.unpack('<L', f.read(4))`. Then a simple check to make sure the `version` is equal to `4`. The other variables can be created the same way and then simply print the info. 

{% highlight powershell linenos %}
 $overlap = $true

if ($FirstBootLogEntry -gt $NextBootLogEntry)
{
    $overlap = $false
    Write-Debug "Log partially overwritten due to its circular nature."
}

$currentPos = $headerSize + $FirstBootLogEntry

$arrExp=@()
{% endhighlight %} 

Next, the PowerShell script sets up a variable, `overlap` and sets it to `true`. The the script checks if `FirstBootLogEntry` is greater than `NextBootLogEntry`. If it is, then the program sets `overlap` to `false`. Like the `Write-Debug` statement says, this code is checking to see if part of the log has been overwritten. Then the script sets `currentPos` to the sum of `headerSize` and `FirstBootLogEntry`. Then another variable is initialized, this time an array: `arrExp`. This array is used to store the boot records found and print them at the end of the script. This will be simple to replicate:

{% highlight python linenos %}
overlap = True

# Check if the log is partially overwritten
if first_boot_log_entry > next_boot_log_entry:
    overlap = False
    print('Log partially overwritten due to its circular nature.')

current_pos = header_size + first_boot_log_entry

# Loop over records
boot_offsets = []
{% endhighlight %} 

This Python code is pretty simple and self explanatory. Now we look at a bit more complex code in the PowerShell script.

{% highlight powershell linenos %}
while ($true)
{
    $recordStart = $currentPos

    $TimeStamp = Array2Uint64($bytes[$currentPos..($currentPos+7)])
    $currentPos += 8

    $ApplicationID = ([guid]::new([byte[]]$bytes[$currentPos..($currentPos+15)])).ToString()
    $currentPos += 16

    $EntrySize = Array2Ulong($bytes[$currentPos..($currentPos+3)])
    $currentPos += 4
    $Level = Array2Ulong($bytes[$currentPos..($currentPos+3)])
    $currentPos += 4
    $ApplicationType = Array2Ulong($bytes[$currentPos..($currentPos+3)])
    $currentPos += 4
    $EventCode = Array2Ulong($bytes[$currentPos..($currentPos+3)])
    $currentPos += 4

    Write-Debug ("recordStart: " + ('0x{0:X4}' -f $recordStart))
    Write-Debug ("  Timestamp: " + $TimeStamp)
    Write-Debug ("  ApplicationID: " + $ApplicationID)
    Write-Debug ("  EntrySize: " + $EntrySize)
    Write-Debug ("  Level: " + $eventLevels[[int32]$Level])
    Write-Debug ("  ApplicationType: " + $applicationTypes[[int32]$ApplicationType])
    Write-Debug ("  EventCode: " + $eventCodes[[int32]$EventCode])
{% endhighlight %} 

First, `recordStart` is assigned the value of `currentPos`. Next, the script gets the timestamp of the current record. This data is stored in the file as an unsigned long long datatype. Then, the GUID parsed from the next 16 bytes. Finally, 4 more variables are created and printed. 

{% highlight python linenos %}
while(True):
    # Get the record start offset
    record_start = current_pos
    print('\n#########################################################')
    print('RecordStart: 0x%04x' % record_start)

    f.seek(current_pos)
    timestamp, = struct.unpack('Q', f.read(8))
    print('Timestamp:', timestamp)
    
    # Move to the GUID position
    f.seek(current_pos + 8)
{% endhighlight %}

In Python now, we start the loop then set and print `recordStart`. Next, we use `f.seek(current_pos)` to move to the start of the timestamp data. For the timestamp stored as an unsigned long long, we use `struct.unpack('Q', f.read(8))` to unpack the data. Then we move the position to the start of the GUID. 

**GUID Format**
<div class="grid">
  <div id="cell1" class="cell cell--2">----4 bytes---- Little Endian Unsigned Long</div>
  <div id="cell2" class="cell cell--2">----4 bytes---- Little Endian Unsigned Short</div>
  <div id="cell3" class="cell cell--4">----8 Bytes---- <br/> Big Endian <br/> Unsigned Short</div>
</div>

