import requests
from bs4 import BeautifulSoup


def getHTMLText(i):
    try:
        url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-' + str(i)
        r = requests.get(url=url, timeout=30)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
    except:
        print('响应失败')
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def getbookname(soup):
    lis = soup.html.body.contents[21].contents[7].contents[9].contents[7].contents
    book_list = []
    for i in range(20):
        des = lis[2 * i + 1].contents[3].a.img['alt']
        if '(' in des:
            book_list.append(des.split('(')[0])
        elif '（' in des:
            book_list.append(des.split('（')[0])
        else:
            book_list.append(des)
    return book_list


def getauthor(soup):
    lis = soup.html.body.contents[21].contents[7].contents[9].contents[7].contents
    author_list = []
    for i in range(20):
        des = lis[2 * i + 1].contents[9].a.string
        author_list.append(des)
    return author_list


def getpress(soup):
    lis = soup.html.body.contents[21].contents[7].contents[9].contents[7].contents
    press_list = []
    for i in range(20):
        des = lis[2 * i + 1].contents[11].a.string
        press_list.append(des)
    return press_list


def getprice(soup):
    lis = soup.html.body.contents[21].contents[7].contents[9].contents[7].contents
    price_list = []
    for i in range(20):
        des = lis[2 * i + 1].contents[13].p.span.string
        price_list.append(des)
    return price_list


def getallinfo():
    book_list = []
    author_list = []
    press_list = []
    for i in range(1, 11):
        soup = getHTMLText(i)
        book = getbookname(soup)
        author = getauthor(soup)
        press = getpress(soup)
        for j in range(20):
            if book[j] not in book_list:
                book_list.append(book[j])
                author_list.append(author[j])
                press_list.append(press[j])
    return book_list, author_list, press_list
