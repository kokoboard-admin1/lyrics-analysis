import requests
from bs4 import BeautifulSoup
from japanese_bunkatu import BunsetsuWakachi
from japanese_sentiment import JapaneseSentimentAnalyzer

class LyricsAnalyzer:
    def __init__(self):
        self.bunsetsu_splitter = BunsetsuWakachi()
        self.sentiment_analyzer = JapaneseSentimentAnalyzer()

    def fetch_lyrics(self, url):
        """指定されたURLから歌詞を取得し、文字列のリストとして返す。"""
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        
        div = soup.find("div", class_="hiragana")
        
        # ルビテキストを削除
        for tag in div.findAll(class_="rt"):
            tag.decompose()
        
        # 歌詞を抽出して整形
        lyrics = div.get_text().split("\n")
        cleaned_lyrics = [line.replace("\r", "").replace(" ", "") for line in lyrics if line]
        
        return cleaned_lyrics
    
    def get_title(self, url):
        """タイトルを取得"""
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find(class_="newLyricTitle__main").get_text()
        title = title.replace("\n", "").replace(" ", "").replace("歌詞", "")
        return title

    def split_into_bunsetsu(self, lyrics):
        """歌詞を文節（日本語の構文単位）に分割する。"""
        bunsetsu_lyrics = [self.bunsetsu_splitter.bunsetsu_wakachi(line) for line in lyrics]
        return bunsetsu_lyrics

    def calculate_average_tuples(self, tuple_list):
        """タプルのリストの各要素の平均を計算する。"""
        num_tuples = len(tuple_list)
        num_elements = len(tuple_list[0])
        
        averages = [sum(elements) / num_tuples for elements in zip(*tuple_list)]
        return averages

    def analyze_lyrics_sentiment(self, url, debug=False):
        """歌詞の各文節の感情を分析し、結果を返す。"""
        lyrics = self.fetch_lyrics(url)
        bunsetsu_lyrics = self.split_into_bunsetsu(lyrics)
        
        sentiment_results = []
        detailed_sentiment_results = []
        line_sentiments = []

        for bunsetsu_line in bunsetsu_lyrics:
            for bunsetsu in bunsetsu_line:
                line_sentiments.append(self.sentiment_analyzer.analyze_sentiment(bunsetsu))
                detailed_sentiment_results.append(self.sentiment_analyzer.analyze_sentiment(bunsetsu))
            sentiment_results.append(self.calculate_average_tuples(line_sentiments))
        
        if debug:
            return detailed_sentiment_results
        else:
            return sentiment_results
