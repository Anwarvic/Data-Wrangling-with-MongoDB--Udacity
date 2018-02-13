#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'


def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False

def isarray(value):
    if "{" in value:
        return True
    else:
        return False

def fix_area(area):
    if area == "NULL":
        return None
    elif isarray(area):
        temp = area[1:-1]       #without squiggly brackets
        temp_list = temp.split("|")
        num1 = float(temp_list[0])
        num2 = float(temp_list[1])
        if num1>= num2:
            return num1
        else:
            return num2
    else:
        if isfloat(area):
            return float(area)
        else:
            return "A7A"

print fix_area("{5.51667e+07|5.53e+07}")

def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra matadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[8]["areaLand"] == 55300000.0
    assert data[3]["areaLand"] == None
    assert data[20]["areaLand"] == 14581600.0
    assert data[33]["areaLand"] == 20564500.0


if __name__ == "__main__":
    test()