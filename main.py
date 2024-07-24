import requests
from bs4 import BeautifulSoup
import os
from tqdm.rich import tqdm
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Priority": "u=1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}
while True:
    req = requests.get(input("URL:"), headers=headers)

    if req.status_code == 200:
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        img_attr = soup.find_all("img")
        url_list = []
        print("tittle: "+soup.title.string)
        for i in img_attr:
            url_list.append("https:" + i["data-src"])
        k = 0
        if not os.path.exists(soup.title.string):
            os.mkdir(soup.title.string)
        for i in tqdm(url_list):
            try:
                k = k + 1
                r = requests.get(i, headers=headers)
                if r.status_code == 200:
                    open('./' + soup.title.string + '/img' + str(k) + '.png', 'wb').write(r.content)  # 将内容写入图片
                    # print("pic %d done" % k)
                else:
                    print("err")
                del r
            except requests.exceptions.ProxyError:
                print("Sleep !")
                time.sleep(3)
            time.sleep(0.3)
        else:
            print("Done")
    else:
        print("err: "+str(req.status_code))
