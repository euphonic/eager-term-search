import pandas as pd
import numpy as np
import csv
import re
import datetime
from multiprocessing.dummy import Pool as ThreadPool

'''
There will be two exclusion lists (one for the other terms that exclude a paper, one for the nano-animals).

One measure list, which excludes lists if it is the only nano term to appear, but not if other nanoterms appear

One list of search terms and dependencies (things that must appear with the search term)

'''
#make a list of the exclusion terms
exclusion_terms = pd.read_excel("exclusion_terms1.xlsx", header = None)
exclusion_terms =[str(i) for i in exclusion_terms[0].tolist()]
#make a list of the nano-organisms to exclude
with open("nano_organism_to_exclude.txt", "r") as myfile:
    nano_organism_to_exclude = []
    for line in myfile:
        line = line.strip("\n").split(";")
        for item in line:
            if item != "":
                nano_organism_to_exclude.append(item.strip())
#if any of these terms appear the patent should be excluded
exclusion_terms = exclusion_terms + nano_organism_to_exclude

#these are the nano-measure terms which are not a sufficient reason to include a paternt
measure_terms = pd.read_excel("measure_terms.xlsx", header = None)
measures =[str(i) for i in measure_terms[0].tolist()]

#this are some of the additional conditions needed for a search term to count
with open("MolEnv_1_in.txt", "r") as myfile:
    for line in myfile:
        Mol1 = line.strip("\n")
with open("MolEnv_R_in.txt", "r") as myfile:
    for line in myfile:
        MolR = line.strip("\n")

conditions = pd.read_excel("search_terms.xlsx")

#function that takes in these lists of terms and outputs a search regex
def organize_text(list_of_terms, islist = False):
    terms = list_of_terms
    if islist:
        pass
    else:
        terms = terms.split(" OR ")
    terms = [str(item).strip('"') for item in terms]
    #there are no middle wild cards so just remove
    terms = [str(item).strip('*') for item in terms]
    terms = [re.sub('\*',"[a-zA-Z]*", item) for item in terms] #internal wildcards replace with regex to match letters
    terms = [r"\b"+item for item in terms]
    terms = "|".join(terms)
    terms = re.compile(terms)
    return terms

nano = r"\bnano"
nano_pattern = re.compile(nano)


measures = organize_text(measures, islist = True)

quantum_terms = organize_text(conditions.iloc[1,0])

self_terms = organize_text(conditions.iloc[2,0])

MolEnv1 = organize_text(Mol1)

MolEnvR = organize_text(MolR)

motor = organize_text(conditions.iloc[3,0])

micro = organize_text(conditions.iloc[4,0])

quasi = organize_text(conditions.iloc[5,0])

biosensor = organize_text(conditions.iloc[6,0])

exclusion_terms = organize_text(exclusion_terms, islist = True)


import os
subdirs = os.listdir("D:/SarahNewParserDev/Full_Database")
paths = [os.path.join("D:/SarahNewParserDev/Full_Database/", item) for item in subdirs]
fields_to_search = ["brf_sum_text.csv", "detail_desc_text.csv", "claim.csv"]
files = []
for path in paths:
    for j in fields_to_search:
        files.append(os.path.join(path, j))
print files
print datetime.datetime.now().time()


def patent_search(file):
	print file
	with open(file, "r") as myfile:
	    patents_identified = []
	    patent_info = []
	    for line in myfile.readlines():
	        line = line.split("\t")
	        patent_id = line[1]
	        text = line[2]
	        match_id = []
	        exclusion = False
	        #search for nanorecord is special because have to exclude nano-terms
	        #find the matches so can check if all of them are nanomeasures
	        nano_terms = re.findall(nano_pattern, text)
	        are_measures = [bool(re.search(measures, item)) for item in nano_terms]
	        if not all(are_measures):
	            #record should be flagged
	            match_id.append("Nano Term")
	        else:
	            pass
	        if bool(re.search(quantum_terms, text)):
	            match_id.append("Quantum Term")
	        if (bool(re.search(self_terms, text)) and bool(re.search(MolEnv1, text))):
	            match_id.append("Self Term")
	        if bool(re.search(motor, text)):
	            match_id.append("Molecular Motor Term")
	        if (bool(re.search(micro, text)) and bool(re.search(MolEnvR, text))) :
	            match_id.append("Micro Term")
	        if (bool(re.search(quasi, text)) and bool(re.search(MolEnv1, text))) :
	            match_id.append("Quasi Term")
	        if (bool(re.search(biosensor, text)) and bool(re.search(MolEnvR, text))):
	            match_id.append("Biosensor Term")
	        if (bool(re.search(biosensor, text)) and bool(re.search(MolEnvR, text))):
	            match_id.append("Biosensor Term")
	        if bool(re.search(exclusion_terms, text)):
	            exclusion = True
	        if match_id:
	            patents_identified.append([patent_id, match_id, exclusion])
	            #patent_info.append([patent_id, text, file])
	    print len(patents_identified)
	    writer = open("patents.csv", 'a')
	    csvwriter = csv.writer(writer, delimiter = '\t')
	    for i in patents_identified:
	        csvwriter.writerow(i)
	    writer.close()

	    #writer = open("patents_info.csv", 'a')
	    #csvwriter = csv.writer(writer, delimiter = '\t')
	    #for i in patent_info:
	    #    csvwriter.writerow(i)
	    #writer.close()
for i in files:
	patent_search(i)