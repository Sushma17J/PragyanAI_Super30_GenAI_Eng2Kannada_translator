
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

# Page configuration
st.set_page_config(
    page_title="English to Kannada Translator",
    page_icon="🌐",
    layout="centered"
)

# Get API key from Streamlit Secrets
try:
    api_key = st.secrets["GROQ_API_KEY_1"]
except (KeyError, FileNotFoundError):
    st.error(
        "Groq API key not found. Configure "
        "GROQ_API_KEY_1 in Streamlit Secrets."
    )
    st.stop()

# Initialize Groq model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key,
    temperature=0
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101828, #172554);
    color: white;
}
h1, h2, p, label {
    color: white !important;
}
.stTextArea textarea {
    background-color: #ffffff;
    color: #111827;
    border-radius: 10px;
}
.stButton > button {
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Application heading
st.title("🌐 English to Kannada Translator")
st.write(
    "Translate English sentences into Kannada using "
    "**Groq AI and Few-Shot Prompting**."
)

st.divider()

# Input
english_text = st.text_area(
    "Enter English Text",
    placeholder="Example: I am learning Python.",
    height=150
)

# Translation function
def translate_text(text):
    messages = [
        SystemMessage(
            content=(
                "You are an English-to-Kannada translator. "
                "Translate English text into natural Kannada. "
                "Preserve the original meaning. "
                "Return only the Kannada translation."
            )
        ),

        # Few-shot example 1
        HumanMessage(content="Good morning."),
        AIMessage(content="ಶುಭೋದಯ."),

        # Few-shot example 2
        HumanMessage(content="How are you?"),
        AIMessage(content="ನೀವು ಹೇಗಿದ್ದೀರಿ?"),

        # Few-shot example 3
        HumanMessage(content="I am going to college."),
        AIMessage(content="ನಾನು ಕಾಲೇಜಿಗೆ ಹೋಗುತ್ತಿದ್ದೇನೆ."),

        # Few-shot example 4
        HumanMessage(content="Thank you very much."),
        AIMessage(content="ತುಂಬಾ ಧನ್ಯವಾದಗಳು."),

        # Actual user query
        HumanMessage(content=text)
    ]

    response = llm.invoke(messages)
    return response.content

# Buttons
col1, col2 = st.columns(2)

with col1:
    translate_button = st.button(
        "🌐 Translate",
        type="primary",
        use_container_width=True
    )

with col2:
    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )

# Handle clear
if clear_button:
    st.session_state["english_text"] = ""
    st.session_state["translation"] = ""
    st.rerun()

# Handle translation
if translate_button:
    if not english_text.strip():
        st.warning("Please enter some English text.")
    else:
        try:
            with st.spinner("Translating into Kannada..."):
                translation = translate_text(english_text)

            st.session_state["translation"] = translation

        except Exception as e:
            st.error(f"Translation failed: {e}")

# Display result
if st.session_state.get("translation"):
    st.divider()
    st.subheader("Kannada Translation 🇮🇳")
    st.text_area(
        "Translated Text",
        value=st.session_state["translation"],
        height=150,
        disabled=True
    )

    st.download_button(
        "⬇️ Download Translation",
        data=st.session_state["translation"],
        file_name="kannada_translation.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()
st.caption("Powered by Groq AI • LangChain • Streamlit")
