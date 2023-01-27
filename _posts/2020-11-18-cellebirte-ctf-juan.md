---
title: Cellebrite Fall 2020 CTF - Part 3 - Juan Mortyme
excerpt: Solutions to the 1st ever Cellebrite CTF! Part 3! This part looks at the solutions to the questions associated with the image of Juan Mortyme's iPhone. 
categories: [CTF, Cellebrite 2020]
tags: cellebrite-ctf ctf forensics
author: rms
---

## Juan Mortyme's iPhone X (A1901)

### Phone Information - 20 points

> What is the owner’s mobile phone number (10 or 11 digits only)?

This first question for this challenge asks us to simply determine the phone number. The phone number is automatically parsed and shown on the `Extraction Summary` page.


![Phone number](https://starwarsfan2099.github.io/public/2020-11-18/juan_1.JPG){:.shadow}{:.center}{: width="586" height="24" }


The phone number is `+16095299858`.
{:.success}

### Location Address - 10 points

> What is the owner’s home street name (just the street name, NO home address number, NO city, NO state, just street name.

The `Device Locations` tab has a search bar that allows us to search locations, titles, addresses, etc. Searching for "*home*", Cellebrite returns several results. One of the rows returned has the description "home".  It is from the Waze App user database. 


![Home](https://starwarsfan2099.github.io/public/2020-11-18/juan_2.JPG){:.shadow}{:.center}{: width="383" height="479" }


The street listed in the address is `NE 44th Ct` and also the answer to the challenge.
{:.success}

### Activation - 20 points

> When was the phone first activated? (after a wipe) format: MM-DD-YYYY

The `activation_records` file's timestamps record the last activation date. 


![Activation](https://starwarsfan2099.github.io/public/2020-11-18/juan_3.JPG){:.shadow}{:.center}{: width="363" height="287" }


Putting the file in the format the answer requires, the solution is found to be `04-23-2020`. 
{:.success}

### Vehicle - 20 points

> Name a vehicle make of which the device was connected to?

Using the `Device Connectivity` tab, we can view a list of all connected devices. None of the device names or descriptions include a reference to a car. Searching different device names is up next. When searching "MY LEAF", an interesting result is returned. 


![MY LEAF](https://starwarsfan2099.github.io/public/2020-11-18/juan_4.JPG){:.shadow}{:.center}{: width="274" height="111" }


Google searching "MY LEAF" returns a link to a Nissan forum. The forum post mentions a 2015 Nissan Leaf SV. 


![Forum](https://starwarsfan2099.github.io/public/2020-11-18/juan_5.JPG){:.shadow}{:.center}{: width="958" height="126" }


Entering `Nissan` shows this is the answer to the challenge. 
{:.success}

### Location Details - 20 points

> In which city is the favorite Starbucks located?

Back to the `Device Locations` tab we go. Searching for Starbucks yields serval results, but one has the tag "Favorite stores" associated with it. 


![Starbucks](https://starwarsfan2099.github.io/public/2020-11-18/juan_6.JPG){:.shadow}{:.center}{: width="362" height="417" }



![Starbucks favorite](https://starwarsfan2099.github.io/public/2020-11-18/juan_7.JPG){:.shadow}{:.center}{: width="355" height="88" }


The GPS coordinates listed are `39.286895, -76.612876`. Pooping this into Google maps reveals it is located in Baltimore. 


![Starbucks GPS](https://starwarsfan2099.github.io/public/2020-11-18/juan_8.JPG){:.shadow}{:.center}{: width="401" height="298" }


Entering `Baltimore` shows that it is indeed the solution to the challenge. 
{:.success}

### Daytrip - 20 points

> What did I pick up from Montana?

[Gerbinator](https://github.com/Gerbinator) once again came in clutch on this question. There isn't one specific artifact that pointed to it. There are multiple pictures of boats, mentions of boats in texts, and browser searches for boats. 

[Gerbinator](https://github.com/Gerbinator) correctly guessed that it was a `boat` and it was the correct answer.
{:.success}

### Printing - 20 points

> On a document printed from this device, what is the 2nd word on the 3rd line?

Opening the `Documents` tab from the `Extraction Summary` shows several documents. Filtering them for the keyword print reveals one document named `1.pdf` and is located at `/root/private/var/mobile/Library/com.apple.printd/1.pdf`. Apparently, iOS devices copy printed documents to this path. 


![Document path](https://starwarsfan2099.github.io/public/2020-11-18/juan_9.JPG){:.shadow}{:.center}{: width="333" height="269" }


The document found there:


![Document](https://starwarsfan2099.github.io/public/2020-11-18/juan_10.JPG){:.shadow}{:.center}{: width="205" height="166" }


The second word on the third line of the document is `delete`. This is the solution. 
{:.success}

### Photo analysis - 20 points

> Find the following photo: [snip] Analyze and determine the offset from UTC, enter numerics only? (without UTC and no +/- for example: 2)

Luckily, we thought we had seen this particular image before. So we checked attachments in conversations with the others. In a WhatsApp conversation with Rene that began on `4/30/2020`, the image was sent to her from Juan.  


![Picture](https://starwarsfan2099.github.io/public/2020-11-18/juan_11.JPG){:.shadow}{:.center}{: width="332" height="180" }


The UTC time offset is already provided for us by Cellebrite right below the image. The solution is `7`. 
{:.success}

### (Audio) Recording Location - 50 points

> There are multiple (Audio) Recordings, created by the user - on the device, a few of them are associated with different airports locations. Name the ICAO code of either one of the airports. (format has 4 characters for example CYYZ for Toronto Pearson airport)

Hmm. Recordings can be found under `Analyzed Data` > `Memos` > `Recordings`. Though, none of the recordings have any mention of a location in them or any metadata containing a location. However, when checking the directory where the recordings are stored, in `/private/var/mobile/Media/Recordings/`, a database is present there - `CloudRecordings.db`. Searching it for the keyword "*airport*" takes us to the `ZCLOUDRECORDING` table. Here, the airport name is present!


![Audio Database](https://starwarsfan2099.github.io/public/2020-11-18/juan_12.JPG){:.shadow}{:.center}{: width="809" height="234" }


Looking at the [Wikipedia entry for O'Hare International Airport](https://www.wikiwand.com/en/O%27Hare_International_Airport), we can see that it's ICAO code is `KORD` and is indeed one of the solutions to the challenge. 
{:.success}

### IP Address - 50 points

> What is the IP Address the device was associated with - while connected to the WiFi network on August 14, 2020? (Standard IP Address format for example: 10.1.123.11)

IP assignments can be found in DHCP leases. These are stored at `/private/var/db/dhcpclient/leases/` in iOS devices. Checking the folder on this device, thankfully there is only one lease, so easy-peasey. We can open the lease in the Plist viewer. 


![DHCP lease](https://starwarsfan2099.github.io/public/2020-11-18/juan_13.JPG){:.shadow}{:.center}{: width="536" height="329" }


The IP address is `192.168.1.98 ` and the solution to this challenge. 
{:.success}

### Financial Situation - 100 points

> In a financial app there is still a $ balance - what is that amount? (full amount with pennies for example: 12.34)

The first plan of attack was the CashApp and CoinBase databases. After quite a lot of time wasted on those, another method was tried. Thinking about how else the phone could have the amount, we considered images, which led us to the splash screens that iOS takes when an app is opened or switched via multitasking. Splash screens are stored as a `.ktx` filetype. Filtering images by that type still results in hundreds of images. Searching for the text `com.squareup.cash` though, pulls up three images, one of which had the monetary amount.  


![CashApp Splashscreen](https://starwarsfan2099.github.io/public/2020-11-18/juan_14.JPG){:.shadow}{:.center}{: width="383" height="800" }


The solution to the challenge is `2.99`.
{:.success}