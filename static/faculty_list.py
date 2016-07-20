from bs4 import BeautifulSoup as BS
import requests


def find_faculty(tree):
    rows = tree.select("section.directory div.row")
    directory = {}

    for person in rows:
        name = person.find('h4').text
        img_url = person.find('img').text if person.find('img') else None

        attr = {'class': 'small-8 medium-9 columns'}
        contact = person.find('div', attr).text \
            if person.find('div', attr) else None

        attr = {'class': 'small-12 medium-9 columns'}
        interests = person.find('div', attr).text \
            if person.find('div', attr) else None

        directory[name] = (img_url, contact, interests)

    return directory


def main():
    url = "http://www.pas.rochester.edu/people/faculty/index.html"
    response = requests.get(url)
    soup = BS(response.text, "lxml")
    faculty_list = find_faculty(soup)

    for name in faculty_list:
        print(name)


if __name__ == "__main__":
    main()
