import bs4
from typing import Dict

"""
Article meta info is stored as follwoing:

    article_obj_json = {
        "title": "Growing strong",
        "date": "2011-10-01",
        "broker": "DBS",
        "analyst": "Ryan Lee",
        "article_link": "https://sginvestors.io/analysts/research/xxxx"
    }
"""

def article_meta_info_parse(article: bs4.element.Tag) -> Dict:
    broker = article.find('a').find('div', "broker").text
    report_date = article.find('a').find('div', 'report_date').text
    analysts = article.find('a').find('div', 'analysts').text
    title = article.find('a').find('h1', 'title').text
    link = article.find('a').get('href')

    article_obj_json = {
        "title": title,
        "date": report_date,
        "broker": broker,
        "analyst": analysts,
        "article_link": link,
        "arguments": []
    }

    return article_obj_json
