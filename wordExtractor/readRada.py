import sys
import os
import math
import operator
import xml.etree.cElementTree as et
import pandas as pd

from xml.dom import minidom


#reading files names from dir
#return arr of files
def getFilenames(filedir):
    file_set = []
    for idx, file in enumerate(os.listdir(filedir)):
        if file[0] == ' ' or file[0] == '.':
            continue
        filename = filedir + file
        file_set.append(filename)
        #print(filename)
    return file_set

def readOneFile(filename):
    root = et.parse(filename)
    

    # parse an xml file by name
    mydoc = minidom.parse(filename)
    onethread = []

    emails = mydoc.getElementsByTagName('email')
    for email in emails:


        items = email.getElementsByTagName('sentence')

        string = ''

        for item in items:
            string += item.firstChild.data

        onethread.append(string)

    return onethread
        

def readFiles(filedir):
    files = getFilenames(filedir)
    thread = []
    for file in files:
        thread.append(readOneFile(file))
    return thread, files

