import pandas as pd

def search_result_dataframe(result={}):
    header = []
    for f in result["fields"]:
        header.append(f["name"])
    rows = result["rows"]
    return pd.DataFrame(rows, columns=header)
