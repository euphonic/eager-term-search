patent_assignee_mapping = pd.read_csv(
    "./patent_assignee/patent_assignee.tsv", sep="\t", low_memory=False)

patent_results = pd.read_csv(
    "synbio_patent_results.csv",
    dtype={
        'Bio Tech/Engg': bool,
        'Cell biology': bool,
        'Chemical': bool,
        'General': bool,
        'Genetics': bool,
        'Nano technology': bool,
        'id': str
    })

patent_results.id = patent_results.id.astype(str)
patent_results = patent_results[patent_results.id != "nan"]

patent_assignee_mapping.assignee_id = patent_assignee_mapping.assignee_id.astype(str)
patent_assignee_mapping.patent_id = patent_assignee_mapping.patent_id.astype(str)

patent_assignee_mapping = patent_assignee_mapping[
    patent_assignee_mapping.assignee_id != "nan"]
patent_assignee_mapping = patent_assignee_mapping[
    patent_assignee_mapping.patent_id != "nan"]

selected_patents=patent_results[patent_results.iloc[:,:6].any(axis=1)]

selected_patent_details = pd.merge(
    selected_patents,
    patent_assignee_mapping,
    how="left",
    left_on="id",
    right_on="patent_id")