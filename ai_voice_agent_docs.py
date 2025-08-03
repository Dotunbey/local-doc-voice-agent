import streamlit as st
import edge_tts
import ollama
import asyncio
import tempfile
from fastembed.embedding import DefaultEmbedding
from qdrant_client import QdrantClient
from qdrant_client.http import models
from firecrawl import Firecrawl
import uuid

# ---------------------------- Configuration ----------------------------
st.set_page_config(page_title="AI Voice Agent", page_icon="🎤", layout="centered")

# Initialize states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "audio_path" not in st.session_state:
    st.session_state.audio_path = ""

# ---------------------------- Sidebar ----------------------------
st.sidebar.title("🚀 Setup")

firecrawl_key = st.sidebar.text_input("Firecrawl API Key", type="password")
qdrant_url = st.sidebar.text_input("Qdrant URL", value="http://localhost:6333")
docs_url = st.sidebar.text_input("Documentation URL")
voice_option = st.sidebar.selectbox("Edge TTS Voice", [
    "en-US-AriaNeural", "en-US-GuyNeural", "en-GB-RyanNeural"
])

# ---------------------------- Initialize System ----------------------------
if st.sidebar.button("Initialize System"):
    with st.spinner("Crawling documentation and creating knowledge base..."):
        firecrawl = Firecrawl(api_key=firecrawl_key)
        crawl = firecrawl.crawl(url=docs_url)
        content = "\n\n".join([p["text"] for p in crawl["pages"]])

        # Generate embeddings
        embed_model = DefaultEmbedding()
        docs = content.split("\n\n")
        embeddings = embed_model.embed(docs)

        # Push to Qdrant
        client = QdrantClient(url=qdrant_url)
        client.recreate_collection(
            collection_name="docs",
            vectors_config=models.VectorParams(size=embed_model.embedding_size, distance=models.Distance.COSINE),
        )
        points = [
            models.PointStruct(id=i, vector=embeddings[i], payload={"text": docs[i]})
            for i in range(len(docs))
        ]
        client.upsert(collection_name="docs", points=points)
        st.success("System initialized and ready to answer questions!")

# ---------------------------- Query Section ----------------------------
st.title(":speech_left: Customer Support Voice Agent")

question = st.text_input("Ask your question:")

if st.button("Submit") and question:
    with st.spinner("Searching knowledge base and generating response..."):
        embed_model = DefaultEmbedding()
        q_emb = embed_model.embed([question])[0]

        client = QdrantClient(url=qdrant_url)
        hits = client.search(
            collection_name="docs",
            query_vector=q_emb,
            limit=5
        )
        context = "\n".join([hit.payload["text"] for hit in hits if "text" in hit.payload])

        # Call Mistral LLM via Ollama
        prompt = f"""
        Answer the following question using the documentation context below:

        Context:
        {context}

        Question:
        {question}

        Answer:"""
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        answer = response['message']['content']

        st.session_state.messages.append((question, answer))

        # ---------------- TTS ----------------
        async def save_audio(text, voice):
            tts = edge_tts.Communicate(text, voice)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                await tts.save(f.name)
                return f.name

        path = asyncio.run(save_audio(answer, voice_option))
        st.session_state.audio_path = path

# ---------------------------- Display Messages ----------------------------
for q, a in st.session_state.messages[::-1]:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Agent:** {a}")

# ---------------------------- Audio Player ----------------------------
if st.session_state.audio_path:
    st.audio(st.session_state.audio_path)
