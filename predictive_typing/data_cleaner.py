import nltk
import pandas as pd
import re
import os

data = pd.read_csv('../../data/twcs.csv')

# TODO remove rows with numeric author_id (i.e. customers not businesses)
company_responses = data[data['author_id'].str.isnumeric() == False]['text']

# remove all @'s from text
# remove all URLs from text
rx_1 = "[@][a-zA-Z0-9_]*[\s]"
rx_2 = "(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?"
cleaned_responses = company_responses.replace(to_replace = rx_1 + '|' + rx_2, value = '', regex = True)

print(cleaned_responses)

# TODO concat text
text = cleaned_responses.str.cat(sep='\n').lower()
# Remove non-printable characters and remove signatures eg -anne, and thread notifs 1/2 2/2 etc
rx = r"[^\x00-\x7F]+|[*][\w]+|[\s]+[-][\s]*[\w]+|[\^][\w]+|[0-9]+[\/][0-9]+"
text = re.sub(rx, "", text)

# remove empty or very short tweets (common from say, tweets only containing foreign languages)
text = os.linesep.join([s for s in text.splitlines() if (s and len(s) > 5)])

chars = sorted(list(set(text)))
print(chars)
print(len(chars))

# TODO write text to file in ../../data
with open('../../data/twcs.txt', 'w') as f:
    f.write(text)