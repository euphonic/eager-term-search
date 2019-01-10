# coding: utf-8

# In[56]:

import pandas as pd
import numpy as np
import csv
import re
import datetime
from multiprocessing.dummy import Pool as ThreadPool

import pprint

# from tqdm import tqdm
# tqdm.pandas(desc="progress")


'''
There will be two exclusion lists (one for the other terms that exclude a paper, one for the nano-animals).

One measure list, which excludes lists if it is the only nano term to appear, but not if other nanoterms appear

One list of search terms and dependencies (things that must appear with the search term)

'''
# make a list of the exclusion terms

exclusion_terms = pd.read_excel("nanotech/exclusion_terms1.xlsx", header=None)
exclusion_terms = [str(i) for i in exclusion_terms[0].tolist()]

# In[3]:

with open("nanotech/nano_organism_to_exclude.txt", "r") as myfile:
    nano_organism_to_exclude = []
    for line in myfile:
        line = line.strip("\n").split(";")
        for item in line:
            if item != "":
                nano_organism_to_exclude.append(item.strip())
# if any of these terms appear the patent should be excluded
exclusion_terms = exclusion_terms + nano_organism_to_exclude

# these are the nano-measure terms which are not a sufficient reason to
# include a paternt
measure_terms = pd.read_excel("nanotech/measure_terms.xlsx", header=None)
measures = [str(i) for i in measure_terms[0].tolist()]

# this are some of the additional conditions needed for a search term to count
with open("nanotech/MolEnv_1_in.txt", "r") as myfile:
    for line in myfile:
        Mol1 = line.strip("\n")
with open("nanotech/MolEnv_R_in.txt", "r") as myfile:
    for line in myfile:
        MolR = line.strip("\n")

conditions = pd.read_excel("nanotech/search_terms.xlsx")


# function that takes in these lists of terms and outputs a search regex

def organize_text(list_of_terms, islist=False):
    terms = list_of_terms
    if islist:
        pass
    else:
        terms = terms.split(" OR ")
    terms = [str(item).strip('"') for item in terms]
    # there are no middle wild cards so just remove
    terms = [str(item).strip('*') for item in terms]
    # internal wildcards replace with regex to match letters
    terms = [re.sub('\*', "[a-zA-Z]*", item) for item in terms]
    terms = [r"\b" + item for item in terms]
    terms = "|".join(terms)
    terms = re.compile(terms, re.IGNORECASE)
    return terms


nano = r"\bnano[^\s]*"
nano_pattern = re.compile(nano)

measures = organize_text(measures, islist=True)
quantum_terms = organize_text(conditions.iloc[1, 0])
self_terms = organize_text(conditions.iloc[2, 0])
MolEnv1 = organize_text(Mol1)
MolEnvR = organize_text(MolR)
motor = organize_text(conditions.iloc[3, 0])
micro = organize_text(conditions.iloc[4, 0])
quasi = organize_text(conditions.iloc[5, 0])
biosensor = organize_text(conditions.iloc[6, 0])
exclusion_terms = organize_text(exclusion_terms, islist=True)


# This essentially processes one record at a time and returns a list of
# booleans indicating existence of search terms


def search_for_terms(row, nano_pattern, measures, quantum_terms, self_terms, motor, micro,
                     quasi, biosensor, MolEnv1, MolEnvR, exclusion_terms):
    match_id = {"Nano Term": False, "Quantum Term": False, "Self Term": False, "Molecular Motor Term": False,
                "Micro Term": False,
                "Quasi Term": False, "Biosensor Term": False, "Biosensor 2 Term": False, "exclusion": False,
                "measure_exclusion": False, "selection": False}

    # search for nanorecord is special because have to exclude nano-terms
    # find the matches so can check if all of them are nanomeasures
    nano_terms = re.findall(nano_pattern, row.text)
    are_measures = [bool(re.search(measures, item)) for item in nano_terms]
    final_inclusion = False
    if bool(re.search(quantum_terms, row.text)):
        match_id["Quantum Term"] = True
        final_inclusion = True
    if (bool(re.search(self_terms, row.text)) and bool(re.search(MolEnv1, row.text))):
        match_id["Self Term"] = True
        final_inclusion = True
    if bool(re.search(motor, row.text)):
        match_id["Molecular Motor Term"] = True
        final_inclusion = True
    if (bool(re.search(micro, row.text)) and bool(re.search(MolEnvR, row.text))):
        match_id["Micro Term"] = True
        final_inclusion = True
    if (bool(re.search(quasi, row.text)) and bool(re.search(MolEnv1, row.text))):
        match_id["Quasi Term"] = True
        final_inclusion = True
    if (bool(re.search(biosensor, row.text)) and bool(re.search(MolEnvR, row.text))):
        match_id["Biosensor Term"] = True
        final_inclusion = True
    if (bool(re.search(biosensor, row.text)) and bool(re.search(MolEnvR, row.text))):
        match_id["Biosensor Term"] = True
        final_inclusion = True
    if bool(re.search(exclusion_terms, row.text)):
        match_id["exclusion"] = True
    if all(are_measures) and len(are_measures) > 0:
        match_id["measure_exclusion"] = True
    elif len(are_measures) > 0:
        match_id["Nano Term"] = True
        final_inclusion = True
    match_id["selection"] = final_inclusion and not match_id["exclusion"]
    return (pd.Series(match_id))


# This function processes one file at a time and appends the patents to
# the same csv file


def patent_search(file, field_list, nano_pattern, measures, quantum_terms, self_terms, motor, micro,
                  quasi, biosensor, MolEnv1, MolEnvR, exclusion_terms):
    current_file_data = pd.read_csv(file, sep="\t")
    current_file_data.assign(
        text=current_file_data[field_list].apply(lambda x: ' '.join(x.dropna().values.tolist()), axis=1))
    current_file_results = current_file_data.join(current_file_data.apply(search_for_terms, axis=1,
                                                                          args=(
                                                                              field_list, nano_pattern, measures,
                                                                              quantum_terms, self_terms, motor, micro,
                                                                              quasi, biosensor, MolEnv1, MolEnvR,
                                                                              exclusion_terms)))
    current_file_results.to_csv("patents.csv", index=False, mode="a")


fields_to_search = ["abstract", "title"]
files = ["titles_abstracts_20170307.tsv"]
pprint.pprint(files)
pprint.pprint(datetime.datetime.now().time())

for i in files:
    patent_search(i, fields_to_search, nano_pattern, measures, quantum_terms, self_terms, motor, micro,
                  quasi, biosensor, MolEnv1, MolEnvR, exclusion_terms)
