import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np

stop_words = set(stopwords.words('english'))

with open('massmedia.txt', 'r') as file:
    data = file.read().replace('\n', ' ')
data=data.lower()
def worddcloudgen(stri):
     comment_words=' '
     tokens = word_tokenize(stri)
     tokens = [w for w in tokens if not w in stop_words]
     print(tokens[:5])
     comment_words += " ".join(tokens)+" "
     wordcloud = WordCloud(width = 800, height = 800, background_color ='white',min_font_size = 10,max_font_size=130).generate(comment_words) 
     # plot the WordCloud image                        
     plt.figure(figsize = (8, 8), facecolor = None) 
     plt.imshow(wordcloud) 
     plt.axis("off") 
     plt.tight_layout(pad = 0) 
     plt.show()
worddcloudgen(data)
