# 🗣️ Local Doc Voice Agent

A cost-free, professional voice-powered assistant that analyzes `.txt` files or web docs and responds using a locally run AI model (Mistral) with natural speech output (via edge-tts).

## 🔧 Features
- 💬 Local LLM (Mistral via Ollama)
- 🔍 FastEmbed for semantic search
- 🧠 Qdrant for vector database indexing
- 🌐 Firecrawl for crawling website content
- 🔊 Text-to-speech using Edge TTS
- ⚡ Built with Streamlit

## 🚀 Getting Started

1. Clone this repo
```bash
git clone https://github.com/yourusername/local-doc-voice-agent.git
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
Upload a .txt file or crawl a webpage.

The document is chunked and embedded.

Your query is semantically matched via Qdrant.

Mistral generates a response from the top match.

The response is spoken using edge-tts.

