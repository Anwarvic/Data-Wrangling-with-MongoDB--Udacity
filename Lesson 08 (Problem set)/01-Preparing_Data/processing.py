#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a dictionary of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc
- strip leading and ending whitespace from all fields, if there is any

- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
"""
import codecs
import csv
import json
import pprint
import re

NON_ALPHANUMERIC_LIST = ["&", "(" ,")", "–", "[", "{", "}", "]",  ":", ";", "'", ",", "?", "/", "*", '"']
DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}

def change_null_to_none(dic, field):
  # CHANGING 
  if dic[field] == "NULL":
    dic[field] = None

def delete_headings(dic, headings, fields):
  # DELETING ANY OTHER HEADING NOT IN FIELDS.KEYS()
  # AND ALSO CHANGES EVERY NULL VALUE IN ANY FIELD INTO NONE
  for heading in headings:
    if heading not in fields.keys():
      del dic[heading]

  for key in fields.keys():
    if dic[key] == "NULL" and key != "name":
      dic[key] = None

def change_headings(dic, fields):
    # CHANGING THE HEADINGS
    for key, value in fields.iteritems():
        dic[value] = dic[key]
        if key not in fields.values():
            del dic[key]
    

def trim_label(dic):
  # DELETE ADDITIONAL LABELS, THOSE IN PARENTHESES
  temp_list = dic["label"].split(" ")
      return temp_list[0]

def is_non_alphanumeric(string):
  #RETURN TRUE IF A GIVEN STRING HAS NO NON-ALPHANUMERIC CHARACTER
  for letter in string:
    if letter in NON_ALPHANUMERIC_LIST:
      return False
  return True


def trim_name(dic):
  # CHANGE NAME INTO LABEL IF IT'S 'NULL' OR HAS NON-ALPHANUMERIC CHARACTER 
  if dic["name"] != None:
    if dic["name"] == "NULL" or not is_non_alphanumeric(dic["name"]):
      dic["name"] = dic["label"]

def isarray(value):
    #RETURNS TRUE IF THE CELL HAS {}
    if "{" in value:
        return True
    else:
        return False      

def strip_astrix(string):
    #DELETES THE * CHARACTER FROM A GIVEN STRING
    temp = ""
    for letter in string:
        if letter == "*":
            pass
        else:
            temp += letter
    return temp.strip()


def fix_array(v):
    # CHANGES ARRAYS INTO LISTS
    temp_list = []
    output= []
    if v != None and isarray(v):
        s = v[1:-1]       #without squiggly brackets
        temp_list = s.split("|")
        for element in temp_list:
            output.append(strip_astrix(element))
    
        return output
    else:
        return v

def fix_array2(v):
    # CHANGES ELEMENTS INTO LISTS
    temp_list = []
    output= []
    if v != None and isarray(v):
        s = v[1:-1]       #without squiggly brackets
        temp_list = s.split("|")
        for element in temp_list:
            output.append(strip_astrix(element))
    
        return output
    else:
        if v != None:
            return [v]

################# MAIN FUNCTION ######################
def process_file(filename, fields):
    process_fields = fields.keys()
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        headings = reader.fieldnames
        for i in range(3):
            l = reader.next()

        for line in reader:
            # DELETING ANY OTHER HEADING NOT IN FIELDS.KEYS()
            # AND ALSO CHANGES EVERY NULL VALUE IN ANY FIELD INTO NONE
            delete_headings(line, headings, FIELDS)

            # CHANGING THE HEADINGS
            change_headings(line, FIELDS)

            #DELETE ADDITIONAL LABELS, THOSE IN PARENTHESES
            line["label"] = trim_label(line)

            # CHANGE NAME INTO LABEL IF IT'S 'NULL' OR HAS NON-ALPHANUMERIC CHARACTER 
            trim_name(line)

            # CHANGE THESE FIELDS OF ARRAYS INTO LISTS
            line["synonym"] = fix_array2(line["synonym"])
            line["family"] = fix_array(line["family"])
            line["class"] = fix_array(line["class"])
            line["phylum"] = fix_array(line["phylum"])
            line["order"] = fix_array(line["order"])
            line["kingdom"] = fix_array(line["kingdom"])


            # ADD CLASIFICATION  FIELD 
            line["classification"] = {}
            line["classification"]["family"] = line["family"]
            del line["family"]
            line["classification"]["class"] = line["class"]
            del line["class"]
            line["classification"]["phylum"] = line["phylum"]
            del line["phylum"]
            line["classification"]["order"] = line["order"]
            del line["order"]
            line["classification"]["kingdom"] = line["kingdom"]
            del line["kingdom"]
            line["classification"]["genus"] = line["genus"]
            del line["genus"]


            #print line["synonym"]
            data.append(line)          

  return data


#process_file(DATAFILE, FIELDS)
# test = process_file(DATAFILE, FIELDS)
# print test[0]





def test():
    data = process_file(DATAFILE, FIELDS)

    pprint.pprint(data[0])
    assert data[0] == {
                        "synonym": None, 
                        "name": "Argiope", 
                        "classification": {
                            "kingdom": "Animal", 
                            "family": "Orb-weaver spider", 
                            "order": "Spider", 
                            "phylum": "Arthropod", 
                            "genus": None, 
                            "class": "Arachnid"
                        }, 
                        "uri": "http://dbpedia.org/resource/Argiope_(spider)", 
                        "label": "Argiope", 
                        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
                    }


if __name__ == "__main__":
    test()