from bs4 import BeautifulSoup
from japanese_bunkatu import BunsetsuWakachi
from japanese_sentiment import JapaneseSentimentAnalyzer
import requests

def get_kashi(url):
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html.parser")

    div = soup.find("div", class_="hiragana")

    for tag in div.findAll(class_="rt"):
        tag.decompose()
    
    kashi = div.get_text().split("\n")
    kashi2 = []

    for i in kashi:
        i = i.replace("\r","")
        i = i.replace(" ","")

        if i != "":
            kashi2.append(i)
    
    return kashi2

def shori_kashi(url):
    kashi = get_kashi(url)
    bunsetu = BunsetsuWakachi()
    bunsetu_kashi = []
    for i in kashi:
        bunsetu_kashi.append(bunsetu.bunsetsu_wakachi(i))

    return bunsetu_kashi

def average_tuples(tuple_list):
    # タプルリストの各要素の平均を計算する
    num_tuples = len(tuple_list)
    num_elements = len(tuple_list[0])
    
    averages = [sum(elements) / num_tuples for elements in zip(*tuple_list)]
    return averages

def henkan_kashi(url,debug=False):
    bunsetukashi = shori_kashi(url)
    analyzer = JapaneseSentimentAnalyzer()
    
    henkan_kashi = []
    kuwashii_henkan_kashi = []
    for bunsetu in bunsetukashi:
        b = []
        for i in bunsetu:
            a = analyzer.analyze_sentiment(i)
            kuwashii_henkan_kashi.append(a)
            b.append(a)
        henkan_kashi.append(average_tuples(b))
    
    if debug:
        return henkan_kashi,kuwashii_henkan_kashi
    else:
        return henkan_kashi

print(henkan_kashi("https://utaten.com/lyric/mi22101740/",True))