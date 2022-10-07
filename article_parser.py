from lib2to3.pgen2.parse import ParseError
from logging import root
from tkinter import ALL
import requests
from bs4 import BeautifulSoup
import re

from ArgumentTree import ArgTreeNode


exclude_list = ['\'s Share Price,', '\'s Target Price,', ' Analyst Reports,', ' Dividend History,', 'Announcements,', ' Latest News.']

ALL_PARSERS = []

def reg_parser(func):
    ALL_PARSERS.append(func)

url = 'https://research.sginvestors.io/2016/02/singapore-airlines-ocbc-investment-2016-02-10.html'

def add_list_to_rt(root, ul):
    if len(root.children) == 0:
        for li in ul.find_all('li'):
            if any(s in li.text for s in exclude_list):
                continue
            node = ArgTreeNode(content=li.text, level=2)
            root.add_child(node)
    else:
        for li in ul.find_all('li'):
            if any(s in li.text for s in exclude_list):
                continue
            root.children[-1].add_child(ArgTreeNode(content=li.text))


@reg_parser
def parser_div_desc(_html):
    title = _html.find('div', class_='research').find('h2')
    root = ArgTreeNode(content=title.text, level=0)
    div_lists = _html.find('div', attrs={'itemprop':'description'})
    for fil in div_lists:
        if fil.name == 'h4':
            node = ArgTreeNode(content=fil.text)
            root.add_child(node)
        elif fil.name == 'ul' or fil.name == 'ol':
            add_list_to_rt(root, fil)
    return [root]

@reg_parser
def parser_article_id(_html):
    title = _html.find('div', class_='research').find('h2')
    root = ArgTreeNode(content=title.text, level=0)
    sectors = _html.find_all('div', attrs={'id':re.compile("article-part-\d")})
    if len(sectors) == 0:
        return []
    for sector in sectors:
        main_pt = sector.find(['h3', 'h4'])
        support = sector.find(['ul', 'ol'])
        if main_pt:
            node = ArgTreeNode(main_pt.text)
            root.add_child(node)
        elif support:
            add_list_to_rt(root, support)
    return [root]

@reg_parser
def parser_no_article_id(_html):
    research_blk = _html.find('div', class_='research')
    title = research_blk.find('h2')
    root = ArgTreeNode(content=title.text, level=0)

    for sector in research_blk:
        if sector.name == 'h4' or sector.name == 'h3':
            node = ArgTreeNode(content=sector.text)
            root.add_child(node)
        elif sector.name == 'ul' or sector.name == 'ol':
            add_list_to_rt(root, sector)
    return [root]

@reg_parser
def parser_post_body_id(_html):
    sectors = _html.find('div', attrs={'id':re.compile("post-body-\d")})
    title = sectors.find('h3')
    root = ArgTreeNode(content=title.text, level=0)
    for sector in sectors:
        if sector.name == 'h4':
            node = ArgTreeNode(content=sector.text)
            root.add_child(node)
        elif sector.name == 'div':
            ul = sector.find(['ul', 'ol'])
            if ul:
                add_list_to_rt(root, ul)
    return [root]

@reg_parser
def parser_post_body_id_many_researches(_html):
    sectors = _html.find('div', attrs={'id':re.compile("post-body-\d")})
    title = sectors.find('h2')
    print(title)
    root = ArgTreeNode(content=title.text, level=0)
    for sector in sectors:
        if sector.name == 'h4':
            node = ArgTreeNode(content=sector.text)
            root.add_child(node)
        elif sector.name == 'div':
            ul = sector.find(['ul', 'ol'])
            if ul:
                add_list_to_rt(root, ul)
    return [root]

# @reg_parser
# def parser_div_post_body(_html):
#     points = []
#     sectores = _html.find('div', attrs={'id':re.compile("post-body-\d")}).find_all('div')
#     for sector in sectores:
#         # print(sector.text, '\n\n\n')
#         filtered = sector.find('ul')
#         if (filtered != None):
#             filtered = filtered.find_all('li')
#         else:
#             if (len(sector.text) > 35):
#                 points.append(sector.text)
#             continue
#         for pt in filtered:
#             points.append(pt.text)
#     return points

def parse_article_keypoints(content=None, folder=''):
    points = []
    _html = BeautifulSoup(content, "html.parser")
    for ps in ALL_PARSERS:
        try:
            print(ps.__name__)
            points = ps(_html)
            if len(points) == 0 or len(points[0].children) == 0:
                raise ParseError()
            print("parsed with ", ps.__name__)
            break
        except Exception as e:
            continue
    return points


# print(parse_article_keypoints(url))
