import json
from html_parser import get_all_tickers, query_one_company, parse_one_company_articles
from arguments import get_parser
import os

from utils import json_to_df

if __name__ == '__main__':
    # url = "https://sginvestors.io/sgx/stock/c6l-sia/analyst-report"
    parser = get_parser()
    args = parser.parse_args()
    ticker_list = get_all_tickers()

    if not os.path.exists('data'):
        os.mkdir('data')
        os.mkdir('data/parsed')
        os.mkdir('data/raw')

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
        json_to_df('data/parsed/' + ticker + '_parsed.json')
