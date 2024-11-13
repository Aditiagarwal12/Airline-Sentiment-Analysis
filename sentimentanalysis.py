from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import seaborn as sns

# Download necessary NLTK files
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)

# Load the dataset
def load_data():
    df = pd.read_csv("Tweets.csv")  # Ensure you have this CSV file in the project
    return df

# Process the dataset
df = load_data()
tweet_df = df[['text', 'airline_sentiment', 'airline_sentiment_confidence']].copy()

# Sentiment transformation function
def sentiment(label):
    if label < 0:
        return "Negative"
    elif label == 0:
        return "Neutral"
    elif label > 0:
        return "Positive"

# Apply sentiment function
tweet_df['sentiment'] = tweet_df['airline_sentiment_confidence'].apply(sentiment)

# Sentiment distribution plot
def plot_sentiment_distribution():
    fig, ax = plt.subplots(figsize=(7, 7))
    tags = tweet_df['airline_sentiment'].value_counts()
    num_unique_sentiments = len(tags)
    explode = (0.1,) * num_unique_sentiments
    colors = ("yellowgreen", "gold", "red")
    wp = {'linewidth': 2, 'edgecolor': "black"}

    tags.plot(kind='pie', autopct='%1.1f%%', shadow=True, colors=colors[:num_unique_sentiments],
              startangle=90, wedgeprops=wp, explode=explode, label='', ax=ax)

    ax.set_title('Distribution of sentiments')
    plt.savefig(os.path.join('static', 'sentiment-distribution.png'))  # Save the plot in the static folder
    plt.close()

# Wordcloud for positive sentiment tweets
def plot_positive_wordcloud():
    pos_tweets = tweet_df[tweet_df['sentiment'] == 'Positive']
    pos_tweets = pos_tweets.sort_values(['airline_sentiment_confidence'], ascending=False)
    text = ' '.join([word for word in pos_tweets['text']])
    
    # Generate the word cloud with adjusted size
    wordcloud = WordCloud(max_words=500, width=400, height=300).generate(text)  # You can adjust width/height if needed
    
    # Create a plot with the same size as the sentiment distribution plot
    fig, ax = plt.subplots(figsize=(5, 5), facecolor='None')  # Adjusted figure size to match sentiment distribution
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    ax.set_title('Most frequent words in positive tweets', fontsize=14)  # Adjusted title font size
    
    # Save the plot as an image in the 'static/images' folder
    plt.savefig('static/wordcloud.png', bbox_inches='tight', pad_inches=0.1)
    plt.close()

# Top 50 most frequent words bar chart
def plot_top_50_words():
    vectorizer = CountVectorizer(stop_words=nltk.corpus.stopwords.words('english'))
    word_matrix = vectorizer.fit_transform(tweet_df['text'])
    word_freq = pd.DataFrame(
        word_matrix.toarray(), columns=vectorizer.get_feature_names_out()
    ).sum(axis=0).sort_values(ascending=False).head(50)
    
    # Create the bar plot for top 50 frequent words
    plt.figure(figsize=(12, 8))
    sns.barplot(x=word_freq.index, y=word_freq.values)
    plt.xticks(rotation=90)
    plt.title("Top 50 Most Frequent Words")
    
    # Save the plot in the 'static' folder for web display
    plt.savefig(os.path.join('static', 'top_50_words.png'), bbox_inches='tight')
    plt.close()

@app.route('/')
def index():
    # Generate the charts
    plot_sentiment_distribution()
    plot_positive_wordcloud()
    plot_top_50_words()  # Add this line to generate the top 50 words graph
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
