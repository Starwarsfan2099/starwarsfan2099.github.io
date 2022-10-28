---
title: Cellebrite Spring 2021 CTF - Part 4 - Marsha - iPhone X
excerpt: Solutions to 2022 Spring Cellebrite CTF! Part 4! This part looks at the solutions to the questions associated with the image of Marsha's iPhone X. 
categories: [CTF, Cellebrite 2022]
tags: cellebrite-ctf ctf forensics
author: clark
---

## Marsha's iPhone X - iOS 14.6 

### Question 44 – 10pts

> Criminals tend to keep their business private. The suspects used an App that hides data (photos/video/contacts) behind an ordinary calculator. Provide icloud address used to purchase this app.

The iCLoud address used by Marsha can be found on the Physical Analyzer homepage.


![iCloud address](https://starwarsfan2099.github.io/public/2022-06-09/44.JPG){:.shadow}{:.center}


It's a clever email address as well, `marshamellos@icloud.com` is the correct solution. 
{:.success}

### Question 45 – 10pts

> What is the device vendor’s internal model name?

The internal model name can also be found on the homepage.


![Internal model name](https://starwarsfan2099.github.io/public/2022-06-09/45.JPG){:.shadow}{:.center}


The internal model name is `D22AP`. 
{:.success}

### Question 46  – 10pts

> Which 3rd party app had the longest active session? provide app identifier such as: com.ubercab.UberClient

We can go to the `Aggregated Application Usage` tab to how long applications were used for and when. Then, we can sort by `Active time` to see the longest sessions. 


![App usage](https://starwarsfan2099.github.io/public/2022-06-09/46.JPG){:.shadow}{:.center}


The longest active session belongs to `com.apple.SleepLockScreen`, however, that is not a third party app. The longest session on a third party app was 01:12:24 spent in `com.google.photos`. 
{:.success}

### Question 47  – 10pts

> What is the MD5 hash value for the file classified as Type: Images with a file size of 68147 bytes?

Once again, we need to use the `Images` tab. From there, we can simply search for the filesize! 


![Image](https://starwarsfan2099.github.io/public/2022-06-09/47.JPG){:.shadow}{:.center}


Using the returned results, we can see the exact image and the file hash. The hash and solution is `d9777bb03efb817bb6eaeec026a5b0c2`.
{:.success}

### Question 48 – 20pts

> The suspect had Pizza for lunch, what was the date and time of the order? Format: MM-DD-YYYY HH:MM, e.g. 01-22-2019 19:46

For this question, I got lucky and had stumbled across a photo of a receipt earlier. I'm sure there is a way to find it via Cellebrite's image classification. 


![Receipt](https://starwarsfan2099.github.io/public/2022-06-09/48.JPG){:.shadow}{:.center}


The data and time she had lunch was `03-08-2021 12:11`. 
{:.success}

### Question 49 – 20pts

> The investigators were looking for a specific Kia stolen by the gang. They were missing 3 digits of the license plate (left most). Find the first 3 digits they were missing.

Once again, I got lucky and stumbled upon this solution while looking for another challenge's solution. The intended solution is probably more image categorization using a vehicle/license plate number filter. Remember, always read all of the questions in a section before grinding to solve the first one, it can pay off. 


![Receipt](https://starwarsfan2099.github.io/public/2022-06-09/49.JPG){:.shadow}{:.center}


The first three digits are `508`. 
{:.success}

### Question 50 – 20pts

> What is the most frequently interacted phone number over a call? format should be +[country_code][number] for example: +97243501234

First, we need to go to the `Call Log` tab. Then we can select the `Parties` tab to allow us to sort by the calls. This dialog also shows a count of repeated incoming or outgoing calls. 


![Call log](https://starwarsfan2099.github.io/public/2022-06-09/50.JPG){:.shadow}{:.center}


By quickly scrolling the list, we can see the most frequently interacted with number is `+15162879924`. 
{:.success}