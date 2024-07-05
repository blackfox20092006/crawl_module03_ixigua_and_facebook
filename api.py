#module
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-default-apps')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--log-level=3')
# chrome_options.add_argument('--headless')
def get_token_user_pass(username, password):
    url = 'https://b-graph.facebook.com/auth/login?email={}&password={}&access_token=6628568379|c1e620fa708a1d5696fb991c1bde5662&method=post'.format(username, password)
    res = requests.get(url).json()
    return res["access_token"]
def crawl_fb(id, token):
    videos = []
        #user or pro5
    url = 'https://graph.facebook.com/{}/videos?type=uploaded&access_token={}'.format(str(id), token)
    res = requests.get(url)
    try:
        if res.json()['data'] == []:
            return 'NoData'
        else:
            for i in res.json()['data']:
                title = i["description"]
                time = i["updated_time"]
                try:
                    comments = i["comments"]["data"]  # list
                except:
                    pass
                watch_link = 'https://www.facebook.com/watch/?v=' + i["id"]
                source_link = i["source"]
                nguoi_dang = i["from"]["name"]
                videos.append(
                    {
                        "tieude": title,
                        "nguoidang": nguoi_dang,
                        "thoigian": time,
                        "binhluan": comments,
                        "linkwatch": watch_link,
                        "linktai": source_link
                    }
                )
            return videos
    except:
        return 'Error'
# print(crawl_fb('100080147624102', 'EAABwzLixnjYBO3jZBDP6ZAEWKKPJxkrCiMToN3TMWZAovwduc9ip3yMbc1MmjZAopDEyWkXB6fyzvuBGBkVORzyldzLpzGQIiklZAd0SEQyqx4bNyHJ0IO0rN7PHA6BTTcTT1Ehz4hSWtal8VpkIr91jcy4ptPZBw8ZBttUYcaZCMETd2bGGzvug81Qkb1EvX3Npgs0ZD'))
def crawl_ixigua(id):
    url = 'https://www.ixigua.com/home/{}?list_entrance=homepage&video_card_type=shortvideo'.format(str(id))
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    end = '已经到底部，没有更多内容了'
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, timeout=10)
        if driver.page_source.find(end) != -1:
            break
    html = driver.page_source
    videos = []
    a = BeautifulSoup(html, 'html.parser')
    lista = a.find_all(attrs={'class': True})
    listb = a.find_all('a')
    for i in lista:
        if i in listb:
            try:
                tmp = BeautifulSoup(str(i), 'html.parser')
                title = tmp.find('a')['title']
                href = tmp.find('a')['href']
                if {
                        'title': title,
                        'link': 'https://www.ixigua.com' + href
                    } not in videos:
                    videos.append(
                        {
                            'title': title,
                            'link': 'https://www.ixigua.com' + href
                        }
                    )
            except:
                pass
    return videos
# print(crawl_ixigua('2208284108405639'))
