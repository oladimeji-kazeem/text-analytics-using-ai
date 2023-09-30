import streamlit as st
from wordcloud import WordCloud
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from docx import Document
import pdfplumber
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser  # Add these import statements
from sumy.summarizers.text_rank import TextRankSummarizer  # Add this import statement
import nltk
nltk.download('punkt')

# Download NLTK data including stopwords
nltk.download('stopwords')

from nltk.corpus import stopwords

# Get the list of English stopwords
stop_words = set(stopwords.words('english'))


# Function to summarize text using Gensim TextRank
def summarize_text_textrank(text, sentences_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return " ".join([str(sentence) for sentence in summary])

# Function to extract text from a Word document
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Function to extract text from a PDF file using pdfplumber
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to generate a word cloud
def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Function to analyze sentiment using NLTK's VADER
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment

text_to_summarize = ""  # Initialize text_to_summarize

st.title("Text Summarization and Analysis")

summarization_library = st.selectbox("Select a summarization library", ["textrank"])

source = st.selectbox("Select the data source", ["text", "file"])

if source == "text":
    input_text = st.text_area("Enter the text you want to summarize")
    text_to_summarize = input_text
elif source == "file":
    uploaded_file = st.file_uploader("Upload a Word document or PDF", type=["docx", "pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Processing..."):
            if uploaded_file.type == "application/pdf":
                text_to_summarize = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text_to_summarize = extract_text_from_docx(uploaded_file)
else:
    st.warning("Please select a valid data source.")

if text_to_summarize:
    # User control for the number of words in the summary
    sentences_count = st.number_input("Number of sentences in the summary", min_value=1, max_value=10, value=5)
    
    # Create two tabs: "Summary" and "Analytics"
    selected_tab = st.radio("Select a tab:", ["Summary", "Analytics"])

    if selected_tab == "Summary":
        # Summarize button (in "Summary" tab)
        if st.button("Summarize"):
            summary = summarize_text_textrank(text_to_summarize, sentences_count)
            st.subheader("Summary:")
            st.write(summary)
    elif selected_tab == "Analytics":
        # Word cloud
        st.header("Word Cloud")
        if st.button("Generate Word Cloud"):
            st.image(generate_word_cloud(text_to_summarize).to_image())

        # Sentiment analysis
        st.header("Sentiment Analysis")
        if st.button("Analyze Sentiment"):
            sentiment = analyze_sentiment(text_to_summarize)
            st.subheader("Sentiment Analysis:")
            st.write(f"Positive: {sentiment['pos']:.2%}")
            st.write(f"Negative: {sentiment['neg']:.2%}")
            st.write(f"Neutral: {sentiment['neu']:.2%}")
            st.write(f"Compound Score: {sentiment['compound']:.2f}")

        # User control for the number of keywords
        num_keywords = st.number_input("Number of keywords to display", min_value=1, max_value=20, value=10)

        # Keywords button
        if st.button("Extract Keywords"):
            st.subheader("Keywords:")
            # Extract keywords using NLTK's stopwords
            keywords = [word for word in text_to_summarize.split() if word.lower() not in stop_words][:num_keywords]
            st.write(keywords)