import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="English to Kannada Translator",
    page_icon="🌐",
    layout="centered"
)

# ---------------- GROQ API CONFIGURATION ----------------
try:
    api_key = st.secrets["GROQ_API_KEY_1"]
except (KeyError, FileNotFoundError):
    st.error(
        "Groq API key not found. Please configure "
        "GROQ_API_KEY_1 in Streamlit Secrets."
    )
    st.stop()

# Initialize Groq model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key,
    temperature=0
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Main application background */
.stApp {
    background: linear-gradient(135deg, #101828, #172554);
    color: white;
}

/* Main heading */
h1, h2, h3, p {
    color: white;
}

/* Input and output text areas */
.stTextArea textarea {
    background-color: white !important;
    color: black !important;
    -webkit-text-fill-color: black !important;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    font-size: 17px;
}

/* Text area labels */
.stTextArea label {
    color: white !important;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
    min-height: 45px;
}

/* Download button */
.stDownloadButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: bold;
}

/* Divider */
hr {
    border-color: #475569;
}

/* Footer */
.footer {
    text-align: center;
    color: #cbd5e1;
    font-size: 13px;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🌐 English to Kannada Translator")

st.markdown(
    "Translate English sentences into Kannada using "
    "**Groq AI and Few-Shot Prompting.**"
)

st.divider()

# ---------------- SESSION STATE ----------------
if "english_text" not in st.session_state:
    st.session_state.english_text = ""

if "translation" not in st.session_state:
    st.session_state.translation = ""

# ---------------- TRANSLATION FUNCTION ----------------
def translate_text(text):
    messages = [
        SystemMessage(
            content=(
                "You are an English-to-Kannada translator. "
                "Translate the given English text into natural, "
                "grammatically correct Kannada. Preserve the "
                "original meaning. Return only the Kannada "
                "translation without explanations."
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

# ---------------- INPUT ----------------
english_text = st.text_area(
    "Enter English Text",
    placeholder="Example: I am learning Python.",
    height=130,
    key="english_text"
)

# ---------------- BUTTONS ----------------
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

# ---------------- CLEAR FUNCTION ----------------
if clear_button:
    st.session_state.english_text = ""
    st.session_state.translation = ""
    st.rerun()

# ---------------- TRANSLATE ACTION ----------------
if translate_button:
    if not english_text.strip():
        st.warning("Please enter some English text.")
    else:
        try:
            with st.spinner("Translating into Kannada..."):
                result = translate_text(english_text)

            st.session_state.translation = result

        except Exception as e:
            st.error(f"Translation failed: {e}")

# ---------------- OUTPUT ----------------
if st.session_state.translation:
    st.divider()

    st.subheader("Kannada Translation 🇮🇳")

    st.text_area(
        "Translated Text",
        value=st.session_state.translation,
        height=150,
        disabled=True,
        key="kannada_output"
    )

    st.download_button(
        label="⬇️ Download Translation",
        data=st.session_state.translation,
        file_name="kannada_translation.txt",
        mime="text/plain",
        use_container_width=True
    )

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    Powered by Groq AI · LangChain · Streamlit
</div>
""", unsafe_allow_html=True)
