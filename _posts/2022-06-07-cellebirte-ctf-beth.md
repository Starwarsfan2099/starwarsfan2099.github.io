---
title: Cellebrite Spring 2021 CTF - Part 3 - Beth - iPhone X
excerpt: Solutions to 2022 Spring Cellebrite CTF! Part 3! This part looks at the solutions to the questions associated with the image of Beth's iPhone. 
tags: cellebrite-ctf ctf forensics
author: rms
---

## Beth's iPhone X - iOS 14.6

### Question 31 – 10pts

> Beth wanted to meet her partner in an isolated place in the mountains to close a deal. Which email address did she send to?

A simple keyword search for mountains shows three results, with one being an email. 

{:refdef: style="text-align: center;"}
![Mountains Search](https://starwarsfan2099.github.io/public/2022-06-05/31.JPG){:.shadow}
{: refdef}

The email was to `livingstonhank11@gmail.com` and is the solution to this question. 

### Question 32 – 10pts

> Where was Beth on June 29th 2021 when she made a call to Marsha? (Provide only the city in your answer)

For this question, we need to load up the timeline created by Physical Analyzer and looked at June 29th, 2021. Here, we can see the outgoing phone call to Marsha and  look for any other artifacts that could contain location data.

{:refdef: style="text-align: center;"}
![Phone Call](https://starwarsfan2099.github.io/public/2022-06-05/32.JPG){:.shadow}
{: refdef}

See it right there? A location artifact around 20 minutes before the call! 

{:refdef: style="text-align: center;"}
![Location](https://starwarsfan2099.github.io/public/2022-06-05/32_2.JPG){:.shadow}
{: refdef}

Popping the location coordinates into Google Earth reveals she was in `New York` when she made the call to Marsha. 

### Question 33 – 10pts

> Two of the suspects use the same app to facilitate money transfers without handling fees. Who are they? Provide first names separated by a comma: [AAA],[BBB]

This one is requires analysis of the other images provided as well as this image. It turns out, the only finance app shared between two people was `PassBook` - shared between Beth and Marsha. 

{:refdef: style="text-align: center;"}
![PassBook](https://starwarsfan2099.github.io/public/2022-06-05/33.JPG){:.shadow}
{: refdef}

Since this is a default iOS, I was unsure but decided to use an attempt to answer the challenge, and indeed the answer was `Beth,Marsha`. 

### Question 34 – 10pts

> What is the version of the extraction container format in the provided evidence file?

The extracted container format can be found inside the zip archive that Physical Analyzer processes. Inside the zip file is the phone filesystem, a log file, and a version file containing the container format version. 

{:refdef: style="text-align: center;"}
![Container Version](https://starwarsfan2099.github.io/public/2022-06-05/34.JPG){:.shadow}
{: refdef}

The solution is `CLBX-0.3.1`. 

### Question 36 – 10pts

> Who was Beth supposed to meet at the Vienna Inn?

Another simple keyword search for `Vienna Inn` provides only one result. 

{:refdef: style="text-align: center;"}
![Vienna Inn](https://starwarsfan2099.github.io/public/2022-06-05/36.JPG){:.shadow}
{: refdef}

The solution is `Heisenberg White`. 

### Question 37 – 10pts

> What was Beth's furthest walking distance?

To solve this one, we need to use the `Activity Sensor Data` pane that Cellebrite Provides. 

{:refdef: style="text-align: center;"}
![Sensor Data](https://starwarsfan2099.github.io/public/2022-06-05/37.JPG){:.shadow}
{: refdef}

In this window, we can sort by the `Distance Traveled` column to see the longest distance. 

{:refdef: style="text-align: center;"}
![Longest Distance](https://starwarsfan2099.github.io/public/2022-06-05/37_2.JPG){:.shadow}
{: refdef}

The solution is `2482.28`. 

### Question 38 – 10pts

> What is the IMEI number of the device?

Another super-easy one, displayed right on the Physical Analyzer homepage.

{:refdef: style="text-align: center;"}
![IMEI](https://starwarsfan2099.github.io/public/2022-06-05/38.JPG){:.shadow}
{: refdef}

The solution is `359405082912450`. 

### Question 39 – 10pts

> What is the Apple ID associated with the device?

This answer is also displayed on the homepage.

{:refdef: style="text-align: center;"}
![Apple ID](https://starwarsfan2099.github.io/public/2022-06-05/39.JPG){:.shadow}
{: refdef}

The solution is `tornadobeth@gmail.com`. 

### Question 42 – 20pts

> What is the Exclusive Chip Identification (ECID) of the mobile device?

A method for solving this challenge can be found on the [ECID iPhone Wiki page](https://www.theiphonewiki.com/wiki/ECID). The page list several methods for recovering the ECID from a running device or filesystem. Within the filesystem, the ECID can be recovered from the `apticket.der` file. The location of this file can be found at `/System/Library/Caches/apticket.der`. By going to this location in Physical Analyzer, we can see the location of the actual file we want.

{:refdef: style="text-align: center;"}
![apticket location](https://starwarsfan2099.github.io/public/2022-06-05/42.JPG){:.shadow}
{: refdef}

And opening up this file, we can search for and see the ECID.

{:refdef: style="text-align: center;"}
![ECID](https://starwarsfan2099.github.io/public/2022-06-05/42_2.JPG){:.shadow}
{: refdef}

The ECID and solution is `1242319429238830`. 

### Question 43 – 20pts

> What was the search query in the open tab of the DuckDuckGo Privacy Browser?

Hmmmm. The first place we want to look is the for any cache files present related to the DuckDuckGo browser. Using the SQLite browser, we can see there is a `Cache.db` file that contains a few tables that store some queries and timestamps, but no easy way to connect the two to get the most recent or currently open tab query. 

{:refdef: style="text-align: center;"}
![Cache.db](https://starwarsfan2099.github.io/public/2022-06-05/43.JPG){:.shadow}
{: refdef}

The app folder can be found at `Apple_iPhone X (A1901).zip/root/private/var/mobile/Containers/Data/Application/1CFB7BE5-990B-4971-908A-10C2EC94080B`. By going through all the files here and searching keywords, a property list file called `com.duckduckgo.mobile.ios.plist` can be found containing the key `com.duckduckgo.opentabs`. 

{:refdef: style="text-align: center;"}
![Open Tab](https://starwarsfan2099.github.io/public/2022-06-05/43_2.JPG){:.shadow}
{: refdef}

Here we see an array containing info about the currently open tabs. The url for the open tab is `https://duckduckgo.com/?q=daphne+bridgerton+actress&t=ddg_ios&atb=v266-3mc&ko=-1&iax=images&ia=images`, making the search query and solution for the challenge `daphne bridgerton actress`. 