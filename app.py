from flask import Flask, render_template
import pandas as pd
import random
from nltk.corpus import stopwords
from collections import Counter
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk

# Ensure stopwords are downloaded
nltk.download('stopwords')

app = Flask(__name__)

def display_topics(model, feature_names, no_top_words):
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topics.append([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
    return topics

@app.route('/')
def index():
    # Load data
    df = pd.read_csv('headlines.csv')
    headlines = df['Headline'].dropna().str.lower()
    
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = ' '.join(headlines).split()
    words = [word for word in words if word not in stop_words and word != 'watch']
    
    # Word frequency analysis
    word_counts = Counter(words)
    top_n_words = word_counts.most_common(10)
    
    # Generate a phrase using a subset of the top words
    phrase_words = random.sample([word for word, _ in top_n_words], random.randint(1, min(5, len(top_n_words))))
    phrase = ' '.join(phrase_words)
    
    # Sentiment analysis
    df['Sentiment'] = df['Headline'].apply(lambda x: TextBlob(x).sentiment.polarity)
    sentiment_counts = df['Sentiment'].apply(lambda x: 'Positive' if x > 0 else 'Negative' if x < 0 else 'Neutral').value_counts()
    
    # Topic modeling
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(headlines)
    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(X)
    topics = display_topics(lda, vectorizer.get_feature_names_out(), 5)
    
    return render_template('index.html', phrase=phrase, topics=topics, sentiment_counts=sentiment_counts.to_dict(), top_n_words=top_n_words)

if __name__ == "__main__":
    app.run(debug=True)
