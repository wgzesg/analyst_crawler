import requests
from bs4 import BeautifulSoup
import json
from html_parser import article_meta_info_parse
from arguments import get_parser
from test import parse_article_keypoints
from tqdm import tqdm

def query(url, output_file):
    response = requests.get(url)
    content = (response.text)
    _html = BeautifulSoup(content, "html.parser")
    article_list = []
    for article in tqdm(_html.find_all('article', "analystreportitem")):
        obj = article_meta_info_parse(article)
        points = parse_article_keypoints(obj['article_link'])
        obj['arguments'] = points
        article_list.append(obj)

    json_string = json.dumps(article_list)
    with open(output_file, 'w') as f:
        f.write(json_string)



if __name__   == '__main__':
    # url = "https://sginvestors.io/sgx/stock/c6l-sia/analyst-report"
    parser = get_parser()
    args = parser.parse_args()
    print(args)
    query(args.url, args.out)
