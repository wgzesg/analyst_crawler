import json
from html_parser import get_all_tickers, query_one_company, parse_one_company_articles
from arguments import get_parser
import os
import pandas as pd
import pickle

from utils import json_to_df, pkl_to_df

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    ticker_list = get_all_tickers()

    if not os.path.exists('data'):
        os.mkdir('data')
        os.mkdir('data/parsed')
        os.mkdir('data/raw')

    full_df = pd.DataFrame()

    for company in ticker_list:
        name, ticker = company
        article_list = query_one_company(ticker, name)
        with open('data/raw/' + ticker + '.json', 'w') as f:
            content = json.dumps(article_list,
                                 default=lambda o: o.toJson(),
                                 indent=4)
            f.write(content)
        parse_one_company_articles(article_list, args.folder)
        with open('data/parsed/' + ticker + '_parsed.json', 'w') as f:
            content = json.dumps(article_list,
                                 default=lambda o: o.toJson(),
                                 indent=4)
            f.write(content)
        pickle.dump(article_list, open('data/parsed/' + ticker + '_parsed.pkl', 'wb'))
        # df = json_to_df('data/parsed/' + ticker + '_parsed.json')
        df = pkl_to_df('data/parsed/' + ticker + '_parsed.pkl')
        full_df = pd.concat([full_df, df], ignore_index=True)
    full_df.to_csv('full.csv', index=False)
