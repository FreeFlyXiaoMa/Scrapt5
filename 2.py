from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

def getHTMLText(url):
    try:
        kw = {'user-agent': 'chrome/10.0'}
        r = requests.get(url, params=kw)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('error')


def parseHTML(bookinfo, html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.findAll('table', {"width": "100%"})
    for table in tables:
        link = table.div.a['href']
        title = table.div.a.text.strip().replace('\n', '').replace(' ', '')
        people = table.find('span', {'class': 'pl'}).text.strip()
        people = re.findall(r'[0-9]+', people)[0]
        score = table.find('span', {'class': 'rating_nums'}).text.strip()
        detail = table.find('p', {"class": "pl"}).text
        if table.find('span', {"class": "inq"}):
            abstract = table.find('span', {"class": "inq"}).text.strip()
        else:
            abstract = 'no abstract'
        bookinfo.append([title, score, people, detail, abstract, link])
    return bookinfo


def saveInfo(bookinfo, path):
    a = pd.DataFrame(bookinfo, columns=['书籍名称', '豆瓣评分', '评价人数', '书籍信息', '书籍描述', '书籍豆瓣链接'])
    a.to_excel(path, index=False)


def main():
    book = []
    path = r'doubanbook2.xlsx'
    for i in range(10):
        bookinfo = []
        url = 'https://book.douban.com/top250?start='
        url = url + str(i * 25)
        print(url)
        html = getHTMLText(url)
        books = parseHTML(bookinfo, html)
        for i in range(len(books)):
            book.append(books[i])
    saveInfo(book, path)


main()
