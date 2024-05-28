from concurrent.futures import ThreadPoolExecutor
from functools import partial
from lyrics_sentiment_analyzer import LyricsAnalyzer
import pickle
import concurrent

def hennkann(url, ly, kuwasii):
    data = ly.analyze_lyrics_sentiment(url,kuwasii)
    title = ly.get_title(url)
    return title, data

def main(urls,kuwasii):
    ly = LyricsAnalyzer()
    # シングルトンのThreadPoolExecutorを作成
    executor = ThreadPoolExecutor(max_workers=10)

    # main関数にURLを部分適用して実行
    future_to_url = {executor.submit(partial(main, url, ly, kuwasii)): url for url in urls}
    resu = []
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            title, data = future.result()
            data_a = [item[0] for item in data]
            data_b = [item[1] for item in data]
            resu.append([title,data_a,data_b])
        except Exception as e:
            print(f"Error fetching URL {url}: {e}")

    with open('data.pickle', mode='wb') as fo:
        pickle.dump(resu, fo)



urls = [
    "https://utaten.com/lyric/mi22101740/", #ここにうたてんのurlを貼り付けます(ここにあるのはボカロ系)
    "https://utaten.com/lyric/mi24022638/",
    "https://utaten.com/lyric/mi23080838/",
    "https://utaten.com/lyric/mi24050832/",
    "https://utaten.com/lyric/mi24010930/",
    "https://utaten.com/lyric/tt23052477/",
    "https://utaten.com/lyric/mi23101932/",
    "https://utaten.com/lyric/mi24022628/",
    "https://utaten.com/lyric/mi23081038/"
]

kuwasii = True #ここを変えるとFalseだと歌詞一行一行のTrueだと歌詞を文節ごとに分けたときの値を返します

main(urls,kuwasii)