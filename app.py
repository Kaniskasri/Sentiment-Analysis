import streamlit as st
import sqlite3
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import docx
import PyPDF2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="Sentiment Analysis", page_icon="📊", layout="wide")

# NLTK Data
nltk.download('vader_lexicon', quiet=True)

# Initialize Database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# User Authentication
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Authentication Flow
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔑 User Authentication")
    option = st.radio("Choose an option:", ["Login", "Register"], horizontal=True)

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Submit", use_container_width=True):
        if option == "Register":
            if register_user(username, password):
                st.success("✅ Registration successful! Please log in.")
            else:
                st.error("⚠️ Username already exists!")
        else:
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials!")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("🔍 Navigation")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()

# File Processing Functions
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return " ".join([para.text for para in doc.paragraphs])

# Sentiment Analysis
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    
    positive, negative, neutral, total_compound = 0, 0, 0, 0
    positive_reviews, negative_reviews, neutral_reviews = [], [], []
    
    for sentence in sentences:
        score = sia.polarity_scores(sentence)
        total_compound += score['compound']
        if score['compound'] >= 0.05:
            positive += 1
            positive_reviews.append(sentence)
        elif score['compound'] <= -0.05:
            negative += 1
            negative_reviews.append(sentence)
        else:
            neutral += 1
            neutral_reviews.append(sentence)
            
    total = max(len(sentences), 1)
    return {
        "positive": round((positive / total) * 100, 1),
        "negative": round((negative / total) * 100, 1),
        "neutral": round((neutral / total) * 100, 1),
        "compound": round(total_compound / total, 3),
        "positive_reviews": positive_reviews,
        "negative_reviews": negative_reviews,
        "neutral_reviews": neutral_reviews
    }

# Main UI
st.markdown("""
    <h1 style='text-align:center;'>SENTIMENT ANALYSIS</h1>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📎 Upload PDF or DOCX", type=["pdf", "docx"])

if uploaded_file is not None:
    with st.spinner("⏳ Analyzing..."):
        text = extract_text_from_pdf(uploaded_file) if uploaded_file.name.endswith("pdf") else extract_text_from_docx(uploaded_file)
        sentiment_result = analyze_sentiment(text)

        df = pd.DataFrame({
            "Sentiment": ["Positive", "Negative", "Neutral"],
            "Percentage": [sentiment_result['positive'], sentiment_result['negative'], sentiment_result['neutral']]
        })
        
        fig = px.pie(df, values='Percentage', names='Sentiment', title='Sentiment Distribution')
        st.plotly_chart(fig)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("✨ Positive", f"{sentiment_result['positive']}%")
        with col2:
            st.metric("⚠️ Negative", f"{sentiment_result['negative']}%")
        with col3:
            st.metric("⚖️ Neutral", f"{sentiment_result['neutral']}%")
        
        st.markdown("""<br>""", unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns(3)
        
        if col_a.button("📜 Show Positive Reviews"):
            st.session_state['show_positive'] = not st.session_state.get('show_positive', False)
        if col_b.button("📜 Show Negative Reviews"):
            st.session_state['show_negative'] = not st.session_state.get('show_negative', False)
        if col_c.button("📜 Show Neutral Reviews"):
            st.session_state['show_neutral'] = not st.session_state.get('show_neutral', False)
        
        if st.session_state.get('show_positive', False):
            st.write("### Positive Reviews")
            st.write(sentiment_result['positive_reviews'])
        if st.session_state.get('show_negative', False):
            st.write("### Negative Reviews")
            st.write(sentiment_result['negative_reviews'])
        if st.session_state.get('show_neutral', False):
            st.write("### Neutral Reviews")
            st.write(sentiment_result['neutral_reviews'])
        
        fig_bar = px.bar(df, x='Sentiment', y='Percentage', title='Sentiment Comparison')
        st.plotly_chart(fig_bar)
        
        fig_line = px.line(df, x='Sentiment', y='Percentage', markers=True, title='Sentiment Trend')
        st.plotly_chart(fig_line)

if __name__ == "__main__":
    init_db()