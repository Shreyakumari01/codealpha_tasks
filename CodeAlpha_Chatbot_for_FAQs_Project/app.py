import streamlit as st
import pandas as pd
import nltk
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources
nltk.download('punkt_tab')
nltk.download('stopwords')

# Load English stopwords
stop_words = set(stopwords.words('english'))

# Text preprocessing function
def preprocess_text(text):

    # Convert text to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize the text
    words = word_tokenize(text)

    # Remove stopwords
    words = [word for word in words if word not in stop_words]

    # Join tokens back into a sentence
    return ' '.join(words)

# Load the FAQ dataset
df = pd.read_json("train.jsonl", lines=True)

# Remove rows with missing questions or answers
df = df.dropna(subset=['question', 'answer'])

# Remove duplicate questions
df = df.drop_duplicates(subset=['question'])

# Reset index
df = df.reset_index(drop=True)

# Display dataset information
print("Dataset loaded successfully!")
print("Total FAQs:", len(df))
print(df.head())

# Preprocess all FAQ questions
df['processed_question'] = df['question'].apply(preprocess_text)

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Convert FAQ questions into TF-IDF vectors
faq_vectors = vectorizer.fit_transform(df['processed_question'])

print("TF-IDF model created successfully!")

# Function to find the best matching FAQ
def get_response(user_question):

    # Preprocess the user's question
    processed_question = preprocess_text(user_question)

    # Convert the question into a TF-IDF vector
    user_vector = vectorizer.transform([processed_question])

    # Calculate cosine similarity with all FAQ questions
    similarities = cosine_similarity(user_vector, faq_vectors).flatten()

    # Find the index of the most similar FAQ
    best_match_index = similarities.argmax()

    # Get the highest similarity score
    best_score = similarities[best_match_index]

    # Set a minimum similarity threshold
    if best_score < 0.20:
        return "Sorry, I couldn't find a relevant answer. Please try asking in a different way."

    # Return the answer of the best matching FAQ
    return df.iloc[best_match_index]['answer']

# Streamlit chatbot interface
st.set_page_config(
    page_title="CustomerCare Chatbot",
    page_icon="🛍️"
)

# Sidebar
st.sidebar.title("🛍️ CustomerCare")
st.sidebar.write("Your E-commerce Support Assistant")

st.sidebar.subheader("What can I ask?")
st.sidebar.markdown("""
- 📦 Order Tracking
- 💳 Payment Methods
- 🚚 Shipping Information
- 🔄 Returns and Refunds
- ❌ Order Cancellation
- 🛒 Product Availability
- 👤 Account Support
""")

st.sidebar.info(
    "Ask a question to get an instant answer from our FAQ database."
)

# Main chatbot interface
st.title("🛍️ CustomerCare")
st.subheader("E-commerce Customer Support Chatbot")

st.write(
    "Hello! Ask me anything about orders, payments, "
    "shipping, returns, and cancellations."
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Welcome message
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write(
            "👋 Hello! Welcome to CustomerCare. "
            "I'm your e-commerce support assistant. "
            "How can I help you today?"
        )

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Accept user input
user_question = st.chat_input("Type your question here...")

if user_question:

    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.write(user_question)

    # Generate chatbot response
    response = get_response(user_question)

    # Display chatbot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)