# python -m streamlit run ann2.py

# libraries
import streamlit as st
from textblob import TextBlob
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import cleantext
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nrclex import NRCLex

# Load the dataset
df = pd.read_csv("Reviews.csv")

review_text = df["Text"]

# Initialize the VADER sentiment intensity analyzer
analyzer = SentimentIntensityAnalyzer()

# Analyze sentiment and subjectivity
sentiment_scores = []
blob_subj = []
for review in review_text:
    sentiment_scores.append(analyzer.polarity_scores(review)["compound"])
    blob = TextBlob(review)
    blob_subj.append(blob.subjectivity)

# Classify sentiment based on VADER scores
sentiment_classes = []
for sentiment_score in sentiment_scores:
    if sentiment_score > 0.8:
        sentiment_classes.append("highly positive")
    elif sentiment_score > 0.4:
        sentiment_classes.append("positive")
    elif -0.4 <= sentiment_score <= 0.4:
        sentiment_classes.append("neutral")
    elif sentiment_score < -0.4:
        sentiment_classes.append("negative")
    else:
        sentiment_classes.append("highly negative")

# Streamlit app
st.title("Sentiment and Emotion Analysis On Customer Feedback")

# Take input from the user
user_input = st.text_area("Enter customer feedback:")
blob = TextBlob(user_input)

user_sentiment_score = analyzer.polarity_scores(user_input)["compound"]
if user_sentiment_score > 0.8:
    user_sentiment_class = "highly positive"
elif user_sentiment_score > 0.4:
    user_sentiment_class = "positive"
elif -0.4 <= user_sentiment_score <= 0.4:
    user_sentiment_class = "neutral"
elif user_sentiment_score < -0.4:
    user_sentiment_class = "negative"
else:
    user_sentiment_class = "highly negative"

st.write("**VADER Sentiment Class:** ", user_sentiment_class, "\n**VADER Sentiment Scores:**", user_sentiment_score)
st.write("**TextBlob Polarity**", blob.sentiment.polarity, "\n**TextBlob Subjectivity:**", blob.sentiment.subjectivity)

# Emotion Analysis
if user_input:
    emotion_scores = NRCLex(user_input)
    st.subheader("Emotion Analysis")
    st.write("Top Emotions:", emotion_scores.top_emotions)
    st.write("Emotion Intensity:", emotion_scores.raw_emotion_scores)

# Display clean text
pre = st.text_input('Clean Text: ')
if pre:
    st.write(cleantext.clean(pre, clean_all=False, extra_spaces=True, stopwords=True, lowercase=True, numbers=True, punct=True))
else:
    st.write("No text provided for cleaning.")

# Word Cloud Visualization
if not review_text.empty:  # Check if review_text is not empty
    all_text = ' '.join(review_text)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    st.subheader("Word Cloud")
    st.image(wordcloud.to_image())
else:
    st.subheader("Word Cloud")
    st.write("No data available for generating word cloud.")

# Graphical Representation of Data
st.subheader("Graphical Representation of Data")
plt.figure(figsize=(10, 6))

sentiment_scores_by_class = {k: [] for k in set(sentiment_classes)}
for sentiment_score, sentiment_class in zip(sentiment_scores, sentiment_classes):
    sentiment_scores_by_class[sentiment_class].append(sentiment_score)

for sentiment_class, scores in sentiment_scores_by_class.items():
    plt.hist(scores, label=sentiment_class, alpha=0.5)

plt.xlabel("Sentiment score")
plt.ylabel("Count")
plt.title("Distribution of sentiment scores by class")
plt.legend()
st.pyplot(plt)

# Exporting Data
st.subheader("Export Data")
export_format = st.selectbox("Select export format:", ["CSV", "Excel"])

if st.button("Export Data"):
    if export_format == "CSV":
        csv_data = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv_data, file_name="sentiment_analysis_results.csv", mime="text/csv")
    elif export_format == "Excel":
        excel_data = df.to_excel(index=False)
        st.download_button(label="Download Excel", data=excel_data, file_name="sentiment_analysis_results.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# DataFrame with sentiment analysis results
df["Sentiment Class"] = sentiment_classes
df["Sentiment Score"] = sentiment_scores
df["Subjectivity"] = blob_subj

new_df = df[["Score", "Text", "Sentiment Score", "Sentiment Class", "Subjectivity"]]
st.subheader("Input Dataframe")
st.dataframe(new_df.head(30), use_container_width=True)