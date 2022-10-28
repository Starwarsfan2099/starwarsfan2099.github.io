---
title: Magnet AXIOM Introduction - Part 2
excerpt: Introduction and tutorial to the Magnet AXIOM suite of tools. In part two, we'll look at AXIOM Examine and how it can be used to search for evidence.
categories: [Tutorial, Magnet AXIOM]
tags: forensics
author: clark
---

## What is Magnet AXIOM?

Magnet AXIOM is advertised as a comprehensive suite of tools for digital forensic investigations that can recover and analyze digital evidence from most sources, including smartphones, cloud services, computers, IoT devices and third-party images. The tool also is equipped with unique analysis tools, such as AI chat categorization, image categorization, and comprehensive keyword search functions pre-processing. 

In Part 2, we will focus on the basics of AXIOM Examine and using the tool to search for evidence. AXIOM Examine is Magnet's solution for sifting through processed data for evidence. The tool is fully equipped for timeline analysis, keyword searching, analyzing evidence connections, and much more. 

## AXIOM Examine

### Case Dashboard


![Start Screen](https://starwarsfan2099.github.io/public/2021-04-05/main.JPG){:.shadow}{:.center}


After opening AXIOM Examine, the first view you will see is the **Case Dashboard** view. There are several boxes and options in this view. Looking at the boxes and starting at the top left, you can see the *Case Summary* box. This box includes the examiner name and the case summary. Below this is the *Case Processing Details*. This box shows who scanned and processed the evidence, when it was processed, and a scan description if it was filled in during the processing phase. And below that is the *Case Information* box. This allows the examiner to open the case information file as well as the log file.

In the center, is the *Evidence Overview*. This is where the individual evidence sources can be found. You can see the Evidence Number, Description, Location, and Platform type for all the evidence. You can also add a picture of the evidence and select *View Evidence for this Source Only* to see the artifacts for only that evidence source. There is also a button for adding new evidence sources.

On the right is the *Places to Start* section. AXIOM gives us firstly a nice *Artifact Categories* section. You can select the evidence source, or view it for all sources (default). It's a quick way to see what kind of data was on the device and what artifact category could be interesting to look at. Below this is the *Tags and Comments* box. This box will show any evidence that has been given any tags or comments by the examiner. Next is the *Magnet.AI Categorization* box. This box allows us to filter by evidence that has been tagged with any of the categories selected during the processing phase. In this case, we can sort the evidence by *Possible Human Faces* and *Possible Drones/UAVs*. 

Below that section is the *CPS Data Matches* section. This section shows results from checking for any hashes, GUIDs, IPs, and more that have flagged by CPS. Below and to the left is the *Keyword Matches* box. This box shows the keywords entered during the processing phase. Selecting a keyword takes you to the evidence view showing only evidence that contains the keyword. Or, you can hit *View all keyword matches* to show only evidence with any of the keywords. Below that is the *Media Categorization* box. 

### Evidence View


![Evidence View](https://starwarsfan2099.github.io/public/2021-04-05/evidence.JPG){:.shadow}{:.center}


The evidence view looks daunting at first, but it's actually pretty simple. On the left, are the evidence categories. The artifacts found are automatically sorted and can be viewed using these. Sections like **All Evidence**, **Media**, **Documents**, and **Web Related**. The sections are further categorized into sub categories. These can be by application, file type, or just general artifact type. The categories and sub categories are extremely useful and allow for easily navigating through mountains of evidence. 

In the center of the screen is the **Evidence** pane. This is simply a list of artifacts or evidence in the category selected on the left. It can be sorted via selecting the columns at the top of this pane. On the right, is the **Details** pane. This pane is similar to the properties pane in the Windows. It shows details for the artifact that is currently selected. And finally, at the very top are the **Filters**. These allow for filtering artifacts based upon many criteria. Filtering works alongside of the categories selected on the right, with filters having priority. Artifacts that have been filtered will still be categorized. And just to the right of the filter is the search bar. This will search all the currently filtered artifacts. This includes text in documents, file names, and paths. 

Using the button to the right of the home button, in the top right, we can choose other views. 

### Timeline View


![Timeline View](https://starwarsfan2099.github.io/public/2021-04-05/timeline.JPG){:.shadow}{:.center}


In this view, evidence is presented and able to be sorted chronologically. The timeline range can be adjusted, artifacts can still be filtered, and the everything is presented chronologically based on these adjustments and is entirely searchable.

### Connections View


![Connections View](https://starwarsfan2099.github.io/public/2021-04-05/connections.jpg){:.shadow}{:.center}


This view can be accessed via right clicking on an artifact and selecting show connections. It builds and shows relationships of the selected artifacts with other artifacts and events. Artifacts can further be filtered, selected, and examined in this view. 

### Filesystem View


![Filesystem View](https://starwarsfan2099.github.io/public/2021-04-05/filesystem.JPG){:.shadow}{:.center}


If the examiner would rather directly search the file system, there's a tab for that as well.

### Registry and Media

There are tabs for the Windows Registry tab and a general Media tab. 

### So how is easy is finding evidence?

Remember that keyword search for *"Drone"*? Selecting it from the home page shows all artifacts associated with the word *drone*. 


![Filesystem View](https://starwarsfan2099.github.io/public/2021-04-05/drone.jpg){:.shadow}{:.center}


We are immediately greeted with conversations and contacts discussing the drone the batteries were taken from. Everything is easily viewable and presented to the examiner. Supporting evidence and more information can be easily found via the connections to the contact or conversation. The conversation can be bookmarked as flagged evidence and we can continue searching through artifacts. 

Magnet AXIOm is an amazingly useful tool in the forensic world. This small post only touches on a few of Magnet AXIOM's features, there are still plenty of useful features we have not looked at, and we may get to in another post. 