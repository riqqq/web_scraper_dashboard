import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Ensure stopwords are downloaded
nltk.download('stopwords')

# Load the data
df = pd.read_csv('headlines.csv')

# Preprocess the data
headlines = df['Headline'].dropna().str.lower()

# Tokenize and remove stopwords
stop_words = set(stopwords.words('english'))
words = ' '.join(headlines).split()
words = [word for word in words if word not in stop_words and word != 'watch']

# Word frequency analysis
word_counts = Counter(words)
top_n_words = word_counts.most_common(10)

# Sentiment analysis
df['Sentiment'] = df['Headline'].apply(lambda x: TextBlob(x).sentiment.polarity)
sentiment_counts = df['Sentiment'].apply(lambda x: 'Positive' if x > 0 else 'Negative' if x < 0 else 'Neutral').value_counts()

# Topic modeling
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(headlines)
lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(X)

def display_topics(model, feature_names, no_top_words):
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topics.append([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
    return topics

topics = display_topics(lda, vectorizer.get_feature_names_out(), 5)

# Visualizations
# Bar plot for top 10 words
plt.figure(figsize=(10, 6))
plt.bar([word for word, _ in top_n_words], [count for _, count in top_n_words], color='skyblue')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 10 Most Frequent Words')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('static/word_plot.png', format='png')

# Word cloud for top 10 words
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(top_n_words))
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.savefig('static/wordcloud.png', format='png')

# Sentiment distribution plot
plt.figure(figsize=(10, 6))
sentiment_counts.plot(kind='bar', color=['green', 'red', 'grey'])
plt.xlabel('Sentiment')
plt.ylabel('Frequency')
plt.title('Sentiment Distribution of Headlines')
plt.tight_layout()
plt.savefig('static/sentiment_plot.png', format='png')
