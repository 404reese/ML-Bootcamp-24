import streamlit as st
import pandas as pd

# Load the CSV file
df = pd.read_csv("https://raw.githubusercontent.com/404reese/ML-projects/main/Book%20Recommendation%20System/books-dataset.csv")

# Convert 'average_rating' column to numeric type
df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')

def search_books(keyword):
  keyword = keyword.lower()
  result = df[df['title'].str.lower().str.contains(keyword) |
              df['authors'].str.lower().str.contains(keyword) |
              df['publisher'].str.lower().str.contains(keyword)
              ]
  return result

def main():
  st.title("Book Recommender System")
  
  st.header("Search for Books")
  keyword = st.text_input("Enter a keyword to search for books:")
  sort_by = st.selectbox("Sort by:", ["", "average_rating", "publication_date", "num_pages"])
  ascending = st.checkbox("Ascending")
  if st.button("Search"):
    books = search_books(keyword)
    st.write("Search Results:")
    st.write(books)
  
  st.header("Top 50 Books by Average Rating")
  top_books = df.nlargest(50, 'average_rating')
  st.write("Top 50 Books:")
  st.write(top_books)

if __name__ == "__main__":
  main()