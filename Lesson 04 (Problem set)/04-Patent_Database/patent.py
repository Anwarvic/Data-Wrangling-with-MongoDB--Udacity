#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This and the following exercise are using US Patent database. The patent.data
file is a small excerpt of much larger datafiles that are available for
download from US Patent website. These files are pretty large ( >100 MB each).
The original file is ~600MB large, you might not be able to open it in a text
editor.

The data itself is in XML, however there is a problem with how it's formatted.
Please run this script and observe the error. Then find the line that is
causing the error. You can do that by just looking at the datafile in the web
UI, or programmatically. For quiz purposes it does not matter, but as an
exercise we suggest that you try to do it programmatically.

NOTE: You do not need to correct the error - for now, just find where the error
is occurring.
"""

import xml.etree.ElementTree as ET
import re

PATENTS = 'patent.data'
def get_root(fname):

    tree = ET.parse(fname)
    """
    The error was due to two main reasons:
     -> the XML file doesn't have a <root> tag which is essential to contain all the other nodes.
     -> XML file was bad-formatted due to the repeating defining the XML version and the document type
        which should be done once at the beginning of the file.
    I solved these problems directly in the data. 
    """
    return tree.getroot()


get_root(PATENTS)