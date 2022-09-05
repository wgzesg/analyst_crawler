import requests
from bs4 import BeautifulSoup
import json
from html_parser import article_meta_info_parse

url = 'https://sginvestors.io/analysts/research/2022/03/singapore-airlines-cgs-cimb-research-2022-03-17'
def parse_article_keypoints(url):
    points = []
    try:
        response = requests.get(url)
        content = (response.text)
        _html = BeautifulSoup(content, "html.parser")

        filtered = _html.find('div', attrs={'itemprop':'description'}).find('ul').find_all('li')
        for fil in filtered:
            points.append(fil.text)
    except Exception as e:
        name = url.split('/')[-1]
        with open('log/{}.html'.format(name), 'w') as f:
            f.write(content)
        print(e)
    return points
# article_list = []
# for article in _html.find_all('article', "analystreportitem"):
#     obj = article_meta_info_parse(article)
#     article_list.append(obj)

# # json_string = json.dumps(article_list)
# with open('file.html', 'w') as f:
#     f.write(content)

