
# HITESH-GPT 🎧☕

Persona-based AI mentor inspired by the teaching style of Hitesh Choudhary.  
Built with **Streamlit + OpenAI GPT-4.1-mini**, this app answers coding / career / consistency doubts in friendly Hinglish.

🔗 **Live demo:** https://persona-gpt-mwbo4wkogkik5mnvejal3q.streamlit.app/

---

## ✨ Features

- 🧠 **Persona chat** – HITESH-GPT replies in warm, casual Hinglish (bhai / yaar / dekho vibes).
- 👨‍💻 **Tech mentor** – Helps with MERN stack, backend APIs, DevOps basics, GenAI, roadmaps.
- 💬 **ChatGPT-style UI** – Centered chat, sticky input, dark theme, example prompts.
- 📚 **Recent questions sidebar** – Shows your last questions so you can revisit topics.
- 💸 **Cost estimator** – Rough token cost of the last AI reply (uses GPT-4.1-mini for low cost).
- 🔁 **New chat** – One-click button to clear chat and start fresh.

---

## 🏗 Tech Stack

- [Python 3.11+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI Python SDK](https://platform.openai.com/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🚀 Running locally

```bash
# 1. Clone the repo
git clone https://github.com/Weptsugar/Persona-Gpt.git
cd Persona-Gpt

# 2. Create and activate a virtual env (optional but recommended)
# python -m venv venv
# venv\Scripts\activate  (Windows)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file in the project root
echo OPENAI_API_KEY=your_api_key_here > .env

# 5. Run the app
python -m streamlit run app.py


App starts at:
👉 http://localhost:8501

🔑 Environment Variables

The app loads the API key from two places:

1️⃣ Locally (development)

Create .env file:

OPENAI_API_KEY=sk-xxxxx

2️⃣ Streamlit Cloud (production)

Add in Settings → Secrets:

OPENAI_API_KEY = "sk-xxxxx"

🧠 Persona Design

HITESH-GPT behaves like:

A friendly senior engineer / coding mentor

Explains concepts step-by-step

Gives project-based roadmaps

Helps with burnout, consistency and confusion

Uses Hinglish naturally ("bhai", "simple si baat", "dekho yaar")

Clear rule:
Does NOT claim to be the real Hitesh Choudhary.

📸 Screenshots

Add your screenshot here later

Example:

![HITESH-GPT UI](./screenshot.png)

📝 Future Improvements

Save chat history per user

Light/dark mode toggle

Multiple personas (DSA mentor, DevOps mentor, Career mentor)

PDF export of chat

Add image upload + vision model support

💼 Why I Built This

This project demonstrates:

Streamlit app development

OpenAI API integration

Prompt engineering & persona design

UI/UX styling with custom CSS

Deployment on Streamlit Cloud

Token cost optimization with GPT-4.1-mini

Useful for portfolio, resume, and cloud + AI experience.

⭐ Contribute / Feedback

Feel free to open issues or submit PRs.
Suggestions are always welcome!


---

# 🎉 You're all set!

This README is **professional, clean, and recruiter-ready**.  
It will make your GitHub project look solid.

---

# If you want next:

### ✔ Add badges  
### ✔ Add screenshot banner  
### ✔ Generate a LinkedIn announcement post  
### ✔ Improve UI further  
### ✔ Add light/dark theme switch  
### ✔ Add multiple personas

Just tell me **"Add badges"** or **"Give LinkedIn post"** etc