---
title: Windows `bootstat.dat` Forensic Parser
excerpt: Quick post to go over a Python parser for the Windows binary boot log. 
tags: programming forensics
author: rms
---

## Grzegorz Tworek's PSBits

{:refdef: style="text-align: center;"}
![Tweet](../public/2022-09-12/tweet.JPG){:.shadow}
{: refdef}

Grzegorz Tworek, also known as [0gtweet](https://twitter.com/0gtweet), posted this [link to a PowerShell script](https://github.com/gtworek/PSBits/blob/master/DFIR/Extract-BootTimes.ps1) a few days ago. I thought is was interesting, because I had never heard of this file, much less it being parsed for possible forensic measures. 