---
title: Cellebrite Spring 2021 CTF - Part 2 - Heisenberg - Galaxy Note 10
excerpt: Solutions to 2022 Spring Cellebrite CTF! Part 2! This part looks at the solutions to the questions associated with the image of Heisenberg's Galaxy Note.
categories: [CTF, Cellebrite 2022] 
tags: cellebrite-ctf ctf forensics
author: clark
---

## Heisenberg's Galaxy Note 10 - Android 11

### Question 13 – 10pts

> What package was used by the Mobile App used by Heisenberg to scan/optimize his device? (package name)

The app can be found by simply looking under the `Clean mobile` category in the `Installed Applications` section. 


![Cleaning apps](https://starwarsfan2099.github.io/public/2022-06-07/13.JPG){:.shadow}{:.center}


The solution is `com.samsung.android.lool`. 
{:.success}

### Question 14 – 10pts

> What is the package name used by the Mobile App which Heisenberg looked up license plates/VIN of target vehices?

A simple keyword search for "License Plate" will show you the installed application. 


![License Plate App](https://starwarsfan2099.github.io/public/2022-06-07/14.JPG){:.shadow}{:.center}


The app id and solution is `com.orto.usa`. 
{:.success}

### Question 15 – 10pts

> What app does “zebedee.db” correspond to?

Once again, a simple keyword search for `zebedee.db` shows the application the database is associated with. 


![zebedee App](https://starwarsfan2099.github.io/public/2022-06-07/15.JPG){:.shadow}{:.center}


The app and solution is `Device Health Services`.
{:.success}

### Question 16 – 10pts

> What is the password for mobile data hotspot on Heisenberg’s device that was shared with Beth? (Case Sensitive)

Physical Analyzer does not appear to parse this hotspot data and place it in `Device connectivity` or the `Networking` sections. However, when searching for `Wifi` and looking through the data not used in the `Device connectivity` or the `Networking` sections, a few xml files can be found. One named `WifiConfigStoreSoftAp.xml`. This file stores the solution.


![Hotspot](https://starwarsfan2099.github.io/public/2022-06-07/16.JPG){:.shadow}{:.center}


The hotspot password and solution is `yipz5901`. 
{:.success}

### Question 17 – 10pts

> What is the Bluetooth MAC address, date, and time for the last connection to Bose Sound Touch/CE2D10 (MAC YYYY-MM-DD HH:MM:SS) (24-hr format) Example: aa:bb:cc:dd:ee:ff 2020-04-28 18:29:33

First, looking under the `Device Connectivity` tab does indeed show a "Bose Sound Touch" device. However, it only records the start time instead of the last connection time. It does show us the Mac though: `2c:6b:7d:1d:21:a7`. 


![Devices](https://starwarsfan2099.github.io/public/2022-06-07/17.JPG){:.shadow}{:.center}


Searching for the Mac though doesn't return anything useful. If there are no results parsed be Cellebrite, perhaps the info is in a third party source. Looking through the installed apps, an app called `SmartThings` can be found. 


![Bluetooth app?](https://starwarsfan2099.github.io/public/2022-06-07/17_1.JPG){:.shadow}{:.center}


The package name also gives a clue, being called `com.samsung.android.oneconnect`. Hmmm. Sounds like it could involve Bluetooth. Using the SQLite Wizard, we can look through the app's databases.


![Timestamp](https://starwarsfan2099.github.io/public/2022-06-07/17_2.JPG){:.shadow}{:.center}


Eventually, a database named `QcDb.db` is found. It contains a table named `devices` that includes the Sound Touch Mac address, name, and a timestamp.  

After converting the timestamp and formatting the answer we get the solution: `2c:6b:7d:1d:21:a7 2021-06-27 17:47:41`.
{:.success}

### Question 18 – 10pts

> What is the phone number of the undercover cop who approached Heisenberg? (Format: +1–212–555–1234)

When looking through the chats and conversations, Mr. White really only has one conversation with an unknown individual. All other conversations are with a known contact or spam. 


![Phone number](https://starwarsfan2099.github.io/public/2022-06-07/18.JPG){:.shadow}{:.center}


This number is the correct number, and solution to the challenge - `+1–540–299–3169`. 
{:.success}

### Question 19 – 10pts

>     BONUS Question Select anything to receive 10pts.

Just select anything and enjoy the free points!
{:.success}

### Question 20 – 10pts

> What is the total number of messages deleted (could be partially or not recovered)?

We *should* be able to see the deleted messages in the `Messages` tab or in the `Analyzed Data` sidebar view.


![Deleted](https://starwarsfan2099.github.io/public/2022-06-07/20.JPG){:.shadow}{:.center}


Both views show `3` deleted messages. That was an incorrect solution, and so was `6` if we include the emails. Not sure what the answer here is. 
{:.success}

### Question 21 – 10pts

> Based on retrieved data from the device, the phone operated in West Virginia. True/False?

By looking at the `Device Locations` tab, we can see that the device was operated near Arbuckle, WV. 


![Phone number](https://starwarsfan2099.github.io/public/2022-06-07/21.JPG){:.shadow}{:.center}


The answer is `True`.
{:.success}

### Question 22 – 10pts

> How many native images on the device contain location data?

The `Images` tab in Physical Analyzer allows for filtering via metadata containing location information. 


![Pictures with location info](https://starwarsfan2099.github.io/public/2022-06-07/22.JPG){:.shadow}{:.center}


Looking at the bottom bar, it shows the stats on the specific images. We need to be careful to not look at the `Selected` and the `Deduplication` fields. The answer we are looking for is in the `Items` or `Selected` fields.

 The answer and solution is `57`.
 {:.success}

### Question 23 – 10pts

> What is the IMSI of the device?

This can be found on the Physical Analyzer homepage. 


![IMSI](https://starwarsfan2099.github.io/public/2022-06-07/23.JPG){:.shadow}{:.center}


The solution and IMSI is `310260275793897`. 
{:.success}

### Question 24 – 20pts

> Was the image with the MD5 hash “066858f4b1971b0501b9a06296936a34” hidden by Heisenberg? If Yes, what is the name of the package of the app used to hide the image else answer No. Example: yes+com.apple.wallet

Simply searching for the has reveals several locations the image is stored, and each filepath has the app package name. 


![Hash Photo](https://starwarsfan2099.github.io/public/2022-06-07/24.JPG){:.shadow}{:.center}


The app used to hide the image was `com.flatfish.cal.privacy`. 
{:.success}

### Question 25 – 20pts

> What is the name, username and account number corresponding to the media id “2623237359273252101”.  Was Heisenberg following this account? (Answer Format: Name_Username_AccountNumber_Yes/No) (No Spaces)

Searching for `2623237359273252101` yields no results. However, by doing a more thorough hex search on the actual image, we can find several mentions of the string in an Instagram database. 


![Hex search](https://starwarsfan2099.github.io/public/2022-06-07/25.JPG){:.shadow}{:.center}


All the parts to the solution are in this file. Specifically, the `username`, `full_name`, `id`, and `following` keys. 

Placing these in the properer format for the solution, we get `MarshaMellos_marsha4mellos_44072330861_Yes`!
{:.success}

### Question 26 – 20pts

> What is the Date and Time for the last use of Instagram on Heisenberg’s device? (YYYY-MM-DD HH:MM:SS) (24-hr format) example: 2019-03-22 23:45:12

The timeline in Physical Analyzer doesn't show a specific Instagram usage times. However, filtering in the **Analyzed Data > Databases** section for instagram shows some Instagram databases with `time_in_app` in the name. 


![Instagram](https://starwarsfan2099.github.io/public/2022-06-07/27.JPG){:.shadow}{:.center}


Looking at the intervals table, there is column `end_walltime` that is a timestamp of the last usage. 

Converting the timestamp to the proper format, we get `2021-07-22 19:06:37` and is indeed the correct solution. 
{:.success}

### Question 27 – 20pts

> Find the first six and the last four digits of a burner card that was used by Heisenberg for gas. (FirstSix_LastFour)

By doing a basic search for the keyword `gas`, we can see the user has an app installed titled **GetUpside** for gas discounts. Searching the **Analyzed Data > Databases** again for `gas` or `GetUpside` shows the databases associated with the apps. After poking around them, a table named `class_CreditCard` can be found in the `upside.realm` database. It includes two columns we need, `firstSix` and `lastFour`. 


![GetUpside DB](https://starwarsfan2099.github.io/public/2022-06-07/28.JPG){:.shadow}{:.center}


Now we can get the solution to the challenge! `414720_0834 `. 
{:.success}

### Question 28 – 20pts

> Android Standard (20 points) – Heisenberg intended to have a meeting with the person he was intensely communicating with. Establish the name of the street in which the meeting was about to take place and the exact time of the chat in which the requesting party confirmed the meeting. format: [street name] [time HH:MM:SS UTC] example: Main St. 19:27:21

Once again, Search is our friend. By simply searching for the keyword `meet` we can see one chat where that word is mentioned. 


![Meeting chat](https://starwarsfan2099.github.io/public/2022-06-07/29.JPG){:.shadow}{:.center}


All of the information we need is right there. The solution in the proper format is `washington street 18:44:58`. 
{:.success}

### Question 29 – 20pts

> This meeting was a setup in which a police agent arrested Heisenberg. Find evidence that was generated during the estimated time of the meeting in which you can witness (see and hear) Heisenberg’s arrest.  What is the location in which this evidence was created? Note: There are only two instances of similar evidence that have geographical locations. (format: Lat,Long example: 33.333,-77.7777)

Well, we know the data of the meeting from question 29. The question says *see and hear*, so this must be a video! Filtering videos by the date of the meeting, we can find the meeting video!


![Meeting video](https://starwarsfan2099.github.io/public/2022-06-07/30.JPG){:.shadow}{:.center}


Physical analyzer fails to show any coordinates for where the video was taken, even with **Carve Locations** enabled during processing. However, by simply exporting the video and using exiftool, we can see the coordinates are `37.2249,-80.4159`.
{:.success}