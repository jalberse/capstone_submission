import nltk
from nltk.corpus import webtext
from nltk.corpus import gutenberg as gb
from nltk.tokenize import RegexpTokenizer

def get_emoji_response(comment):
    pass

if __name__ == "__main__":
    '''
    VERY basic text prediction using ngrams
    Does not even account for frequency, etc
    Better to use a statistical model.
    '''

    nltk.download('webtext')
    nltk.download('punkt')
    nltk.download('gutenberg')

    # TODO would save this dict, or maybe use a tree structure for shared prefix for faster search
    ngrams = {} # maps ngram to a list of words which follow the ngram in the corpus
    n = 3 # number of previous words to predict from

    # TODO grab existing model
    # TODO sample JSON request/responses -> slack

    # TODO by end of year : predictive model comments -> comment response

    webtext_raw = webtext.raw()
    gb_raw = gb.raw()
    
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(webtext_raw)
    tokens.append(tokenizer.tokenize(gb_raw))

    for i in range(len(tokens) - n):
        seq = ' '.join(tokens[i:i+n])
        #print(seq)
        if seq not in ngrams.keys():
            ngrams[seq] = [] 
        # Add the word following ngram
        ngrams[seq].append(tokens[i+n]) # could suggest next m words instead? Till punctuation?

    # Many trigrams are obviously not in model
    # Can search for trigram -> bigram -> 1-gram
    # Which we prefer should rely on statistical weighting
    while True:
        response = input()
        tokens = tokenizer.tokenize(response)
        seq = ' '.join(tokens[-3:]) # get last 3 words of response
        if seq not in ngrams.keys():
            print('** not in model **')
        else:
            print(ngrams[seq])
