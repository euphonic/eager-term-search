
import pandas as pd
import numpy as np
import csv
import difflib
from tqdm import tqdm
tqdm.pandas(desc="Fuzzy Match Progress")

patent_assignee_mapping=pd.read_csv("./patent_assignee/patent_assignee.tsv", sep="\t", low_memory=False)

patent_assignee_mapping.head()
patent_results=pd.read_csv("../Phase-1-Search-Term/green-technology/all-patent-green-terms-searches.csv", 
                           dtype={'Emerging low carbon-Additional energy sources':bool,
                                  'Emerging low carbon-All-purpose':bool, 'Emerging low carbon-Alternative fuel':bool,
                                  'Emerging low carbon-Alternative fuel vehicle':bool, 'Emerging low carbon-Battery':bool,
                                  'Emerging low carbon-Building technologies':bool,'Emerging low carbon-Carbon capture & storage':bool,
                                  'Emerging low carbon-Electrochemical processes':bool,'Emerging low carbon-Energy management':bool,
                                  'Environmental-Air pollution':bool,'Environmental-All-purpose':bool,
                                  'Environmental-Biological treatment':bool,'Environmental-Contaminated land reclamation & remediation':bool,
                                  '"Environmental-Environmental monitoring':bool,' instrumentation and analysis"':bool,
                                  'Environmental-Marine pollution control':bool,'Environmental-Noise & vibration control':bool,
                                  'Environmental-Recovery and recycling':bool,'Environmental-Waste management':bool,
                                  'Environmental-Water supply & was te water treatment':bool,'General-':bool,
                                  'Renewable energy-All-purpose':bool,'Renewable energy-Biomass':bool,
                                  'Renewable energy-Geothermal':bool,'Renewable energy-Photovoltaic & solar':bool,
                                  'Renewable energy-Wave & Tidal':bool,'Renewable energy-Wind':bool,'user_id': str})

# Lookup Assignee details from PV database
selected_patents=patent_results[patent_results.iloc[:,:26].any(axis=1)]
selected_patents.reset_index(drop=True, inplace=True)
selected_ids= [str(x) for x in selected_patents.id.tolist()]

selected_patent_assignees=patent_assignee_mapping[patent_assignee_mapping.patent_id.isin(selected_ids)]

assignee_details=pd.read_csv("./assignee/assignee.tsv", sep="\t", low_memory=False, encoding='latin-1')
assignee_details.head()

selected_patent_assignee_details = pd.merge(
    selected_patent_assignees, assignee_details, how="left", left_on="assignee_id", right_on="id")
selected_patent_assignee_details.shape
missing_ids=set(selected_ids).difference(set(selected_patent_assignees.patent_id))


selected_patent_assignee_details.to_csv("green_organizations.csv", index=False)

# Lookup assignee details from SAM database
sam_entities=pd.read_csv("./sam-entities.csv", encoding="latin-1")
sam_entities=sam_entities.assign(compare_lbn=sam_entities.LEGAL_BUSINESS_NAME.str.lower())
sam_entities=sam_entities.assign(compare_dban=sam_entities.DBA_NAME.str.lower())

len(sam_entities.compare_lbn.unique())

sam_small_businesses=sam_entities[(~pd.isnull(sam_entities.NAICS_CODE_COUNTER > 0) &
              sam_entities.NAICS_CODES.str.contains("Y"))]


green_organizations=green_organizations.assign(compare_organization=green_organizations.organization.str.lower())

green_sam=pd.merge(left=green_organizations, right=sam_entities, how="inner",left_on="compare_organization", right_on="compare_lbn")

len(green_sam[(green_sam.NAICS_CODE_COUNTER > 0) & (
    green_sam.NAICS_CODES.str.contains("Y"))].compare_organization.unique())

set([type(i) for i in sam_entities.compare_lbn.tolist()])
sam_entities.loc[:,"compare_lbn"]=sam_entities.compare_lbn.astype(str)


def match_closest_sam(x, sam_rows):
    matches=difflib.get_close_matches(x, sam_rows['compare_lbn'],1)
    if len(matches)>0:
        return matches[0]
    else:
        None
    

match_closest_sam("test", sam_entities)


green_organizations['compare_organization'] = green_organizations['compare_organization'].progress_apply(
    match_closest_sam, args=(sam_entities,))


green_sam=pd.merge(left=green_organizations, right=sam_entities, how="inner",left_on="compare_organization", right_on="compare_lbn")
green_organizations=pd.read_csv("./green_organizations.csv", encoding="latin-1")
