#!/bin/bash

rm Packages.bz2
dpkg-scanpackages -m . /dev/null >Packages
bzip2 Packages
dpkg-scanpackages -m . /dev/null >Packages

