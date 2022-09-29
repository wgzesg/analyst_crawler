from bs4 import BeautifulSoup
import bs4
from typing import List, Tuple
import os
from tqdm import tqdm
import requests
from ArticleMeta import ArticleMeta
import re
from article_parser import parse_article_keypoints

BASE_URL = 'https://sginvestors.io/sgx/stock/NAME/analyst-report'


def get_all_tickers() -> List[tuple]:
    '''
    Get a list of all companies in SGX

    return :
        List[(str, str)] each tuple is a pair of (company, ticker)
    '''
    url = 'https://sginvestors.io/sgx/stock-listing/alpha'
    tickers = []
    response = requests.get(url)
    content = (response.text)
    _html = BeautifulSoup(content, "html.parser")
    ticker_lists = _html.find_all('div',
                                  attrs={'id': re.compile("stocklist-[a-z]")})
    for list in ticker_lists:
        for stock in list.find_all('li'):
            name = stock.find('a').text
            ticker = stock.find('a').get('href').split('/')[-2]
            tickers.append((name, ticker))
    return tickers


def query_one_company(ticker: str, name: str):
    '''
        Query one company and find all the articles meta info
        input :
            ticker
        return :
            list of ArticleMeta
    '''
    url = BASE_URL.replace('NAME', ticker)
    response = requests.get(url)
    content = (response.text)
    _html = BeautifulSoup(content, "html.parser")
    article_list = []
    for article in tqdm(_html.find_all('article', "analystreportitem")):
        obj = article_meta_info_parse(article, ticker, name)
        article_list.append(obj)
    return article_list


def parse_one_company_articles(article_list: List[ArticleMeta],
                               root_data_folder: str):
    '''
    Parse all the articles for one company
    input : 
        article_list: list of ArticleMeta
        root_data_folder: root folder to store the articles html
    return : 
        list of ArticleMeta with arguments filled
    '''
    if len(article_list) < 1:
        return
    folder = article_list[0].ticker
    folder_path = os.path.join(root_data_folder, folder)
    if not os.path.exists(root_data_folder):
        os.mkdir(root_data_folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    success = fail = 0
    for article in tqdm(article_list):
        points = parse_one_article(article)
        if (len(points) == 0):
            print('failed:', article.article_path)
            fail += 1
            continue
        success += 1
        article.textual_arguments = points
    print("Ticker:", article_list[0].ticker)
    print("fail:", fail)
    print("success:", success)


def parse_one_article(article: ArticleMeta):
    '''
    Parse one single article. Store the html to local if not exist
    input :
        one ArticleMeta
    return :
        one ArticleMeta with arguments filled
    '''
    if not os.path.exists(article.article_path):
        try:
            response = requests.get(article.article_url)
            content = (response.text)
        except:
            print("failed to get:", article.article_url)
            return []
        with open(article.article_path, 'w') as f:
            f.write(content)
    with open(article.article_path, 'r') as file:
        points = parse_article_keypoints(content=file.read())
        points = [p.strip() for p in points]
        return points
    return []


def article_meta_info_parse(article: bs4.element.Tag, ticker: str,
                            company_name: str) -> ArticleMeta:
    broker = article.find('a').find('div', "broker").text.strip()
    report_date = article.find('a').find('div', 'report_date').text.strip()
    analysts = article.find('a').find('div', 'analysts').text.strip()
    title = article.find('a').find('h1', 'title').text.strip()
    link = article.find('a').get('href').strip()
    article_obj = ArticleMeta(
        title, report_date, broker, analysts, link, company_name, ticker,
        "articles/" + ticker + "/" + link.split('/')[-1] + ".html")
    return article_obj
