import json
import re
import emoji

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# VADER sentiment analysis is licensed under the MIT license
# https://github.com/cjhutto/vaderSentiment

# TODO: Can't detect sentiment of emojis by themselves. 
#       Solution: regex to replace emojis by their names
#       this will at least give it a nonzero sentiment

class TextAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        # TODO fill in and load config files mapping sentiment to responses
        with open('emoji_response.json', 'r') as f:
            self.emoji_responses = json.load(f)
        with open('text_response.json', 'r') as f:
            self.text_responses = json.load(f)

    def replace_emojis(self, text):
        text = emoji.demojize(text)
        result = re.sub(r'[_:]', ' ', text)
        return result

    def get_emoji_response(self, text):
        text = self.replace_emojis(text)
        snt = self.vader.polarity_scores(text)
        sentiment = self.get_sentiment_class(snt)
        return self.emoji_responses[sentiment]

    def get_text_response(self, text):
        # TODO possibly combine with emoji response
        text = self.replace_emojis(text)
        snt = self.vader.polarity_scores(text)
        sentiment = self.get_sentiment_class(snt)
        return self.text_responses[sentiment]

    def get_sentiment_class(self, snt):
        if snt['compound'] >= 0.5:
            sentiment = 'very_positive'
        elif snt['compound'] >= 0.1:
            sentiment = 'positive'
        elif snt['compound'] >= 0:
            sentiment = 'neutral'
        elif snt['compound'] >= -0.5:
            sentiment = 'negative'
        else:
            sentiment = 'very_negative'
        return sentiment

if __name__ == '__main__':
    analyzer = TextAnalyzer()

    tmp = '🥰😍😻💘💝💖💗💓💞💕💟❤🧡💛💚💙💜'

    print(analyzer.replace_emojis(tmp))
    print(analyzer.get_text_response(tmp))