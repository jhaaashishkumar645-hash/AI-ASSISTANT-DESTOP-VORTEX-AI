# 🤖 Desktop Vortex AI Assistant

**Desktop Vortex AI** is a high-performance, Python-based intelligent voice assistant designed to bridge the gap between human intent and desktop automation. By leveraging **Speech-to-Text (STT)**, **Large Language Models (LLMs)**, and **OS-level integration**, it transforms your computer into a voice-controlled powerhouse.

Whether you're looking to automate repetitive tasks, fetch real-time data, or engage in AI-driven conversation, Vortex provides a hands-free, seamless experience.

---

## 🚀 Key Features

* **🎤 Intelligent Voice Recognition:** Powered by `SpeechRecognition` with ambient noise adjustment for high accuracy.
* **🧠 Brain of the Vortex:** Integration with **OpenAI / Groq APIs** for context-aware, human-like responses.
* **🔊 Natural Synthesis:** Uses `Pyttsx3` for offline text-to-speech, ensuring your assistant responds even without a high-speed connection.
* **🌐 Web & Media Mastery:**
    * Instant YouTube playback via `PyWhatKit`.
    * Deep web searching and automated browser navigation.
* **☁️ Real-time Intelligence:** Live weather fetching and global news briefings via REST APIs.
* **💻 System Automation:** Launch local applications, manage files, and control system volume or power states using the `OS` module.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **AI/LLM** | OpenAI GPT-4 / Groq (Llama 3) |
| **Voice Processing** | SpeechRecognition (Google Web Speech API) |
| **Speech Synthesis** | Pyttsx3 (SAPI5 / NSSpeechSynthesizer) |
| **Automation** | PyWhatKit, Webbrowser, OS Module |
| **Data Fetching** | Requests, BeautifulSoup4 |

---

## 📂 Project Structure

```text
desktop-vortex-ai/
├── src/
│   ├── main.py           # Application entry point & listener loop
│   ├── engine/           # TTS and STT configuration
│   ├── brains/           # AI API integrations (OpenAI/Groq)
│   ├── actions/          # Automation scripts (Web, System, Apps)
│   └── utils/            # Helpers (Weather, News, Logger)
├── config/
│   └── settings.yaml     # Assistant name, voice rate, and preferences
├── requirements.txt      # Project dependencies
└── .env                  # Private API Keys (Hidden)
