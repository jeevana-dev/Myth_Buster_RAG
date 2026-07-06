import os
import streamlit as st

from rag import MythBusterRAG

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="🛡️ Myth Buster AI",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Read API Keys from Streamlit Secrets
# -----------------------------
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

# -----------------------------
# Title
# -----------------------------
st.title("🛡️ Myth Buster AI")
st.subheader("AI-powered Myth vs Fact Verification using RAG + Groq + Tavily")

st.markdown("---")

question = st.text_area(
    "Enter a myth or claim",
    placeholder="Example: Drinking water cures cancer."
)

# -----------------------------
# Load RAG only once
# -----------------------------
@st.cache_resource
def load_rag():
    return MythBusterRAG()

rag = load_rag()

# -----------------------------
# Ask Button
# -----------------------------
if st.button("Verify Claim"):

    if question.strip() == "":
        st.warning("Please enter a claim.")
    else:

        with st.spinner("Searching knowledge base and trusted sources..."):

            answer = rag.answer(question)

        st.success("Verification Complete")

        st.markdown(answer)
