
import streamlit as st
from deep_translator import MyMemoryTranslator

# Page configuration
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

# Application heading
st.title("🌍 Language Translation Tool")
st.write("Translate text between different languages.")

# Supported languages for MyMemory
languages = {
    "English": "english",
    "Hindi": "hindi",
    "French": "french",
    "Spanish": "spanish",
    "German": "german",
    "Japanese": "japanese",
    "Chinese (Simplified)": "chinese simplified",
    "Bengali": "bengali",
    "Tamil": "tamil india",
    "Telugu": "telugu",
    "Marathi": "marathi",
    "Arabic": "arabic"
}

# Language selection
col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "Translate from",
        list(languages.keys())
    )

with col2:
    target = st.selectbox(
        "Translate to",
        list(languages.keys()),
        index=1
    )

# Text input
text = st.text_area(
    "Enter text",
    placeholder="Type something to translate...",
    height=150
)

# Translation button
if st.button("Translate 🌐", type="primary"):

    if not text.strip():
        st.warning("Please enter some text.")

    elif source == target:
        st.info("Source and target languages are the same.")
        st.subheader("Result")
        st.write(text)

    else:
        try:
            # Create translator
            translator = MyMemoryTranslator(
                source=languages[source],
                target=languages[target]
            )

            # Translate text
            result = translator.translate(text)

            # Display result
            st.subheader("Translated Text")
            st.text_area(
                "Translation Result",
                value=result,
                height=150
            )

            st.success("Translation completed successfully!")

        except Exception as e:
            st.error("Translation failed. Please try again.")
            st.caption(f"Error details: {e}")

# Footer
st.divider()
st.caption("Language Translation Tool | Developed using Python and Streamlit")
