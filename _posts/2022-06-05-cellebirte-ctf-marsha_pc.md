---
title: Cellebrite Spring 2021 CTF - Part 1 - Marsha - PC
excerpt: Solutions to 2022 Spring Cellebrite CTF! Part 1! This part looks at the solutions to the questions associated with the image of Marsha's Windows 10 PC. 
tags: cellebrite-ctf ctf forensics
author: rms
---

## Cellebrite 2022 CTF!

Cellebrite decided to launch another CTF this year! Their last CTF was quite fun and helped me learn more about forensic methodology. Here's the scenario for this year:

> Beth Dutton was invited to the Vienna Inn in Vienna, VA on July 21st at 5:00 PM and was arrested while there. She was invited by Heisenberg. Police arrested her for grand theft. Upon questioning Beth, she revealed that her sister, Marsha Mellos introduced her to Heisenberg and that he was responsible for stealing cars and she and her sister were innocent. They are in the cattle business in Montana and got mixed up with the wrong guy. Marsha has both a PC and an iPhone. Beth had an iPhone and Heisenberg had an Android.  The interest here is auto theft and selling. Cash transfers matter.

## Marsha's PC - Windows 10 - Build 19043

For the first set of challenges, we can't use Cellebrite's tools just yet. We'll start with Magnet AXIOM. 

### Question 1 – 10pts

> What is the Serial Number of the disk acquired?

To solve this challenge, we don't even need to load the image. The answer can be found in `Acquisition Log.txt`. 

{:refdef: style="text-align: center;"}
![/dev/sda serial](https://starwarsfan2099.github.io/public/2022-06-11/serial.JPG){:.shadow}
{: refdef}

The serial number for `/dev/sda` is `170615BA93CC` and is the solution for challenge 1.
{:.success}

### Question 2 – 10pts

> How did the user most recently sign into Windows?

The first approach we can use is the Magnet Timeline view and filter by account activity. It shows data for the last login, but not the login type that we need. Next, we can check the registry. [Some Googling](https://social.technet.microsoft.com/Forums/windows/en-US/7fb857b3-a760-40fb-a8be-a14ffa285214/i-need-to-be-able-to-change-the-default-domainuser-logon-prompt?forum=w7itprosecurity) shows that the last login information can be found under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI`. This can be access within the Magnet Registry viewer. 

{:refdef: style="text-align: center;"}
![Registry path](https://starwarsfan2099.github.io/public/2022-06-11/lastlogon.JPG){:.shadow}
{: refdef}

We can see the key `LastLoggedOnDisplayName` to see who logged in (Marsha) and `LastLoggedOnProvider` shows us the method: `{BEC09223-B018-416D-A0AC-523971B639F5}`. Microsoft provides a handy table for the credential providers [here](https://docs.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/feature-multifactor-unlock). 

{:refdef: style="text-align: center;"}
![Providers table](https://starwarsfan2099.github.io/public/2022-06-11/providers.JPG){:.shadow}
{: refdef}

And now we have the sign in method! The credential provider `BEC09223-B018-416D-A0AC-523971B639F5` is the Fingerprint login method. 

`fingerprint` is the solution to the challenge. 
{:.success}

### Question 3 – 10pts

> Someone stole a truck and left his inmate card behind. What is his inmate number?

Now we need to find a card number. Since we aren't given any idea as to the length or format of the number, we can make the educated guess that there is a picture of the card. When processing the case, I enabled the Magnet.AI image categorization. This lets a user sort by images that may contain drugs, documents, id's, etc. Unfortunately, no image with an inmate card was categorized under Card/ID. However, several images can help lead where should look. One image is a photo of a sim packaging card and is stored in `C:\Users\marsh\OneDrive\Pictures\Camera Roll`. Looking around these directories, one can find a `Pictures\Screenshots` directory with several images, one being an inmate card!

{:refdef: style="text-align: center;"}
![Inmate card](https://starwarsfan2099.github.io/public/2022-06-11/card.JPG){:.shadow}
{: refdef}

The inmate number and solution is `2101460`.
{:.success}

### Question 4 – 10pts

> What is the serial number of the last USB drive connected to the device, excluding acquisition tools?

One of the first places to go when time is involved in a question, is the timeline. In Magnet, we can sort the timeline by latest first and filter by only USB device usage. The last devices used shows the following details:

{:refdef: style="text-align: center;"}
![Last USB](https://starwarsfan2099.github.io/public/2022-06-11/blackbag.JPG){:.shadow}
{: refdef}

Seeing as this has the manufacturer listed as Blackbag, a forensic company now owned by Cellebrite, this is probably the acquisition device. Continuing down the timeline of devices, the next device found is a Toshiba USB 3.0 flash drive. 

{:refdef: style="text-align: center;"}
![Other last USB](https://starwarsfan2099.github.io/public/2022-06-11/toshiba.JPG){:.shadow}
{: refdef}

The listed serial number is `20151017004222F`. This is the solution! 
{:.success}

(Note, you may have noticed the `&F` after the serial in the image. This appears to be a parsing error and the "&" character shouldn't appear in a flash drive serial number.)

### Question 5 – 10pts

> What is the only camera model that was found within a picture created by the user browsing the Internet? e.g. 1 3 01-22-2019 19:46

Magnet AXIOM Examine keyword searches include image metadata, so we can just do a search for common camera manufacturers. Searching for "canon" reveals a single cached image that contains the camera model in metadata. 

{:refdef: style="text-align: center;"}
![Camera](https://starwarsfan2099.github.io/public/2022-06-11/canon.JPG){:.shadow}
{: refdef}

The camera model in the metadata is a `Canon EOS 5D Mark II` and is the solution to this challenge!
{:.success}

### Question 6 – 10pts

> What two email addresses were found in web forms? Format: [email address] [email address] e.g. john@gmail.com ryan@gmail.com

One again, we can use the keyword search and filtering to our advantage. Searching for the "@" character and filtering by 'Web Related' category shows us the first email in the Chrome autofill:

{:refdef: style="text-align: center;"}
![Chrome](https://starwarsfan2099.github.io/public/2022-06-11/chrome.JPG){:.shadow}
{: refdef}

There aren't any more user related emails returned though. Searching for common email domain names within the Web Related and form content still wasn't revealing anything. Finally, filtering web related content for the keyword "email" and web encoded @ character (%40), another email is revealed in the carved Webkit Browser history! 

{:refdef: style="text-align: center;"}
![Another email](https://starwarsfan2099.github.io/public/2022-06-11/email.JPG){:.shadow}
{: refdef}

Hmmmm. Seeing as this a Cellebrite email address, one would think it *might* not be an intended solution, but attempting to submit `marsha4mellos@gmail.com sydney.peason@cellebrite.com` reveals it is indeed the intended solution!
{:.success}

### Question 7 – 20pts

> What is the content of a user-made file where the file extension is a mismatch?

For this challenge, I had accidentally stumbled upon the answer when trying to solve challenge #3. When browsing around `C:\Users\marsh`, a Google drive folder can be found. Inside this folder is a file titled `Figure it out.zip`. AXIOM Examine immediately shows something is up with the file.

{:refdef: style="text-align: center;"}
![Zip file?](https://starwarsfan2099.github.io/public/2022-06-11/notzip.JPG){:.shadow}
{: refdef}

The file is actually just a text file containing the ASCII text `Huh this is a test`. And that text is the solution to challenge 6!
{:.success}

### Question 8 – 20pts

> The target captured a sports game that took place in April 2014. What was the name of the venue (at that time) and the name of the guest team? Format: [Name of stadium] [guest team] eg: Mercedes Benz Stadium Atlanta Falcons

This seems easy enough. First, select the **Media** category then set the date/time filter to between 4/1/2014 and 4/30/2014. This shows a single `.MOV` file that records the game that day.

{:refdef: style="text-align: center;"}
![Stadium game](https://starwarsfan2099.github.io/public/2022-06-11/video.JPG){:.shadow}
{: refdef}

Looking at the footage, we can see the stadium name in the background!

{:refdef: style="text-align: center;"}
![Stadium name](https://starwarsfan2099.github.io/public/2022-06-11/game.JPG){:.shadow}
{: refdef}

This is the Centurylink Field. A quick [Google search](https://www.alamy.com/april-26-2014-seattle-sounders-fc-fans-during-a-match-against-the-image68825366.html) for the date the video was taken reveals this is the Seattle Sounders vs. the Colorado Rapids. 

Using the specified format, the solution is `Centurylink Field Colorado Rapids`!
{:.success}

### Question 9 – 20pts

> How many unique acquisition tools were recognized by Marsha’s PC, how many times did the acquisition tools connect, and when was the last time an acquisition tool was connected? Format: [unique #] [total #] MM-DD-YYYY HH:MM e.g. 1 3 01-22-2019 19:46

Unfortunately, I was unable to solve this challenge. Will update when I have solved it. 
{:.error}

### Question 10 – 50pts

> What is the Windows Hello PIN code of the user signed into the Windows PC with a Microsoft account?

Cool! We need to break a Windows Hello pin. Researching how to crack a Windows Hello Pin leads to the [WINHELLO2hashcat Github repo](https://github.com/Banaanhangwagen/WINHELLO2hashcat). It's a Python script designed to spit out a hash that is crackable with Hashcat. Looking at the README and some other tutorials, we first need to export some files and folders from the image to pass to the tool. 

| Argument | Path |
|----|----|
| --cryptokeys | C:\Windows\ServiceProfiles\LocalService\AppData\Roaming\Microsoft\Crypto\Keys |
| --masterkey | C:\Windows\System32\Microsoft\Protect\S-1-5-18\User |
| --ngc | C:\Windows\ServiceProfiles\LocalService\AppData\Local\Microsoft\Ngc |
| --system | C:\Windows\System32\config\SYSTEM |
| --security | C:\Windows\System32\config\SECURITY |
| --software | C:\Windows\System32\config\SOFTWARE |

Once we have those, we can run the tool to get the pin hash.

{:refdef: style="text-align: center;"}
![Hash](https://starwarsfan2099.github.io/public/2022-06-11/hellohash.JPG){:.shadow}
{: refdef}

Then, we can pass the hash as input to Hashcat. Hahcat needs to be passed the mode for the Windows Hello Pin (`-m 28100`), an attack type (`-a 3` for a mask attack), the mask (`?d?d?d?d` for 4 digit passcode), and the file containing the hash as well output file. However, Hashcat fails exhausts all codes without finding the correct one. Trying a 6 digit pincode (`?d?d?d?d?d?d`) works!

{:refdef: style="text-align: center;"}
![Hash cracked](https://starwarsfan2099.github.io/public/2022-06-11/crack.JPG){:.shadow}
{: refdef}

The Windows Hello pin and the solution to this challenge is `134679`!
{:.success}

### Question 11 – 100pts

> What is the Personal Meeting ID of the Zoom user account holder?

Sadly, this question went unsolved as well. Again, will update if I get it figured out. 
{:.error}

### Question 12 – 100pts

> What is the password for the URL containing a private IPv4 address in Microsoft Edge web browser’s saved logins? (Case Sensitive)

I ended up solving this challenge after the CTF ended, but it was still a fun solve. As far as research went, there is no easy way to get the decrypted Edge passwords. But it could be done if it was possible to log into the machine. WHich it is! Using FTK's image mounter and VMWare Workstation, we can mount the E01 and load up a VM of Marsha's machine. [Here is the tutorial I used](https://habr.com/en/post/444940/). After that, simply log into the machine using the Windows Hello Pin we found earlier, open Edge, go to **Settings > Passwords**, and reveal the password! 

{:refdef: style="text-align: center;"}
![Pass](https://starwarsfan2099.github.io/public/2022-06-11/pass.JPG){:.shadow}
{: refdef}

The password used to log into 104.106.102:9997 was `NPaacYaE`.
{:.success}