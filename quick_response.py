
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# VADER sentiment analysis is licensed under the MIT license
# https://github.com/cjhutto/vaderSentiment

class TextAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        # TODO fill in and load config files mapping sentiment to responses

    def get_emoji_response(self, text):
        snt = self.vader.polarity_scores(text)
        print(snt['compound'])
        return snt

    def get_text_response(self, text):
        snt = self.vader.polarity_scores(text)
        print(snt['compound'])
        return snt

if __name__ == '__main__':
    analyzer = TextAnalyzer()

    tmp = 'I did not like this but my cousin did.'

    print(analyzer.get_emoji_response(tmp))