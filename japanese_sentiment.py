import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

class JapaneseSentimentAnalyzer:
    def __init__(self):
        # 事前学習済みの日本語感情分析モデルとそのトークナイザをロード
        self.model = AutoModelForSequenceClassification.from_pretrained('christian-phu/bert-finetuned-japanese-sentiment')
        self.tokenizer = AutoTokenizer.from_pretrained('christian-phu/bert-finetuned-japanese-sentiment', model_max_length=512)
        self.nlp = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer, truncation=True)

    def analyze_sentiment(self, text):
        inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=512)
        outputs = self.model(**inputs)
        logits = outputs.logits

        # ロジットを確率に変換
        probabilities = torch.softmax(logits, dim=1)[0]

        # 各感情ラベルの確率を取得
        sentiment_scores = {
            'positive': probabilities[self.model.config.label2id['positive']].item(),
            'negative': probabilities[self.model.config.label2id['negative']].item()
        }

        # 最も高い確率の感情ラベルを取得
        sentiment_label = self.model.config.id2label[torch.argmax(probabilities).item()]

        return sentiment_label, sentiment_scores