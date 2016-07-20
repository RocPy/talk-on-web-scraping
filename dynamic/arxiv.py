from bs4 import BeautifulSoup as BS
import requests
import argparse


def run_query(query, type_):
    session = requests.Session()

    # Access base page and get cookies for state
    url = 'http://arxiv.org/search'

    payload = {
        'query': query,
        'searchtype': type_
    }

    response = session.post(url, data=payload)

    soup = BS(response.text, "lxml")

    results = soup.select("div#dlpage dl dt span.list-identifier")
    papers = {}

    for item in results:
        title = item.find('a', {'title': 'Abstract'}).text
        abstract = item.find('a', {'title': 'Abstract'})['href']
        pdf = item.find('a', {'title': 'Download PDF'})['href']\
            if item.find('a', {'title': 'Download PDF'}) else None

        ps = item.find('a', {'title': 'Download PostScript'})['href']\
            if item.find('a', {'title': 'Download PostScript'}) else None

        other = item.find('a', {'title': 'Other formats'})['href']\
            if item.find('a', {'title': 'Other formats'}) else None

        papers[title] = (title, abstract, pdf, ps, other)

    return papers


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query",
                        type=str,
                        nargs="?",
                        default=None,
                        help="enter a search query",
                        required=True,
                        action='store')

    parser.add_argument("-t", "--type",
                        type=str,
                        nargs="?",
                        default=None,
                        help="search type: all, ti, au, abs",
                        required=False,
                        action='store')

    args = parser.parse_args()
    if not args.type:
        args.type = 'all'

    papers = run_query(args.query, args.type)

    for title,info in papers.items():
        print("{0}: {1}".format(title, info[1]))


if __name__ == '__main__':
    main()
