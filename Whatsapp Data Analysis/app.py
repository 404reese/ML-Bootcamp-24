# python -m streamlit run app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji
import seaborn as sns

# Create a Streamlit app
st.title("WhatsApp Analysis App")

# Load the data
url = "https://raw.githubusercontent.com/404reese/ML-projects/main/Whatsapp%20Data%20Analysis/big-WH-data.csv"

# Load the CSV file
@st.cache_data(ttl=600)  # 10 minutes
def load_data(url):
    return pd.read_csv(url)

# Load the data
df = load_data(url)

# Drop rows with missing values
df = df.dropna(subset=["Message"])

# Display the CSV file at the top
st.header("Chat Data")
st.write(df)

# Calculate the metrics
st.header("Overall Activity")

# Calculate the number of emojis used
def count_emojis(text):
    return emoji.demojize(text).count(':')

total_emojis = df["Message"].apply(count_emojis).sum()

total_messages = df.shape[0]
total_words = df["Message"].str.count(' ') + 1
total_words = total_words.sum()
unique_users = df["Number"].nunique()

# Display the metrics side by side
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Messages", total_messages)
with col2:
    st.metric("Total Words", total_words)
with col3:
    st.metric("Number of Users", unique_users)
with col4:
    st.metric("Total Emojis", total_emojis)

# Assuming you have a dataframe 'df' with a 'Date' column
df['Date'] = pd.to_datetime(df['Date'])

# Create a figure and axis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot the timeline of the chat
ax1.plot(df['Date'], [1]*len(df), '|')
ax1.set_title('Timeline of Chat')
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Messages')

# Create a new column 'Hour' and 'Day' from the 'Date' column
df['Hour'] = df['Date'].dt.hour
df['Day'] = df['Date'].dt.dayofweek

# Create a pivot table to count the number of messages per hour and day
heatmap_data = df.pivot_table(index='Hour', columns='Day', aggfunc='count', values='Message')

# Plot the heatmap
sns.heatmap(heatmap_data, ax=ax2, cmap='Blues')
ax2.set_title('Overall Heatmap of Chat Activity')
ax2.set_xlabel('Day of the Week')
ax2.set_ylabel('Hour of the Day')

# Show the plots
st.pyplot(fig)

# Create a bar graph of the most busy days
busy_days = df.resample('D', on='Date').count()['Message'].sort_values(ascending=False).head(10)

# Create a figure and axis for the bar graph
fig, ax = plt.subplots()
ax.bar(busy_days.index.date, busy_days.values)
ax.set_title('Most Busy Days')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Messages')

# Show the bar graph
st.pyplot(fig)

# Calculate the most engaged users
most_engaged_users = df["Number"].value_counts().head(5)

# Plot the most engaged users (vertical bar chart)
st.header("Most Engaged Users (Top 5)")
fig, ax = plt.subplots()
ax.bar(most_engaged_users.index, most_engaged_users.values)
ax.set_xlabel("User")
ax.set_ylabel("Number of Messages")

# Plot the top 5 users (pie chart)
fig2, ax2 = plt.subplots()
ax2.pie(most_engaged_users.values, labels=most_engaged_users.index, autopct='%1.1f%%')
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the plots side by side
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig)
with col2:
    st.pyplot(fig2)

# Create a word cloud
st.header("Word Cloud")
text = " ".join(df["Message"])
wordcloud = WordCloud(width=500, height=300, background_color="white").generate(text)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("on")  # Show the axis
st.pyplot(fig)

# Calculate word frequencies
word_freq = Counter(text.split())

# Create a table with the top 20 most used words
st.header("Top used words")
table_data = []
for word, freq in word_freq.most_common(10):
    table_data.append({"Word": word, "Frequency": freq})

# Plot a horizontal bar graph of the top 20 most used words
fig, ax = plt.subplots()
ax.barh(range(20), [freq for word, freq in word_freq.most_common(20)])
ax.set_yticks(range(20))
ax.set_yticklabels([word for word, freq in word_freq.most_common(20)])
ax.set_xlabel("Frequency")

# Create a columns layout
col1, col2 = st.columns(2)

# Add the table to the first column
with col1:
    st.table(table_data)

# Add the plot to the second column
with col2:
    st.pyplot(fig)

#emojis
st.header("Top used emojis")

# Count the total number of emojis used
total_emojis = 0
for message in df["Message"]:
    total_emojis += len([char for char in message if emoji.demojize(char) != char])

# Create a table with the top 20 most used emojis and their frequencies
emoji_freq = {}
for message in df["Message"]:
    for char in message:
        if emoji.demojize(char) != char:
            if char in emoji_freq:
                emoji_freq[char] += 1
            else:
                emoji_freq[char] = 1

table_data = [{"Emoji": emoji, "Frequency": freq} for emoji, freq in sorted(emoji_freq.items(), key=lambda x: x[1], reverse=True)[:10]]

# Plot a horizontal bar graph of the top 20 most used emojis
fig, ax = plt.subplots()
ax.barh(range(20), [freq for emoji, freq in sorted(emoji_freq.items(), key=lambda x: x[1], reverse=True)[:20]])
ax.set_yticks(range(20))
ax.set_yticklabels([emoji for emoji, freq in sorted(emoji_freq.items(), key=lambda x: x[1], reverse=True)[:20]])
ax.set_xlabel("Frequency")
ax.set_title("Top 20 Most Used Emojis")

# Create a columns layout
col1, col2 = st.columns(2)

# Add the table to the first column
with col1:
    st.table(table_data)

# Add the plot to the second column
with col2:
    st.pyplot(fig)

