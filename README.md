# 🗣️ Local Doc Voice Agent

🎙️ Local Doc Voice Agent (Local + Cost-Free)

A professional, local-first customer support agent application that delivers voice-powered responses to documentation-based queries. It uses the **Mistral LLM (via Ollama)** for AI reasoning and **Edge-TTS** for natural speech — all completely **cost-free**. The system crawls documentation websites using **Firecrawl**, processes the content into a searchable vector store with **Qdrant**, and provides both text and audio responses to user queries via a clean **Streamlit UI**.

---

## 🚀 Features

### 🔍 Knowledge Base Creation

- Crawls documentation websites using **Firecrawl**
- Stores and indexes content using **Qdrant** vector database
- Generates embeddings using **FastEmbed** for semantic search

### 🤖 AI Agent Team

- **Local LLM Processor** (Mistral via Ollama): Analyzes documents and generates concise responses
- **TTS Agent**: Converts text to voice using **Edge-TTS**
- Supports multiple **Microsoft Edge** voices (female/male, multi-language)

### 🎛️ Interactive Interface

- Clean **Streamlit** dashboard with sidebar controls
- Real-time query handling and semantic search
- Audio player with playback and download option
- Progress bars for crawling, indexing, and inference steps

---

## ⚙️ How to Run
1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/local-doc-voice-agent.git
cd local-doc-voice-agent

```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Start Ollama (Local LLM)
```
ollama run mistral
```
Make sure Ollama is installed: https://ollama.com

4. Run the app
```
streamlit run ai_voice_agent_docs.py
```
🧠 How It Works
User provides a .txt file or a documentation URL

System uses Firecrawl to gather web content

The text is embedded with FastEmbed

Qdrant is used for similarity search

Top-matching chunks are passed to Mistral via Ollama

Final response is synthesized with Edge-TTS

Response is shown as both text and voice


