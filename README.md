# Phase 1 - Searching for terms
## Search terms input file
| Category 		    | File Name 																|
|-------------------|---------------------------------------------------------------------------|
| green technology  | Phase-1-Search-Term/green-technology/green_terms.json                     |
| synthetic biology | Phase-1-Search-Term/synthetic-biology/synbio_terms.json                   |
| nanotech          | Phase-1-Search-Term/nano-technology/nanotech/nano_organism_to_exclude.txt |
|                   | Phase-1-Search-Term/nano-technology/nanotech/MolEnv_1_in.txt              |
|                   | Phase-1-Search-Term/nano-technology/nanotech/MolEnv_R_in.txt              |
|                   | Phase-1-Search-Term/nano-technology/nanotech/search_terms.xlsx            |


## Search scripts  
| Category          | File Path                                                        |
|-------------------|------------------------------------------------------------------|
| green technology  | Phase-1-Search-Term/search-for-terms.py                          |
| synthetic biology | Phase-1-Search-Term/synthetic-biology/search-for-terms-synbio.py |
| nano tech         | Phase-1-Search-Term/nano-technology/updated-nano-search.py       |

The scripts for green & synbio are very similar (copies of each other with small changes)  


## Output of Phase 1 (Patents matching search terms)  
| Category          | File Path                                                        |
|-------------------|------------------------------------------------------------------|
| green technology  | Phase-1-Search-Term/green-technology/green_utility_patents.csv   |
| synthetic biology | Phase-1-Search-Term/synthetic-biology/synbio_utility_patents.csv |
| nano tech         | Phase-1-Search-Term/nano-technology/nano_utility_patents.csv     |


# Phase 2 - Assignee Detail  

## Script


## Output of  Phase 2 - Step 1 (Getting list of assignees)  
| Category          | File Path                                               |
|-------------------|---------------------------------------------------------|
| green technology  | Phase-2-Assignee-Extraction/us_green_organizations.csv  |
| synthetic biology | Phase-2-Assignee-Extraction/us_synbio_organizations.csv |
| nano tech         | Phase-2-Assignee-Extraction/us_nano_organizations.csv   |