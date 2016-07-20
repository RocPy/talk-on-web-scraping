from bs4 import BeautifulSoup as BS
import requests


def walk(tree):
    for tag in tree.descendants:
        print(type(tag))


def find_town_reports(tree):
    towns = {}

    # Use a CSS selector to pull out a sub-section of the HTML document and
    # then convert that into another 'soup' object.
    sub_tree = tree.select('div.field-item')[0]

    # Use BS's procedural method for extracting tags.
    for tag in sub_tree.find_all("p", {"style": "text-align: center;"}):
        towns[tag.text] = []

    # Iterate over all the tags to find the ones relative to each town heading
    # and add it to the 'towns' dict for each town.
    current_town = None
    title = None
    desc = None

    for tag in sub_tree.select("p"):

        if tag.text in towns:
            current_town = tag.text
            continue

        if tag.next_element.next_element.name == 'strong':
            title = tag.text
            desc = []
            towns[current_town].append((title, desc))
        else:
            desc.append(tag.text)

    return towns


def main():
    url = "https://www2.monroecounty.gov/sheriff-ZoneA-Weekly-CR"
    response = requests.get(url)

    soup = BS(response.text, "lxml")

    reports = find_town_reports(soup)

    for town, rep_list in reports.items():
        print("{0} {1} {0}".format("*" * 4, town))

        for rep in rep_list:
            print("+ {0}".format(rep[0]))
            print("\t {0}".format(*rep[1]))

        print()

if __name__ == '__main__':
    main()
