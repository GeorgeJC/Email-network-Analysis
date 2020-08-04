import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english')) 

data = pd.read_csv("Emails2.csv")
#print(data["RawText"][1])
textlist = data['RawText'].tolist()
def clean(texts):
    ctext=[]
    for txt in texts:
        txt=txt.lower()
        txt1=(re.sub(r'[[$$()<>{}!:,;-_|\."\'\\]','',txt));
        txt1=(re.sub(r'\s+',' ',txt1))
        txt1=(re.sub(r'[0-9]+','',txt1))
        ctext.append(txt1)
    return ctext;



def remo(str1):
    s=''
    for line in str(str1).splitlines():
        if not(line.startswith('From:') or line.startswith('To:') or line.startswith('Case No.')
               or line.startswith('Sent:') or line.startswith('Doc No.') or
               line.startswith('Subject:')or line.startswith('Fw:')or line.startswith('Cc:')
               or line.startswith('B6') or line.startswith('Date 05132015:')
               or line.startswith('STATE DEPT.')or line.startswith('SUBJECT TO AGREEMENT')
               or line.startswith('U.S. Department of State')or line.startswith('Sunday')
               or line.startswith('Monday') or line.startswith('Tuesday') or line.startswith('Wednesday')
               or line.startswith('Thursday') or line.startswith('Friday') or line.startswith('Saturday')
               or line.startswith('B5') or line.startswith('B7C') or line.startswith('Attachments:')
               or line.startswith('U.S. Department') or line.startswith('UNCLASSIFIED')
               or line.startswith('Original Message') or line.startswith('RELEASE IN') or line.startswith('FULL')):
            s=s+line+'\n'
    return s

new=[]

for i in range(0,len(textlist)-1):
    s=remo(textlist[i])
    new.append(s)
txtfinal=clean(new)
wocl=' '.join([str(elem) for elem in txtfinal])

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
#worddcloudgen(wocl)

from textblob import TextBlob
def senti(df,frofn,to):
    sent=0
    c=0
    for i in range(0,len(df)-1):
        if((frofn in str(df['MetadataFrom'][i])) and (to in str(df['MetadataTo'][i]))):
            txt=txtfinal[i]
            c+=1
            pol=TextBlob(txt).polarity
            sent+=pol
    if(c>0):
        return sent/c
    else:
        return 0



#From Hilary
frH=[]
for g in range(0,len(data)-1):
    if(data['MetadataTo'][g]!='nan' and data['MetadataFrom'][g]=='H'):
        frH.append(data['MetadataTo'][g])
fromH=Counter(frH)

#To Hilary
ToH=[]
for g in range(0,len(data)-1):
    if(data['MetadataFrom'][g]!='nan' and data['MetadataTo'][g]=='H'):
        ToH.append(data['MetadataFrom'][g])
TooH=Counter(ToH)


mostsent=[key for key, _ in TooH.most_common()]
print("\n\n")
print("Sentiments of others mails to Hilary are as follows")
print("\n\n")
polmost={}
for y in range(0,5):
    polmost[mostsent[y]]=senti(data,mostsent[y],'H')
plt.bar(range(len(polmost)), list(polmost.values()), align='center')
plt.xticks(range(len(polmost)), list(polmost.keys()))
plt.show()

mostrec=[key for key,_ in fromH.most_common()]
print("\n\n")
print("Sentiments of hilary's mails to others are as follows")
print("\n\n")
polrec={}
for f in range(0,5):
    polrec[mostrec[f]]=senti(data,'H',mostrec[f])

plt.bar(range(len(polrec)), list(polrec.values()),align='center')
plt.xticks(range(len(polrec)), list(polrec.keys()))
plt.show()

allsenti=[]
neg=0
nut=0
pos=0
hpos=0
highest=0
lowest=0
high=''
low=''
for j in range(0,len(txtfinal)):
    pola=TextBlob(txtfinal[j]).polarity
    allsenti.append(round(pola,2))
    if(pola<lowest):
        lowest=pola
        low=data['MetadataFrom'][j]
    if(pola>highest):
        highest=pola
        high=data['MetadataFrom'][j]
    if(pola<(0)):
        neg+=1
    elif(pola>=(-0.1) and pola<=0.1):
        nut+=1
    else:
        pos+=1

print("\nPerson with lowest polarity is : ")
print(low)
print(lowest)
print("\nPerson with highest polarity is : ")
print(high)
print(highest)

print("\n\n")
print("Pie chart of different types of sentiment:-")
print("\n\n")

labels = 'Negative', 'neutral', 'Positive'
sizes = [neg,nut,pos]
colors = ['red', 'yellow','lightgreen']
plt.pie(sizes,labels=labels,colors=colors,autopct='%1.1f%%')
plt.axis('equal')
plt.show()
