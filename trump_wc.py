from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from os import path, getcwd
from bs4 import BeautifulSoup
import requests as req

webpage = 'https://www.debates.org/voter-education/debate-transcripts/'
parentpage = req.get(webpage).text

soup = BeautifulSoup(parentpage, 'lxml')

linklist = soup.findAll('a')

tlinklist = []
for link in linklist:
    if 'Trump' in link.text:
        tlinklist.append(webpage[0:24]+link['href'])

trumpRamble = ''
for link in tlinklist:
    subpage = req.get(link).text.encode('utf-8')
    soup = BeautifulSoup(subpage, 'lxml')

    transcript = soup.find('div', id='content-sm')
    trumpcut = transcript.text.split('TRUMP: ')
    for t in trumpcut[1:len(trumpcut)]:
        firstPersonAfterTrump = ''
        firstIdx = 10000
        for people in ['CLINTON: ','HOLT: ', 'WALLACE: ', '[crosstalk]', 'COOPER: ', 'RADDATZ: ', 'QUESTION: ']:
            if people in t:
                idx = t.find(people)
                if idx < firstIdx:
                    firstIdx = idx
                    firstPersonAfterTrump = people
        trumpSaid = t.split(firstPersonAfterTrump)[0]
        trumpRamble = trumpRamble + trumpSaid

print(trumpRamble)

dir = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
trump_pic = np.array(Image.open(path.join(dir, 'trump.png')))

STOPWORDS.add('re')
wc = WordCloud(background_color="white", max_words=4000, mask=trump_pic, stopwords=STOPWORDS, max_font_size = 150)

wc.generate(trumpRamble)

image_colors = ImageColorGenerator(trump_pic)

plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
plt.axis('off')
plt.show()
