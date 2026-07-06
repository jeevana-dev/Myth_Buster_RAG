from prompts import SYSTEM_PROMPT
import os

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from tavily import TavilyClient


class MythBusterRAG:

    def __init__(self):

        # Embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Load FAISS database
        self.vector_db = FAISS.load_local(
            "vector_db",
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        # Groq LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        )

        # Tavily Search
        self.tavily = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )

    def answer(self, question):

        # Search local knowledge base
        docs = self.vector_db.similarity_search(question, k=3)

        context = "\n\n".join([doc.page_content for doc in docs])

        # Search the web
        web = self.tavily.search(
            query=question,
            search_depth="advanced",
            max_results=3
        )

        web_context = ""

        for result in web["results"]:
            web_context += (
                f"Title: {result['title']}\n"
                f"Content: {result['content']}\n\n"
            )

        prompt = f"""
{SYSTEM_PROMPT}

Local Knowledge:
{context}

Web Knowledge:
{web_context}

Question:
{question}
"""

        response = self.llm.invoke(prompt)

        return response.content
