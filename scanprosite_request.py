"""
Search for signature sequences from the given protein database
by requesting from the ScanProsite Tool.

"""
import requests
from bs4 import BeautifulSoup


def rrrrequest(xulie_string):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'multipart/form-data; boundary=---------------------------391788291618789564242203921715',
        'Origin': 'https://prosite.expasy.org',
        'Connection': 'keep-alive',
        'Referer': 'https://prosite.expasy.org/scanprosite/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    # Replace the usercode 8RbOVfwHgB with your own database code

    data = f'-----------------------------391788291618789564242203921715\r\nContent-Disposition: form-data; name="meta"\r\n\r\nopt3\r\n-----------------------------391788291618789564242203921715\r\nContent-Disposition: form-data; name="meta3_protein"\r\n\r\nopt2\r\n-----------------------------391788291618789564242203921715\r\nContent-Disposition: form-data; name="userdbcode"\r\n\r\nSjHGGVFjkD\r\n-----------------------------391788291618789564242203921715\r\nContent-Disposition: form-data; name="sig"\r\n\r\n{xulie_string}\r\n-----------------------------391788291618789564242203921715\r\nContent-Disposition: form-data; name="output"\r\n\r\ntabular\r\n-----------------------------391788291618789564242203921715\r\nContent-Disposition: form-data; name="maxhits"\r\n\r\n10000\r\n-----------------------------391788291618789564242203921715\r\nContent-Disposition: form-data; name="submit"\r\n\r\nSTART THE SCAN\r\n-----------------------------391788291618789564242203921715--\r\n'

    response = requests.post('https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi', headers=headers, data=data)

    soup = BeautifulSoup(response.text, "html.parser")

    pres = soup.find_all('pre')
    retext = pres[0].text
    remarks = retext.split('\n')[2]
    tables_text = retext.split('\n')[4:]
    tables_list = []
    for line in tables_text[5:]:
        if len(line) > 5:
            tables_list.append(line)
    hits = len(tables_list)
    return remarks, hits, tables_list


# For debugging

if __name__ == '__main__':
    remark, hits, table = rrrrequest('L-x-L-P-x-R')
    print(remark, hits)
    for i in table:
        print(i)
