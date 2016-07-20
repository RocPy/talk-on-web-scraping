from bs4 import BeautifulSoup as BS
import requests

session = requests.Session()

# Access base page and get cookies for state
url = 'https://docs.google.com/forms/d/e/'\
    '1FAIpQLSedTwME7Iohu2mQtdCYUaePIX-FOCzLa-x0p1xUgSd54w6Myg'

response = session.get(url)

soup = BS(response.text, "lxml")

# Extract some per-session data (we assume).
fbzx = soup.find('input', {'name': 'fbzx'})
draft_response = soup.find('input', {'name': 'draftResponse'})

payload = [
    # Name
    ('Contact+information', 'John Q. Pythonista'),
    ('entry.2005620554', 'John Q. Pythonista'),
    # Email
    ('Contact+information', 'jqp@rocpy.org'),
    ('entry.1045781291', 'jqp@rocpy.org'),
    # Address
    ('Contact+information', '221B Baker Street'),
    ('entry.1065046570', '221B Baker Street'),
    # Phone number
    ('Contact+information', '555-2368'),
    ('entry.1166974658', '555-2368'),
    # Comments
    ('Contact+information', 'I am a robot. <beep> <boop>'),
    ('entry.839337160', 'I am a robot. <beep> <boop>'),
    # Important metadata?
    ('fvv', '1'),
    ('draftResponse', draft_response),
    ('pageHistory', '0'),
    ('fbzx', fbzx)
]

response = session.post(url + '/formResponse', data=payload)

print(response.text)
