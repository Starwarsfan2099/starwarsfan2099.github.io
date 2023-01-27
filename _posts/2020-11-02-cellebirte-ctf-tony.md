---
title: Cellebrite Fall 2020 CTF - Part 1 - Tony Mederos
excerpt: Solutions to the 1st ever Cellebrite CTF! In part 1, we look at the answers to the Tony Mederos image provided.
categories: [CTF, Cellebrite 2020]
tags: cellebrite-ctf ctf forensics
author: clark
---

## Introduction

On October 18th, 2020, Cellebrite announced on [their blog](https://www.cellebrite.com/en/blog/join-the-first-cellebrite-capture-the-flag-ctf-event/) that they were hosting their own capture the flag event. The event began on the October 26th and ended at midnight on the 29th. The CTF was hosted on [cellebrite.ctfd.io](https://cellebrite.ctfd.io/). Four forensic phone images were provided for analysis and solving the event's challenges. The images could be downloaded from the following links.

[https://d17k3c8pvtyk2s.cloudfront.net/CTF_Apple_iPhone_X_Juan_Mortyme_parts.7z.001](https://d17k3c8pvtyk2s.cloudfront.net/CTF_Apple_iPhone_X_Juan_Mortyme_parts.7z.001)
[https://d17k3c8pvtyk2s.cloudfront.net/CTF_Apple_iPhone_X_Juan_Mortyme_parts.7z.002](https://d17k3c8pvtyk2s.cloudfront.net/CTF_Apple_iPhone_X_Juan_Mortyme_parts.7z.002)
[https://d17k3c8pvtyk2s.cloudfront.net/CTF_Apple_iPhone_X_Ruth_Langmore.7z](https://d17k3c8pvtyk2s.cloudfront.net/CTF_Apple_iPhone_X_Ruth_Langmore.7z)
[https://d17k3c8pvtyk2s.cloudfront.net/CTF_Samsung_Galaxy_A10e_Tony_Mederos.7z](https://d17k3c8pvtyk2s.cloudfront.net/CTF_Samsung_Galaxy_A10e_Tony_Mederos.7z)
[https://d17k3c8pvtyk2s.cloudfront.net/CTF_Samsung_Galaxy_S8_Rene_Gade.7z](https://d17k3c8pvtyk2s.cloudfront.net/CTF_Samsung_Galaxy_S8_Rene_Gade.7z)

Images were password protected. An email had to be sent to the Cellebrite CTF team to get the password to the images. to The images provided were two iPhone X images, a Samsung Galaxy A10e, and a Samsung Galaxy S8. Questions were of three varying difficulties with different points rewarded. 

- Level 1 – 10 points each
- Level 2 – 20 points each
- Level 3 – 50 or 100 points each

Hints were given for certain questions but also cost a certain number of points to view. A trial copy of Cellebrite Physical Analyzer was provided for two weeks to use for the competition. Again, the Cellebrite CTF team had to be emailed for a license. The trial version of Physical Analyzer lasts for two weeks.

## Tony Mederos Galaxy A10e

### Extraction Type – 10pts

> What type of extraction is this? (Acronym or Full Wording)

This question appears simple but actually took a few tries to answer properly. Cellebrite appears to list the extraction type right on the `Extraction Summary` page. 


![Extraction type](https://starwarsfan2099.github.io/public/2020-11-02/tony_1.JPG){:.shadow}{:.center}{: width="407" height="217" }


However, `File System` and `File System [ Android ADB ]` are not accepted answers. 

The correct accepted answer is `Full File System`. 
{:.success}

### Operating System – 10pts

> What Android Version is this device running? (enter just numerical value)

The OS version can also be seen right in the `Extraction Summary` tab. 


![Android OS version](https://starwarsfan2099.github.io/public/2020-11-02/tony_2.JPG){:.shadow}{:.center}{: width="682" height="114" }


The source of this information is the `build.prop` file:


![Android OS version source](https://starwarsfan2099.github.io/public/2020-11-02/tony_3.JPG){:.shadow}{:.center}{: width="454" height="95" }


The solution is `10`.
{:.success}

### Crypto – 10pts

> What is the name of the Crypto Currency application?

Simply look under the `Installed Applications` tab then `Cryptocurrency`.


![Crypto app](https://starwarsfan2099.github.io/public/2020-11-02/tony_5.JPG){:.shadow}{:.center}{: width="362" height="186" }


`com.mycelium.wallet` is installed, with the app name being `Mycelium` and the solution to this question.
{:.success}

### Security Patch – 20pts

> What Security Patch Level does this device have? (Date Format: MM-DD-YYYY for example: 12-30-2025)

The security patch is also found further down in the `build.prop` file. 


![Android security patch](https://starwarsfan2099.github.io/public/2020-11-02/tony_4.JPG){:.shadow}{:.center}{: width="386" height="75" }


Converting this to the answer format, we get `05-01-2020` as the solution.
{:.success}

### Location Location Location – 20pts

> Was Tony looking for any houses, if so, in what city?

Hmm. Tony probably tried looking up houses for sale online. Lets check that. Going to the `Web History` tab and searching for "house" shows Tony visited [https://www.realtor.ca/](https://www.realtor.ca/).


![House search](https://starwarsfan2099.github.io/public/2020-11-02/tony_6.JPG){:.shadow}{:.center}{: width="1131" height="189" }


Searching for "realtor" shows us a list of all the pages on the website he visited. 


![Realtor search](https://starwarsfan2099.github.io/public/2020-11-02/tony_7.JPG){:.shadow}{:.center}{: width="1125" height="278" }


These links are viewable in a browser through copying or Control-Clicking on the link in the tab on the right. Several of these links contain specific information Tony was looking for. Viewing them in the browser shows the exact page Tony was looking at.


![Houses](https://starwarsfan2099.github.io/public/2020-11-02/tony_8.JPG){:.shadow}{:.center}{: width="908" height="601" }


This shows that Tony was looking for houses in *Vancouver*. 
{:.success}

### Job Search – 20pts

> What possible new jobs was Tony looking at?

Again, starting with Tony's browsing history, we can see one of the nine phrases Tony searched is "*how much does an oil tanker captain make*", found under the `Searched Items` tab.


![Houses](https://starwarsfan2099.github.io/public/2020-11-02/tony_9.JPG){:.shadow}{:.center}{: width="401" height="313" }


Searching for "*captain*" in the `Web History` tab also shows a website he looked at after this Google search. 


![History](https://starwarsfan2099.github.io/public/2020-11-02/tony_10.JPG){:.shadow}{:.center}{: width="1077" height="86" }


The solution to this challenge is the job he Googled about, a "*ship captain*".
{:.success}

### Wallet ID – 20pts

> What's the Crypto Wallet ID?

Searching the entire image for "*wallet*" yields several results, including one in the user's messages with Rene. You can find a wallet ID by simply going up a few messages in the conversation to get some context.


![Wallet ID](https://starwarsfan2099.github.io/public/2020-11-02/tony_11.JPG){:.shadow}{:.center}{: width="355" height="348" }


The solution is `33wnUqRbPT49Z6c7Mkc3PojBHAJEZuacao`.
{:.success}

### Name – 20pts

> What is Scurvy’s real name? (Given name only)

Searching the entire image for "*scurvy*" gives a lot of results. The Android contacts database doesn't list a full name for Mr. Scurvy. The social media results are interesting though. There are several Facebook comments from a "Paul Scurvy".


![Scurvy](https://starwarsfan2099.github.io/public/2020-11-02/tony_12.JPG){:.shadow}{:.center}{: width="406" height="37" }


Entering "*Paul Scurvy*" shows us this is the correct answer.
{:.success}

### Auto Join WiFi – 50pts

> Was Auto Join enabled on CSIS?

Selecting the `Wireless Networks` tab from the summary page, we can see the information about the `CSIS` access point.


![Access point](https://starwarsfan2099.github.io/public/2020-11-02/tony_13.JPG){:.shadow}{:.center}{: width="373" height="350" }


Going to the XML source file and searching for "*auto*" reveals the presence of an attribute titled `AutoReconnect`. 


![AutoReconnect](https://starwarsfan2099.github.io/public/2020-11-02/tony_14.JPG){:.shadow}{:.center}{: width="320" height="186" }


The value is set to `1`. So, **Yes**, auto join was enabled.
{:.success}

### WiFi Password – 100pts

> What was the password for the Network of CSIS Mesh?

The plaintext WiFi password is not stored in the XML file found above. Other searches for `CSIS Mesh` did not yield anything of worth. The XML file is found at `/data/misc/wifi/WifiConfigStore.xml`. There are several other directories in `/data/misc` that pertain to WiFi information. In `/data/misc/wifi_share_profile/backup.conf`, the plaintext password can be seen in the file.


![WiFi](https://starwarsfan2099.github.io/public/2020-11-02/tony_15.JPG){:.shadow}{:.center}{: width="1362" height="282" }


The password to the network is `abcdef1234`.
{:.success}