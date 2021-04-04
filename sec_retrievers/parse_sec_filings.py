from sec_edgar_retrievers import edgar_downloader as edl
from bs4 import BeautifulSoup
import sys,os

file_type = "10-K"
ticker = "RPLA"
html, txt = edl.download_latest_filing(file_type,ticker)

myfile = open(html)
contents = myfile.read()
myfile.close()

soup = BeautifulSoup(contents, features='lxml')
VALID_TAGS = ['div', 'p']

for tag in soup.findAll('p'):
        if tag.name not in VALID_TAGS:
            tag.replaceWith(tag.renderContents())
        for attribute in ["class", "id", "name", "style", "td","tr"]:
            del tag[attribute]
        if tag.parent.name == 'p' and tag.name not in ["script", "table"]:
            tag.getText()
soup_out = soup.renderContents()

dir = os.getcwd() + f'/output/{ticker}/'
if not os.path.isdir(dir):
    os.mkdir(dir)
outp = dir + 'soup.txt'
f = open(outp, 'wb')
f.write(soup_out)
f.close()