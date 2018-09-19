
# coding: utf-8

import pandas as pd
import numpy as np
import csv
import difflib
from tqdm import tqdm
tqdm.pandas(desc="Fuzzy Match Progress")

sam_entities = pd.read_csv("./sam-entities.csv", encoding="latin-1")


sam_entities = sam_entities.assign(
    compare_lbn=sam_entities.LEGAL_BUSINESS_NAME.str.lower())
sam_entities = sam_entities.assign(
    compare_dban=sam_entities.DBA_NAME.str.lower())
sam_entities.loc[:, "compare_lbn"] = sam_entities.compare_lbn.astype(str)

green_organizations = pd.read_csv(
    "./green_organizations.csv", encoding="latin-1")
green_organizations = green_organizations.assign(
    compare_organization=green_organizations.organization.str.lower())
green_organizations.loc[
    :, "compare_organization"] = green_organizations.compare_organization.astype(str)


def match_closest_sam(x, sam_rows):
    matches = difflib.get_close_matches(x, sam_rows['compare_lbn'], 1)
    if len(matches) > 0:
        return matches[0]
    else:
        None

fuzzy_green_organizations = green_organizations.assign(closest_sam_organization=green_organizations['compare_organization'].progress_apply(
    match_closest_sam, args=(sam_entities,)))

fuzzy_green_organizations.to_csv(
    "./fuzzy_green_organizations.csv", index=False)
# In[ ]:

fuzzy_green_sam = pd.merge(left=green_organizations, right=sam_entities,
                           how="inner", left_on="closest_sam_organization", right_on="compare_lbn")

fuzzy_green_organizations.to_csv(
    "./fuzzy_green_sam.csv", index=False)

print(len(fuzzy_green_sam.compare_organization.unique()))

print(len(fuzzy_green_sam[(fuzzy_green_sam.NAICS_CODE_COUNTER > 0) & (
    fuzzy_green_sam.NAICS_CODES.str.contains("Y"))].compare_organization.unique()))
