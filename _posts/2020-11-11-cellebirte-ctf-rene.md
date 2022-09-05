---
title: Cellebrite Fall 2020 CTF - Part 2 - Rene Gade
excerpt: Solutions to the 1st ever Cellebrite CTF! Part 2! This part looks at the solutions to the questions associated with the image of Rene Gade's phone. 
tags: cellebrite-ctf ctf forensics
author: rms
---

## Rene Gade's Samsung Galaxy 8+

### Social Media – 10pts

> What is the Snapchat username used by the device owner?

This first question simply asks us what Rene's user's Snapchat username is. Processing Snapchat with AppGenie returns a list of contacts, chats, and also users.

{:refdef: style="text-align: center;"}
![Accounts](https://starwarsfan2099.github.io/public/2020-11-11/rene_2.JPG){:.shadow}
{: refdef}

Selecting `User Accounts` reveals a single table entry with Rene's Snapchat username and a bit more data.

{:refdef: style="text-align: center;"}
![Snapchat account](https://starwarsfan2099.github.io/public/2020-11-11/rene_1.JPG){:.shadow}
{: refdef}

Rene's Snapchat username is "renegade7696" and is the solution to the challenge.
{:.success}

### User Identification – 20pts

> When analyzing the device extraction, determine the Facebook username being used on this device by this user.

Similar to the above challenge, this question asks us for Rene's Facebook username. This can easily be found under `User accounts` and searching for "*facebook*". This reveals 4 rows in the table that deal with Facebook, and one lists the account.

{:refdef: style="text-align: center;"}
![Facebook account](https://starwarsfan2099.github.io/public/2020-11-11/rene_3.JPG){:.shadow}
{: refdef}

The Facebook account signed into Rene's phone is `andy.rod.3910`.
{:.success}

### User Activity – 20pts

> Provide the date the user of this device joined Zoom. Answer must be entered in MM-DD-YYYY format. Use the date associated to UTC+0 timezone for this flag.

Okay, this question wants the date Rene joined Zoom. Zoom can use text messages or emails to verify an account when it is created. Searching the messages for "*zoom*" reveals a single message from Zoom on May 5th, 2020. 

{:refdef: style="text-align: center;"}
![Zoom text](https://starwarsfan2099.github.io/public/2020-11-11/rene_4.JPG){:.shadow}
{: refdef}

However, this message doesn't tell us when the Zoom account was made, just a day when it was used. Searching for "*zoom*" in the emails reveals one with the subject `Please activate your Zoom account`. 

{:refdef: style="text-align: center;"}
![Zoom email](https://starwarsfan2099.github.io/public/2020-11-11/rene_5.JPG){:.shadow}
{: refdef}

The email was sent to Rene's email on `5/1/2020`. Converting it to the format required by the question reveals the solution - `05-01-2020`. 
{:.success}

### Database Analysis – 20pts

> What is the name of the database table that contains direct messages involving the Instagram user id 38106270876?

This question gives us a lot of information. We simply need to find a table name in an Instagram database. We can view the databases in the Instagram app be going to the `Installed Applications`, finding Instagram, and opening the SQLite viewer. Searching for the user ID didn't yield any results. Hm. Just quickly skimming through the databases results in finding the correct table. In `direct.db`, a table appropriately titled "messages" contains our user ID and messages.

{:refdef: style="text-align: center;"}
![Instagram database](https://starwarsfan2099.github.io/public/2020-11-11/rene_6.JPG){:.shadow}
{: refdef}

The solution to the challenges is "messages".
{:.success}

### Files – 20pts

> Ruth sent a video to Rene of a rocket launch. What is the size of the video file in bytes? 

The question says the video was sent from Ruth to Rene. To narrow down this search, a good first assumption based on the wording could mean that the conversation was only between the two. We can filter the chats for only chats between the two people. Then using the attachments tab, look through them for any videos of a rocket launch. Eventually you get to a conversation that began on May 1st. 

{:refdef: style="text-align: center;"}
![Rene and Ruth conversation](https://starwarsfan2099.github.io/public/2020-11-11/rene_7.JPG){:.shadow}
{: refdef}

In the attachments section, a video named `IMG_0036.3gp` is found. This video does in fact contain a rocket launch. 

{:refdef: style="text-align: center;"}
![Rocket](https://starwarsfan2099.github.io/public/2020-11-11/rene_8.JPG){:.shadow}
{: refdef}

In the `File Info` tab, the file size can be seen.

{:refdef: style="text-align: center;"}
![Rocket file size](https://starwarsfan2099.github.io/public/2020-11-11/rene_9.JPG){:.shadow}
{: refdef}

The solution to this challenge is `650880`. 
{:.success}

### MMS Analysis – 20pts

> The hash value a8eb9547d95f569dfde4bceded3f9867 is associated to a file sent to Rene Gade. What is the timestamp of the MMS message associated with this file? ANSWER MUST BE FORMATTED AS: MM-DD-YYYY HH:MM:SS – use the 24-hour clock and do not include time offset. For example, for January 16, 2020 at 10:01:52 PM, the correct answer would be: 01-16-2020 22:01:52

Well, I didn't select the `Hash files` option when loading up the images in Cellebrite. I tied searching the hash anyway just in case and it actually showed some results.

{:refdef: style="text-align: center;"}
![Search results](https://starwarsfan2099.github.io/public/2020-11-11/rene_10.JPG){:.shadow}
{: refdef}

The first file is from a PART file. The second file is a messaging cache file. That could be what we're after. 

{:refdef: style="text-align: center;"}
![Cache](https://starwarsfan2099.github.io/public/2020-11-11/rene_11.JPG){:.shadow}
{: refdef}

Selecting the source file takes us to the hex view of the DAT file. In this file, just above the image, we see two phone numbers in the file!

{:refdef: style="text-align: center;"}
![Hex view](https://starwarsfan2099.github.io/public/2020-11-11/rene_12.JPG){:.shadow}
{: refdef}

Now that we have a phone number, we can search for it in the chats and look in the attachments sent for the conversations. Sure enough, we find the attachment in the first conversation returned. 

{:refdef: style="text-align: center;"}
![Conversations](https://starwarsfan2099.github.io/public/2020-11-11/rene_13.JPG){:.shadow}
{: refdef}

Simply scrolling down the conversation, the image and the timestamp can be seen.

{:refdef: style="text-align: center;"}
![Timestamp](https://starwarsfan2099.github.io/public/2020-11-11/rene_14.JPG){:.shadow}
{: refdef}

Converting this to the format required by the challenge, we get the solution, `08:14:2020 20:36:27`. 
{:.success}

### Application Analysis – 20pts

> What is the most recent Uber code received by the device?

This question simply asks for the last Uber code received. Uber codes are typically received over text. Going to the `Chats` tab and search for "*Uber*" reveals a single conversation. 

{:refdef: style="text-align: center;"}
![Uber codes](https://starwarsfan2099.github.io/public/2020-11-11/rene_15.JPG){:.shadow}
{: refdef}

The last received code is `3748`. 
{:.success}

### User Identification – 50pts

> A "cashtag" is an individual user’s Cash App username. Determine Rene Gade's "cashtag".

Time to find another username. AppGenie is not available for "Cash App", so I went to look through it's databases. Again, using the `Installed applications` > `Cash App` > `Run SQLite Wizard`. The first database is `cash_money.db`. In this database, a certain table stands out that could have information we want. Namely, the `customer` table.

{:refdef: style="text-align: center;"}
![Cash App Customer Table](https://starwarsfan2099.github.io/public/2020-11-11/rene_16.JPG){:.shadow}
{: refdef}

Sure enough, right there is the cashtag username for Rene - `renegader2020`. 
{:.success}

### Financial Information – 100pts

> Rene sent Juan bank account information in a less than conventional manner. What is the Bank of America routing and account number sent to Juan? ANSWER MUST BE FORMATTED AS: routing:account (no spaces, use colon to separate the numbers provided. For example: 1234567:1234567890)

And last but certainly not least, the big 100 point question. The question says "less than conventional manner". Hm. I began by filtering conversations with Juan and then search those for references to banks and money. One of the conversations that mentions money began on April 30th, 2020. It discusses sending money. Going further back in the history, this suspicious message can be seen.  

{:refdef: style="text-align: center;"}
![Suspicious info](https://starwarsfan2099.github.io/public/2020-11-11/rene_17.JPG){:.shadow}
{: refdef}

Hm. "PDF". Maybe it's hidden via steganography in the PDF file. Checking through many PDF files for hidden metadata, strings, and steganography techniques revealed nothing. However, another member of our team made a connection. [Gerbinator](https://github.com/Gerbinator) had seen that one of the PDFs that showed up in several places was named "**M**arijuana **G**row **B**ible". "**MGB**31PDF". Page 31 in the weed bible PDF. Checking there reveals the routing numeber in plain sight. 

{:refdef: style="text-align: center;"}
![Routing info](https://starwarsfan2099.github.io/public/2020-11-11/rene_18.JPG){:.shadow}
{: refdef}

Putting the information in the correct format, we get the solution `121000358:9879982234471`.
{:.success}