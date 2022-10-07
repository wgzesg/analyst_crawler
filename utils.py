import pickle
import pandas as pd
import json


def pkl_to_df(pkl_file):
    with open(pkl_file, 'rb') as f:
        report_list = pickle.load(f)
    df = pd.DataFrame(columns=[
        'title', 'url', "company", "ticker", 'broker', 'analyst', 'date',
        'content', "level", "order in level"
    ])

    for entry in report_list:
        if len(entry.textual_arguments) == 0:
            continue
        entry.textual_arguments[0].append_to_df(df, entry, 0)
    if df.empty:
        return df
    print("Company:", df['company'].unique()[0])
    print("number of articles", df['title'].nunique())
    print("dates range from", df['date'].min(), "to", df['date'].max())
    print('number of arguments', df['content'].count())
    print('average number of arguments per article',
        df['content'].count() / df['title'].nunique())
    return df

def json_to_df(json_path: str):
    with open(json_path, 'r') as f:
        report_list = json.load(f)
    df = pd.DataFrame(columns=[
        'title', 'url', "company", "ticker", 'broker', 'analyst', 'date',
        'content', "level", "order in level"
    ])

    for entry in report_list:
        entry['textual_arguments'].append_to_df(df, entry, 0)
    if df.empty:
        return df
    print("Company:", df['company'].unique()[0])
    print("number of articles", df['title'].nunique())
    print("dates range from", df['date'].min(), "to", df['date'].max())
    print('number of arguments', df['argument'].count())
    print('average number of arguments per article',
          df['argument'].count() / df['title'].nunique())
    return df
