---
title: Windows `bootstat.dat` Forensic Parser
excerpt: Quick post to go over a Python parser for the Windows binary boot log. 
tags: programming forensics
author: rms
published: true
---

## Grzegorz Tworek's PSBits

{:refdef: style="text-align: center;"}
![Tweet](https://starwarsfan2099.github.io/public/2022-09-12/tweet.JPG){:.shadow}
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

### Converting the functions

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

### Some constants

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

`eventLevels`, `eventCodes`, and `applicationTypes` are defined along with the header size we already defined in the Python script. We can easily define these in the Python script using dictionaries. After further testing the finished script, more types were added to the `applicationTypes`. These can be found [here](https://www.omnisecu.com/windows-2008/introduction-to-windows-2008-server/boot-configuration-data-bcd-objects.php).

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

applicationTypes = {1:'BCD_APPLICATION_TYPE_FIRMWARE_BOOT_MANAGER',
                    2:'BCD_APPLICATION_TYPE_WINDOWS_BOOT_MANAGER',
                    3:'BCD_APPLICATION_TYPE_WINDOWS_BOOT_LOADER',
                    4:'BCD_APPLICATION_TYPE_WINDOWS_RESUME_APPLICATION',
                    5:'BCD_APPLICATION_TYPE_WINDOWS_MEMORY_TESTER'}
{% endhighlight %} 

### Unpacking data

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

### Loop over records

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

### Unpack GUID

In Python now, we start the loop then set and print `recordStart`. Next, we use `f.seek(current_pos)` to move to the start of the timestamp data. For the timestamp stored as an unsigned long long, we use `struct.unpack('Q', f.read(8))` to unpack the data. Then we move the position to the start of the GUID. The PowerShell script used `([guid]::new([byte[]]$bytes[$currentPos..($currentPos+15)])).ToString()` to decode the GUID from the file. This uses the `::` operator to create a new GUID from the .NET framework class `guid`. We don't have this luxury in Python sadly. Using `struct.unpack('<L', f.read(4))` for all 16 bytes results in a partially correct GUID. With some trial and error though, we can get the correct unpacking format for the GUID. It looks like this:

**GUID Format**
<div class="grid">
  <div id="cell1" class="cell cell--2">----4 bytes---- Little Endian Unsigned Long</div>
  <div id="cell2" class="cell cell--2">----4 bytes---- Little Endian Unsigned Short</div>
  <div id="cell3" class="cell cell--4">----8 Bytes---- <br/> Big Endian <br/> Unsigned Short</div>
</div>

A Pythonic way of writing it looks something like this:

{% highlight python linenos %}
guid_hex = '%0.2X' % struct.unpack('<L', f.read(4))
    for i in range(0, 2):
        guid_hex += '%0.2X' % struct.unpack('<H', f.read(2))
    for i in range(0, 4):
        guid_hex += '%0.2X' % struct.unpack('>H', f.read(2))
{% endhighlight %}

Then we can use the [uuid](https://docs.python.org/3/library/uuid.html) Python module to format `guid_hex` properly. The we update `current_pos`, unpack, and print out the data we've unpacked.

{% highlight python linenos %}
    # Format the GUID
    guid = uuid.UUID(hex=guid_hex.strip())
    print('GUID: ', guid)
    current_pos += 16

    # Unpack some more data
    entry_size, = struct.unpack('<L', f.read(4))
    level, = struct.unpack('<L', f.read(4))
    app_type, = struct.unpack('<L', f.read(4))
    event_code, = struct.unpack('<L', f.read(4))
    current_pos += 16

    print('EventCode: %s' % eventCodes[event_code])
    print('Level: %s' % eventLevels[level])
    print('ApplicationType: %s' % applicationTypes[app_type])
    print('EntrySize: %s' % entry_size)
{% endhighlight %}

Now lets look at some more PowerShell.

{% highlight powershell linenos %}
f (($ApplicationType -eq 3) -and ($EventCode -eq 1))
    {
        $BootDateTime = (TimeFields2String($bytes[$currentPos..($currentPos+15)]))
        $LastBootId = (Array2Ulong($bytes[($currentPos+24)..($currentPos+27)]))
        #no need to increase currentPos, as it is overwritten anyway soon

        $row = New-Object psobject
        $row | Add-Member -Name Offset -MemberType NoteProperty -Value ('0x{0:X4}' -f $recordStart)
        $row | Add-Member -Name DateTime -MemberType NoteProperty -Value ($BootDateTime)
        $row | Add-Member -Name LastBootId -MemberType NoteProperty -Value ($LastBootId)
        $row | Add-Member -Name TimeStamp -MemberType NoteProperty -Value ($TimeStamp.ToString())
        $arrExp += $row
        
        Write-Debug ("    BOOT ENTRY FOUND")
        Write-Debug ("    DateTime: " + $BootDateTime)
        Write-Debug ("    LastBootId: " + $LastBootId)
    }
{% endhighlight %}

This is checking for a boot entry. If the application type is `3` and the event code is `1`, there is some boot entry data to parse. We can parse the boot time as well as the boot ID. The PowerShell script creates a `row` variable and some of the data to to it. The, it is appended to `arrExp` for display at the end of the script. After that, it prints the boot info it just parsed. Easy enough to do in Python. 

{% highlight python linenos %}
    # Look for a boot entry id and time
    if (app_type == 3) and (event_code == 1):
        boot_date_time = f.read(16)
        time = format_time(boot_date_time)
        f.seek(f.tell()+8)
        last_boot_id, = struct.unpack('I', f.read(4))

        print('Boot entry found:')
        print('\tDateTime: ', time)
        print('\tLastBootID: ', last_boot_id)
        boot_offsets.append([record_start, time, last_boot_id, timestamp])
{% endhighlight %}

We check `app_type` and `event_code`, then parse the boot time and pass it to the `format_time()` function we created earlier. Next, we use `f.seek(f.tell()+8)` to move to the boot id section and read unpack it with `struct.unpack('I', f.read(4))`. Then we print the data, and append it as well as a few more variables to `boot_offsets` to display at the end of the script. 

{% highlight powershell linenos %}
$currentPos = $recordStart + $EntrySize

    if ($overlap -and ($currentPos -ge ($NextBootLogEntry + $headerSize)))
    {
        break
    }

    if (($currentPos + 28) -gt ($BootLogSize + $headerSize)) #next entry wouldnt fit
    {
        $currentPos = $headerSize + $BootLogStart
        $overlap = $true
    }

    $nextEntrySize = Array2Ulong($bytes[($currentPos+24)..($currentPos+27)])

    if ($nextEntrySize -eq 0) #next record is empty
    {
        $currentPos = $headerSize + $BootLogStart
        $overlap = $true
    }
}
{% endhighlight %}

Almost done. First, the PowerShell script checks if `overlap` is true and then if the current file position is greater then the next entry + the header. This indicates there are no more records to be read, and we need to exit. Next, there is a check to see if the next entry doesn't fit. If it's fine, the next entry it read into `nextEntrySize`. If `nextEntrySize` is `0`, then the record is empty and `overlap` is set to true. This is also easy to convert to Python:

{% highlight python linenos %}
# No more records
    if overlap: 
        if current_pos >= (next_boot_log_entry + header_size):
            break

    # Check if the next entry doesn't fit
    if (current_pos + 28) > (boot_log_size + header_size):
        current_pos = header_size + boot_log_start
        overlap = True

    next_entry_size, = struct.unpack('I', f.read(4))

    # Check if the next record is empty
    if next_entry_size == 0:
        current_pos = header_size + boot_log_start
        overlap = True
{% endhighlight %}

And finally, the PowerShell script prints the array of boot entries and the script ends. 

{% highlight powershell linenos %}
# Let's display the result
if (Test-Path Variable:PSise)
{
    $arrExp | Out-GridView
}
else
{
    $arrExp | Format-Table
}
{% endhighlight %}

And we do the same in the Python script:

{% highlight python linenos %}
print('\nOffset DateTime            LastBootId TimeStamp')
print('------ --------            ---------- ---------')
for record in boot_offsets:
    print('0x%04x %s          %d %d' % (record[0], record[1], record[2], record[3]))
{% endhighlight %}

And done!

### Full Python Script

The script can be found [here in this repo](https://github.com/Starwarsfan2099/Parse-Windows-Boot-Log) or below.

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

applicationTypes = {1:'BCD_APPLICATION_TYPE_FIRMWARE_BOOT_MANAGER',
                    2:'BCD_APPLICATION_TYPE_WINDOWS_BOOT_MANAGER',
                    3:'BCD_APPLICATION_TYPE_WINDOWS_BOOT_LOADER',
                    4:'BCD_APPLICATION_TYPE_WINDOWS_RESUME_APPLICATION',
                    5:'BCD_APPLICATION_TYPE_WINDOWS_MEMORY_TESTER'}

# Format time into a human readable string
def format_time(b):
    return '%s-%02d-%02d %02d:%02d:%02d' % (b[1]*256+b[0], b[2], b[4], b[6], b[8], b[10])

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

overlap = True

# Check if the log is partially overwritten
if first_boot_log_entry > next_boot_log_entry:
    overlap = False
    print('Log partially overwritten due to its circular nature.')

current_pos = header_size + first_boot_log_entry

# Loop over records
boot_offsets = []
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

    # Decode GUID:
    #   [----4 bytes----|----4 bytes-----|----------8 bytes------------]
    #   +--------------------------------------------------------------+
    #   | little-endian | little-endian  |         big-endian          |
    #   | unsigned long | unsigned short |       unsigned short        |
    #   +--------------------------------------------------------------+

    guid_hex = '%0.2X' % struct.unpack('<L', f.read(4))
    for i in range(0, 2):
        guid_hex += '%0.2X' % struct.unpack('<H', f.read(2))
    for i in range(0, 4):
        guid_hex += '%0.2X' % struct.unpack('>H', f.read(2))

    # Format the GUID
    guid = uuid.UUID(hex=guid_hex.strip())
    print('GUID: ', guid)
    current_pos += 16

    # Unpack some more data
    entry_size, = struct.unpack('<L', f.read(4))
    level, = struct.unpack('<L', f.read(4))
    app_type, = struct.unpack('<L', f.read(4))
    event_code, = struct.unpack('<L', f.read(4))
    current_pos += 16

    print('EventCode: %s' % eventCodes[event_code])
    print('Level: %s' % eventLevels[level])
    print('ApplicationType: %s' % applicationTypes[app_type])
    print('EntrySize: %s' % entry_size)

    # Look for a boot entry id and time
    if (app_type == 3) and (event_code == 1):
        boot_date_time = f.read(16)
        time = format_time(boot_date_time)
        f.seek(f.tell()+8)
        last_boot_id, = struct.unpack('I', f.read(4))

        print('Boot entry found:')
        print('\tDateTime: ', time)
        print('\tLastBootID: ', last_boot_id)
        boot_offsets.append([record_start, time, last_boot_id, timestamp])

    current_pos = record_start + entry_size

    # No more records
    if overlap: 
        if current_pos >= (next_boot_log_entry + header_size):
            break

    # Check if the next entry doesn't fit
    if (current_pos + 28) > (boot_log_size + header_size):
        current_pos = header_size + boot_log_start
        overlap = True

    next_entry_size, = struct.unpack('I', f.read(4))

    # Check if the next record is empty
    if next_entry_size == 0:
        current_pos = header_size + boot_log_start
        overlap = True

print('\nOffset DateTime            LastBootId TimeStamp')
print('------ --------            ---------- ---------')
for record in boot_offsets:
    print('0x%04x %s          %d %d' % (record[0], record[1], record[2], record[3]))
{% endhighlight %}
