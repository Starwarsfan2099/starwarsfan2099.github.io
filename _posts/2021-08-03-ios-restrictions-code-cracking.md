---
title: iOS Restrictions Code Cracking
excerpt: Diving into recovering a forgotten iOS device's restrictions passcode and writing a tool to do so automatically. 
cover_size: sm
tags: forensics programming
author: rms
---

## Background

This is a tool I wrote three years ago, but had to use again a few days ago and thought I would make a write up about it. So, growing up in a family of 7 and being the one most interested in technology meant I became tech support for my family. As the oldest sibling, I would teach my siblings how to use computers, phones, and iPods. I would also help my parents at handling my sibling's technology. One day, my mother came to me asking if I could get a forgotten passcode for her off one of my youngest sibling's iPod. Surprisingly though, it wasn't the device passcode - it was the passcode to the restrictions.

## iOS Restrictions Passcode

Apple allows restrictions to be setup on their devices. The primary use of these is for parental control - such as disabling installing apps or disabling 18+ music downloads. The restrictions require a separate password be set for access to the restrictions control page. If this code is forgotten, there is no way to recover it. Typically, the device would have to be reset. I didn't exactly want to reset the device, so my goal was to find or crack the restrictions passcode. 

### How does it work?

That's what I wanted to find out. First, I grabbed my jailbroken device and started browsing around the file system. Since the passcode is entered directly into a page in settings, I started looking there hoping I could find a base64 encoded passcode or something simple. Under `/Library