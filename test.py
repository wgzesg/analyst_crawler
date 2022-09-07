from lib2to3.pgen2.parse import ParseError
from tkinter import ALL
import requests
from bs4 import BeautifulSoup
import re


ALL_PARSERS = []

def reg_parser(func):
    ALL_PARSERS.append(func)

url = 'https://research.sginvestors.io/2022/05/singapore-airlines-uob-kay-hian-research-2022-05-20.html'

@reg_parser
def parser_div_desc(_html):
    points = []
    filtered = _html.find('div', attrs={'itemprop':'description'}).find('ul').find_all('li')
    for fil in filtered:
        points.append(fil.text)
    return points

# @reg_parser
# def parser_div_article_part(_html):
#     points = []
#     sectores = _html.find_all('div', attrs={'id':re.compile("article-part-\d")})
#     for sector in sectores:
#         filtered = sector.find('ul')
#         if (filtered != None):
#             filtered = filtered.find_all('li')
#         else:
#             continue
#         for pt in filtered:
#             points.append(pt.text)
#     return points

@reg_parser
def parser_sia_uob_kay_hian_research(_html):
    points = []
    title = _html.find('div', class_='research')
    points.append(title.text)

    sectors = _html.find_all('div', attrs={'id':re.compile("article-part-\d")})
    for sector in sectors:
        filtered = sector.find('ul')
        if (filtered != None):
            filtered = filtered.find_all('li')
            for pt in filtered:
                points.append(pt.text)
        filtered = sector.find('h4')
        if filtered != None:
            points.append(filtered.text)

    return points

def parse_article_keypoints(url=None, content=None):
    points = []
    if content is None:
        response = requests.get(url)
        content = (response.text)
    _html = BeautifulSoup(content, "html.parser")
    for ps in ALL_PARSERS:
        try:
            points = ps(_html)
            if len(points) == 0:
                raise ParseError()
            print('parsed with parser', ps)
            break
        except Exception as e:
            # name = url.split('/')[-1]
            # with open('{}'.format(name), 'w') as f:
            #     f.write(content)
            # print(e)
            continue
    return points


# print(parse_article_keypoints(url))
