import requests
from bs4 import BeautifulSoup
import json
from html_parser import article_meta_info_parse
from arguments import get_parser
from article_parser import parse_article_keypoints
from tqdm import tqdm

import os

def url_query(url, output_file):
    response = requests.get(url)
    content = (response.text)
    _html = BeautifulSoup(content, "html.parser")
    article_list = []
    success = fail = 0
    for article in tqdm(_html.find_all('article', "analystreportitem")):
        obj = article_meta_info_parse(article)
        points = parse_article_keypoints(obj['article_link'])
        if (len(points) == 0):
            fail += 1
        else:
            success += 1
        obj['arguments'] = points
        article_list.append(obj)

    json_string = json.dumps(article_list)
    with open(output_file, 'w') as f:
        f.write(json_string)

    print("fail:", fail)
    print("success:", success)

def local_query(input_file, output_file, folder=''):
    with open(input_file, 'r') as f:
        report_list = json.load(f)
    print(len(report_list))

    success = fail = 0
    for filename in tqdm(os.listdir(folder)):
        file_path = os.path.join(folder,filename)
        with open(file_path, 'r') as file:
            points = parse_article_keypoints(content=file.read())
            if (len(points) == 0):
                print('failed:', file_path)
                fail += 1
                continue
            success += 1
            for entry in report_list:
                if filename in entry['article_link']:
                    entry['arguments'] = points  

    print("fail:", fail)
    print("success:", success)

    json_string = json.dumps(report_list)
    with open(output_file, 'w') as f:
        f.write(json_string)


if __name__   == '__main__':
    # url = "https://sginvestors.io/sgx/stock/c6l-sia/analyst-report"
    parser = get_parser()
    args = parser.parse_args()
    if (args.folder):
        local_query(args.input, args.out, args.folder)
    elif (args.url):
        url_query(args.url, args.out)
