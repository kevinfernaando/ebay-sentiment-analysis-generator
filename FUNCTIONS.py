from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
import nltk


warnings.filterwarnings('ignore')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

def get_data(url):
    r = req.get(url, headers = headers)
    print(r)
    this_soup = BeautifulSoup(r.text, 'html.parser')
    reviews_url = this_soup.find('a', {'class': 'sar-btn right'})['href']
    num_of_reviews = this_soup.find('a', {'class': 'sar-btn right'}).text

    num_of_reviews = int(num_of_reviews.split()[2].replace(',', ''))
    num_of_pages = int(num_of_reviews / 10)

    if num_of_pages > 10:
        num_of_pages = 10

    url = this_soup.find('a', {'class': 'sar-btn right'})['href']

    data = []
    for page in range(1, num_of_pages+1):
        r = req.get(f'{url}&pgn={page}', headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        reviews = soup.findAll('div', {'class': 'ebay-review-section'})
        for review in reviews:
            title = review.find('h3', {'class': 'review-item-title wrap-spaces'})
            review1 = review.find('p', {'class': 'review-item-content rvw-wrap-spaces'})
            review2 = review.find('span', {'class': 'show-full-review'})
            
            stars = len(review.find_all('i', {'class': 'fullStar'}))
            date = review.find('span', {'class': 'review-item-date'}).text    

            if review1 is None:
                continue

            if review2 is None:
                text_review = review1.text
            else:
                text_review = review1.text + review2.text

            this_title = title.text
            this_review = text_review

            d = {'title': this_title, 'review': this_review, 'star': stars, 'date': date}
            data.append(d)

    return data


def generate_df(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df.date, format = '%b %d, %Y')
    df = df.set_index('date').sort_index()
    return df


def get_freq(df):
    global clear_words
    titles = ' '.join(df.title)
    reviews = ' '.join(df.review)
    
    words = set(nltk.corpus.words.words())
    reviews = " ".join(w for w in nltk.wordpunct_tokenize(reviews) if w.lower() in words or not w.isalpha())

    stopwords = nltk.corpus.stopwords.words("english")
    tokens = nltk.word_tokenize(reviews)

    clear_words = [w.lower() for w in tokens if w.lower() not in stopwords]
    clear_words = [w for w in clear_words if w.isalpha()]
    
    nlp_words=nltk.FreqDist(clear_words)
    return nlp_words, clear_words
    
def get_pos_neg(clear_words):
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()

    pos_words = [w for w in clear_words if sia.polarity_scores(w)['pos'] > 0.5]
    neg_words = [w for w in clear_words if sia.polarity_scores(w)['neg'] > 0.5]

    pos_words_freq=nltk.FreqDist(pos_words)
    pos_words_freq = pd.Series(pos_words_freq).sort_values(0, ascending = False).head(20)
    pos_words_freq = pd.DataFrame(list(pos_words_freq.items()), columns=["Word", "Frequency"]).sort_values('Frequency').head(20)

    neg_words_freq=nltk.FreqDist(neg_words)
    neg_words_freq = pd.Series(neg_words_freq).sort_values(0, ascending = False).head(20)
    neg_words_freq = pd.DataFrame(list(neg_words_freq.items()), columns=["Word", "Frequency"]).sort_values('Frequency').head(20)
    
    return pos_words_freq, neg_words_freq, pos_words, neg_words