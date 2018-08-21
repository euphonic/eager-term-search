# Imports
import json
import re
import pandas as pd
import time
from tqdm import tqdm
import pprint
# helper function to print progress of apply (works well in linux /
# powershell in windows)


def logged_apply(g, func, *args, **kwargs):
    step_percentage = 100. / len(g)
    import sys
    sys.stdout.write('apply progress:   0%')
    sys.stdout.flush()

    def logging_decorator(func):
        def wrapper(*args, **kwargs):
            progress = wrapper.count * step_percentage
            sys.stdout.write('\033[D \033[D' * 4 +
                             format(progress, '3.0f') + '%')
            sys.stdout.flush()
            wrapper.count += 1
            return func(*args, **kwargs)
        wrapper.count = 0
        return wrapper

    logged_func = logging_decorator(func)
    res = g.apply(logged_func, *args, **kwargs)
    sys.stdout.write('\033[D \033[D' * 4 + format(100., '3.0f') + '%' + '\n')
    sys.stdout.flush()
    return res

# Compile the regular expression first


def build_re(terms, regexps):
    regexps["joinwith"] = terms["joinwith"]
    regexps["clauses"] = []
    for clause in terms["clauses"]:
        found_flag = False
        if isinstance(clause, dict):
            current_reg = build_re(clause, {})
        else:
            current_expression = clause.replace("*", ".*")
            current_expression = r".*" + current_expression + r".*"
            current_reg = re.compile(current_expression, re.IGNORECASE)
        regexps["clauses"].append(current_reg)
    return regexps

######################

# Below recursive function will look return TRUE / FALSE based on regular
# expression matching of search term json


def search_pattern(string, terms):
    for clause in terms["clauses"]:
        found_flag = False
        # If current element is a dictionary, indicates there is a nested
        # condition
        if isinstance(clause, dict):
            found_flag = search_pattern(string, clause)
        # If not simple pattern checking
        else:
            try:
                if clause.match(string) is not None:
                    found_flag = True
                else:
                    found_flag = False
            except:
                print(clause)
                print(string)
        # For OR condition, its sufficient that only one pattern has to match
        if terms["joinwith"] == "OR" and found_flag == True:
            break
        # For AND condition, even one match failure leads to not matching the
        # set of clauses
        if terms["joinwith"] == "AND" and found_flag == False:
            break
    return found_flag


# Given a dataframe row and set of patterns returns a series of boolean values indicating if the patterns were found
# Called on dataframe using apply function
def search_current_row(row, patterns):
    match_results = {}
    for pattern in pattern_with_regexps:
        key = pattern["category"]
        match_results[key] = search_pattern(
            row.title + row.abstract, pattern["terms"])
    return pd.Series(match_results)

# Reading only part of the file now, once we are sure to proceed we can run this on complete file
# use "r" to treat strings as such i.e ignore backslash

start_time = time.time()

patent_data = pd.read_csv(r"../titles_abstracts_20170307.tsv", sep="\t", nrows=1000)
print("--- %s seconds ---" % (time.time() - start_time))
with open('./synthetic-biology/synbio_terms.json') as data_file:
    patterns = json.load(data_file)

pattern_with_regexps = []
for pattern in patterns:
    pattern_with_regexps.append({"id": pattern["id"], "category": pattern[
                                "category"], "terms": build_re(pattern["terms"], {})})
pprint.pprint(pattern_with_regexps)
# # "Loop" through each row and look for patterns
# tqdm.pandas(desc="")
# match_results = patent_data.progress_apply(
#     search_current_row, 1, args=(patterns,))
# result_frame = patent_data.join(match_results)
# # ## Write all fields leaving out title and abstract
# result_frame[result_frame.columns.difference(['title', 'abstract'])].to_csv(
#     "green_patent_results.csv", index=False)
