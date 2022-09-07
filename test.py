from tkinter import ALL
import requests
from bs4 import BeautifulSoup
import re


ALL_PARSERS = []

def reg_parser(func):
    ALL_PARSERS.append(func)

url = 'https://research.sginvestors.io/2022/06/singapore-aviation-stocks-uob-kay-hian-research-2022-06-21.html'

@reg_parser
def parser_div_desc(_html):
    points = []
    filtered = _html.find('div', attrs={'itemprop':'description'}).find('ul').find_all('li')
    for fil in filtered:
        points.append(fil.text)
    return points

@reg_parser
def parser_div_article_part(_html):
    points = []
    sectores = _html.find_all('div', attrs={'id':re.compile("article-part-\d")})
    for sector in sectores:
        filtered = sector.find('ul')
        if (filtered != None):
            filtered = filtered.find_all('li')
        else:
            continue
        for pt in filtered:
            points.append(pt.text)
    return points


def parser_sia_uob_kay_hian(_html):
    points = []
    sectores = _html.find('div', attrs={'class':'research'}).find_all('h2')
    return points

def parse_article_keypoints(url: str):
    points = []
    response = requests.get(url)
    content = (response.text)
    _html = BeautifulSoup(content, "html.parser")
    for ps in ALL_PARSERS:
        try:
            points = ps(_html)
            break
        except Exception as e:
            name = url.split('/')[-1]
            with open('log/{}.html'.format(name), 'w') as f:
                f.write(content)
            print(e)
    return points


print(parse_article_keypoints(url))
