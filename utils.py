import pandas as pd
import json


def json_to_df(json_path: str):
    with open(json_path, 'r') as f:
        report_list = json.load(f)
    df = pd.DataFrame(columns=[
        'title', 'url', "company", "ticker", 'broker', 'analyst', 'date',
        'argument'
    ])

    for entry in report_list:
        for point in entry['textual_arguments']:
            df = df.append(
                {
                    'title': entry['title'],
                    'url': entry['article_url'],
                    'company': entry['focal_company'],
                    'ticker': entry['ticker'],
                    'broker': entry['broker'],
                    'analyst': entry['analyst'],
                    'date': entry['date'],
                    'argument': point
                },
                ignore_index=True)
    if df.empty:
        return df

    print("Company:", df['company'].unique()[0])
    print("number of articles", df['title'].nunique())
    print("dates range from", df['date'].min(), "to", df['date'].max())
    print('number of arguments', df['arguments'].count())
    print('average number of arguments per article',
          df['arguments'].count() / df['title'].nunique())
    return df
