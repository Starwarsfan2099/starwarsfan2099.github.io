---
title: Cellebrite Fall 2020 CTF - Part 4 - Ruth Langmore
excerpt: Solutions to the 1st ever Cellebrite CTF! Part 4! This part looks at the solutions to the questions associated with the image of Ruth Langmore's infamous iPhone X. 
categories: [CTF, Cellebrite 2020]
tags: cellebrite-ctf ctf forensics
author: rms
---

## Ruth Langmore's iPhone X (D221AP)

### Application Analysis - 10 points

> On what date did Ruth want to be reminded to “Move the product”? (answer MM-DD-YYYY)

Cellebrite provides parsed reminder information under `Analyzed Data` > `Calander` > `Reminders`. In this table, a reminder with the title "Move the product can be seen". 


![Reminder](https://starwarsfan2099.github.io/public/2020-11-19/ruth_1.JPG){:.shadow}{:.center}


The date the reminder is set for in the format required by the solution is `08-14-2020`. 
{:.success}

### Browser History - 10 points

> Where did Ruth look up weather forecasts for? (answer must include city and state in this format - Washington, DC)

The `Web History` tab can reveal the solution to this question. Searching for the term "*weather*" reveals several AccuWeather website visits, with the city and state visible.


![Weather search](https://starwarsfan2099.github.io/public/2020-11-19/ruth_2.JPG){:.shadow}{:.center}


The solution to this challenge is `Carolina Beach, NC`. 
{:.success}

### Communications - 10 points

> Who is the owner/creator of the group named “OG Crew” across the devices?

Searching the image for "*OG Crew*" returns the Telegram conversation. 


![Telegram conversation](https://starwarsfan2099.github.io/public/2020-11-19/ruth_3.JPG){:.shadow}{:.center}


The initial message includes a PeerId listed as `953301191`. Checking the details of the conversation, we can see user PeerIds.


![Tony M PeerId](https://starwarsfan2099.github.io/public/2020-11-19/ruth_4.JPG){:.shadow}{:.center}


The PeerId is listed as Tony M's id. The fact he made the first message supports him creating the group, as well as changing the group photo in the second message. 

Inputting `Tony M` reveals it is indeed the correct answer.
{:.success}

### Device Identification - 20 points

> Which iOS version was running on the device at the time of acquisition? (answer with just the number - i.e. 12.3)

The currently running iOS version can simply be found in the plist file `System/Library/CoreServices/systemversion.plist`. 


![iOS Version](https://starwarsfan2099.github.io/public/2020-11-19/ruth_5.JPG){:.shadow}{:.center}


This plist clearly shows the iPhone is on iOS version `13.6` and is the correct answer to the challenge. 
{:.success}

### Application Analysis - 20 points

> What is Ruth’s user_id on TikTok? (answer is the string of numbers, not the user_name).

The user_id can be found on the in the TikTok databases, but it can also be parsed with AppGenie as well. The database that TikTok contacts are found in is located in `private/var/mobile/Containers/Data/Application/314C0D76-AD79-43D9-93F6-5369A847BEE5/Documents/AwemeIM.db`, in the `AwemeContactsV3` table. Or, AppGenie can parse it us. 


![TikTok user_id](https://starwarsfan2099.github.io/public/2020-11-19/ruth_6.JPG){:.shadow}{:.center}


No matter which method is used, Ruth's user_id is returned as `6854514343108871173` and is the solution.
{:.success}

### Password Recovery - 20 points

> What is the password that can be used to access the link recovered from the locked notes? (answer is caSE SenSITive).

This question actually took a while to solve. It needs to be solved after solving the [Database Analysis question](https://starwarsfan2099.github.io/2020/11/19/cellebirte-ctf-ruth.html#database-analysis---50-points) and getting the DropBox link. Ultimately, there was no real system used to find the password. A password was found while going through other conversations in an attempt to solve another challenge. The password was found in a TikTok chat that began on 8/13/2020. 


![Dropbox password](https://starwarsfan2099.github.io/public/2020-11-19/ruth_7.JPG){:.shadow}{:.center}


Stumbling across the passowrd `Dr3@mT3@m11`, we tried using it to unlock the link and it surprisingly worked! And is the solution to this challenge. The unlocked DropBox has one file stored - `Ruth.z7`.


![Dropbox](https://starwarsfan2099.github.io/public/2020-11-19/ruth_11.JPG){:.shadow}{:.center}


Decompressing the file reveals an iPhone image of Ruth's phone before it was reset! This is used to answer several of the challenges.
{:.success}

### Device Status - 20 points

> When was Ruth’s iPhone last wiped? Provide the date in the following format MM-DD-YYYY)

The date of the last wipe can be found using the file `/private/var/root/.obliterated`. The timestamp on that file is the last time the device was restored, reset, or erased. 


![Obliterated](https://starwarsfan2099.github.io/public/2020-11-19/ruth_8.JPG){:.shadow}{:.center}


The timestamps on the file are listed as `7/27/2020`, and that is the correct solution to this challenge. 
{:.success}

### PList Analysis - 20 points

> When was the WiFi for “Birchrunville_cafe-Guest” first connected (added) to Ruth’s iPhone? The answer must be provide in localtime for the device. (UTC WILL NOT BE ACCEPTED). Answer must be in the following format MM-DD-YYYY HH:MM:SS (i.e. 12-18-2019 23:52:23)

This question and the next question need to be answered using the second image of Ruth's phone obtained in the [Password Recovery question](https://starwarsfan2099.github.io/2020/11/19/cellebirte-ctf-ruth.html#password-recovery---20-points). The answer to this question can be found by going to the `Wireless Networks` tab and sorting by the SSIDs. 


![WiFi](https://starwarsfan2099.github.io/public/2020-11-19/ruth_12.JPG){:.shadow}{:.center}


The time it was first connected to is the timestamp shown. In the format required by the question, the solution is `07-09-2020`. 
{:.success}

### Application Usage - 20 points

> How much time did Ruth spend on TikTok on 07-25-2020? (Answer must be in this format 00:05:27)

This question can be easily solved by looking at the timeline. First, filter by the data in question, 7/25/2020. Then search for the TikTok identifier `com.zhiliaoapp.musically`. This returns 7 rows, 2 of which are application usage logs. 


![Application usage](https://starwarsfan2099.github.io/public/2020-11-19/ruth_13.JPG){:.shadow}{:.center}


Subtracting the times returned, `5:53:47` - `5:51:23` = `00:02:24`. The correct solution is `00:02:24`. 
{:.success}

### Application Usage - 20 points

> How did Ruth listen to the podcast titled “Episode 4: The Importance of Test Data” on this device? (Answer must be just the application name i.e. spotify)

The first place to check is the default Podcasts app. Information on Podcasts is not found in the Podcast app or it's databases, it is actually found in `/private/var/mobile/Media/iTunes_Control/iTunes/MediaLibrary.sqlitedb`, the default media library database. After searching the different tables for the keywords "*Episode 4*", it can finally be found in the `item_extra` table.


![Podcast in database](https://starwarsfan2099.github.io/public/2020-11-19/ruth_9.JPG){:.shadow}{:.center}


This confirms the default iOS Podcast app was used. The question has an example application name in all lower case. So entering `podcast` is the correct answer. 
{:.success}

### Application Usage - 20 points

> Ruth listened to a podcast titled “Episode 4: The Importance of Test Data” on this device. Once you determine how she listened to it, what is the item_pid for this podcast?

Easy enough! This answer is found in the exact same place we used to answer the last question.


![Podcast in database](https://starwarsfan2099.github.io/public/2020-11-19/ruth_9.JPG){:.shadow}{:.center}


The `item_pid` is the first column from the left. `239332200929536034` is the solution to this challenge. 
{:.success}

### Database Analysis - 50 points

> What is the link that was found in a locked note? (Hint: it is a good idea to use this link as it’s a hidden flag and it’s safe!)

The link can be found after unlcoking the locked note, which is described in the [Application Analysis_Notes question](https://starwarsfan2099.github.io/2020/11/19/cellebirte-ctf-ruth.html#application-analysis_notes---100-points).


![Unlocked notes](https://starwarsfan2099.github.io/public/2020-11-19/ruth_10.JPG){:.shadow}{:.center}


The link from the note and solution to the challenge is `https://bit.ly/3arhLSK`. The shortened link takes us to a password protected DropBox link.
{:.success} 

### Financial Information - 50 points

> What is the routing number used by Ruth to make and receive payments for potentially illegal transactions?

[Gerbinator](https://github.com/Gerbinator) again came in clutch on this question. After too long searching anywhere we could think on Ruth's phone, [Gerbinator](https://github.com/Gerbinator) had the idea to check the other images provided. They came across the same SplashScreen image from [Juan's Financial Situation question](https://starwarsfan2099.github.io/2020/11/18/cellebirte-ctf-juan-copy.html#financial-situation---100-points). That image had a routing number in the image.


![CashApp Splashscreen](https://starwarsfan2099.github.io/public/2020-11-18/juan_14.JPG){:.shadow}{:.center}


Attempting that routing number, especially since it's the only one we could find that it could possibly be, it turns out that is the correct answer - `041215663`!!
{:.success}

### Application Analysis_Notes - 100 points

> What is the password to unlock the Notes on Ruth’s device? (case sensitive - as all passwords should be!) You won`t find the answer, but can draw clues to it. Google could help once you find the correct hint.

A bit of research led to the discovery of [this Perl script](https://drive.google.com/file/d/1JleFjz3Nm6fg380-LpUYF0GJ2UrMry5d/view) that can be used to extract the hash of any locked notes file from the `NoteStore.sqlite`. The hash can than be used in a dictionary + mask attack using Hashcat. Hashcat supports iOS note hash cracking with the `-m 16200` mode. All of the passwords we have seen up to this point have used l33tsp3ak. Using a l33tsp3ak mask in combination with the Rockyou wordlist reveals that the password is `w3ndy$`. Reloading Ruth's image and inputting that as the locked note password reveals the contents of the note and is the answer to this challenge[.](https://www.youtube.com/watch?v=dGeEuyG_DIc)