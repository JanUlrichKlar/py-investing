
import requests
from lxml import html
from bs4 import BeautifulSoup




url_base = 'https://www.finanzen.net/historische-kurse/daimler'

r = requests.post(url_base)

soup = BeautifulSoup(r.content, 'lxml')

tab = soup.find('form', action='/historische-kurse/' + 'daimler')


print(tab)