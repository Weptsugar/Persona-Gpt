from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

# ---------- ENV + OPENAI SETUP ----------
load_dotenv()

# 1) Locally: read from .env
# 2) On Streamlit Cloud: read from st.secrets
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error(
        "OPENAI_API_KEY missing.\n\n"
        "• Locally: create a .env file with OPENAI_API_KEY=...\n"
        "• On Streamlit Cloud: add OPENAI_API_KEY in app Secrets."
    )
    st.stop()

client = OpenAI(api_key=api_key)

# ---------- SIMPLE COST CONFIG (gpt-4.1-mini) ----------
# Check latest prices on OpenAI pricing page if they change.
INPUT_PER_MILLION = 0.40   # $ per 1M input tokens (approx)
OUTPUT_PER_MILLION = 1.60  # $ per 1M output tokens (approx)

def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    return (
        (input_tokens / 1_000_000) * INPUT_PER_MILLION
        + (output_tokens / 1_000_000) * OUTPUT_PER_MILLION
    )

# ---------- PERSONA PROMPT ----------
persona = """
You are HITESH-GPT — a friendly, human-like Hinglish-speaking coding mentor
inspired by the teaching vibe of Hitesh Choudhary (but you are NOT the real person).

IDENTITY & EXPERTISE:
- You are an expert AI full-stack engineer and mentor.
- You understand MERN / modern frontend, backend APIs, databases, DevOps basics,
  as well as Gen AI, LLMs, and building real projects end-to-end.
- Your job is to take a student from zero to hero, step by step, without overwhelming them.

GENERAL TONE:
- Speak in warm, casual Hinglish.
- Use words like "bhai", "yaar", "dekho", "simple si baat".
- Sound like a real human mentor, not a robot.
- Be encouraging, chill and practical.
- Light humour allowed, but keep it clean and respectful.

HOW TO TEACH (ZERO TO HERO STYLE):
- Always break concepts into chhote-chhote, clear steps.
- When user is confused, reduce theory and increase simple examples / analogies.
- Whenever possible, give a short roadmap:
  - Step 1: …
  - Step 2: …
  - Step 3: …
- Focus on real-world learning: projects, GitHub, documentation, and small wins.

GREETING STYLE:
When conversation starts, greet like:
- "Haan ji bhai, kaise ho? Aaj kis topic pe baat karni hai?"
- "Namaste dosto! Chalo shuru karte hain, aaj kya seekhna hai?"

SPECIAL BEHAVIOUR EXAMPLES:

1) If user asks: "React kaise start karu?"
   - Suggest: HTML/CSS basics -> JavaScript basics -> React.
   - Recommend good YouTube playlists (for example "Chai aur Code") + official docs.
   - Emphasise: videos + documentation + chhote-chhote projects.

2) If user asks: "Gen AI kaha se padhu?"
   - Suggest: Python basics, thoda math intuition,
     phir Gen AI ke resources (YouTube, blogs, OpenAI/Hugging Face docs).
   - Recommend small hands-on projects: chatbots, summarizers, image apps.

3) If user says they feel burnout / stress / anxiety / demotivation:
   - First acknowledge feelings in a caring, human way.
   - Suggest break: family/friends ke sath time, khelna, hasna,
     thoda tech se door rehna.
   - Help them remember their "why".
   - Then give a very simple step-by-step comeback plan.
   - In these cases, you can use extra supportive lines.

4) If user asks about consistency / routine:
   - Suggest realistic daily target (1–2 ghante).
   - Fixed timing, habit building, tracking progress (calendar, streak).
   - Motivate: roz thoda karo, magar regular karo.

SUPPORTIVE LINES:
- Use supportive lines naturally, not in every answer.
- Especially use them when user sounds lost, demotivated, scared, or stuck.
- Examples:
  - "Koi dikkat ho to bina jhijhak puchho bhai, main yahi hoon help ke liye."
  - "Confusion hona normal hai, puchhne se hi clarity aati hai."
  - "Slow progress bhi progress hi hoti hai, tension mat lo."
  - "Hum milke step by step nikal lenge, tum akela feel mat karo."

RULES:
- Do NOT pretend to be the actual Hitesh Choudhary.
- Do NOT share private info of real people.
- You are HITESH-GPT, a helpful AI full-stack + Gen AI mentor bot with a similar friendly vibe.
- Focus on coding, tech career, mindset, and motivation.
- When user is tensed, your first priority is to lighten their burden and calm them down,
  then give a simple, actionable plan.
"""

# ---------- STREAMLIT PAGE CONFIG ----------
st.set_page_config(
    page_title="HITESH-GPT",
    page_icon="☕",
    layout="wide",
)

# ---------- GLOBAL STYLING ----------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #22c55e11, #020617 55%, #000000 100%);
        color: #e5e7eb;
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .main { padding-top: 1rem; padding-bottom: 0; }
    h1, h2, h3, h4 { color: #f9fafb; letter-spacing: 0.04em; }
    .neon-text { color: #22c55e; text-shadow: 0 0 12px #22c55eaa; }
    .block-container { max-width: 900px !important; padding-top: 1.2rem !important; }

    .subtitle-quote {
        font-size: 13px;
        color: #9ca3af;
        margin-top: 0.2rem;
        margin-bottom: 0.6rem;
    }
    .subtitle-quote span { color: #e5e7eb; font-style: italic; }

    .header-card {
        border-radius: 18px;
        border: 1px solid rgba(31, 41, 55, 0.85);
        background: linear-gradient(135deg, #020617ee, #020617cc);
        padding: 14px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 0.6rem;
    }
    .header-badge {
        font-size: 11px;
        padding: 4px 10px;
        border-radius: 999px;
        border: 1px solid #22c55eaa;
        background: radial-gradient(circle at top left, #22c55e22, #022c22cc);
        color: #bbf7d0;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 999px;
        background: #22c55e;
        box-shadow: 0 0 0 0 rgba(34,197,94,0.8);
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.8); }
        70% { box-shadow: 0 0 0 10px rgba(34,197,94,0); }
        100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
    }
    .header-text-main { font-size: 13px; color: #9ca3af; }
    .chip-row { display:flex; flex-wrap:wrap; gap:6px; margin-top:6px; }
    .chip {
        font-size:11px; padding:4px 10px; border-radius:999px;
        border:1px solid #374151; background:#020617; color:#e5e7eb; opacity:0.9;
    }

    .stChatMessage { padding: 0; }
    .stChatMessage .stMarkdown { width:100%; }
    .stChatMessage [data-testid="stMarkdownContainer"] { width:100%; }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) [data-testid="stMarkdownContainer"] {
        background: linear-gradient(135deg, #020617, #020617f0);
        border-radius: 16px; padding: 10px 13px; border: 1px solid #1f2937;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) [data-testid="stMarkdownContainer"] {
        background: linear-gradient(135deg, #16a34a33, #15803d55);
        border-radius: 16px; padding: 10px 13px; border: 1px solid #16a34a99;
    }

    div[data-testid="stChatInputContainer"] {
        position: sticky; bottom: 0; z-index: 999;
        border-top: 1px solid rgba(31, 41, 55, 0.9);
        background: linear-gradient(180deg, transparent, rgba(15,23,42,0.95));
        backdrop-filter: blur(12px);
    }
    div[data-testid="stChatInputContainer"] textarea {
        border-radius: 999px !important;
        border: 1px solid rgba(55,65,81,0.9) !important;
        background: radial-gradient(circle at top left, #22c55e11, #020617ee) !important;
        color: #e5e7eb !important;
        font-size: 0.9rem !important;
    }
    div[data-testid="stChatInputContainer"] button {
        border-radius: 999px !important;
        background: linear-gradient(135deg, #22c55e, #16a34a) !important;
        color: #022c22 !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 12px 25px rgba(22,163,74,0.45) !important;
    }

    .stButton>button {
        border-radius: 999px;
        border: 1px solid rgba(55, 65, 81, 0.9);
        background: radial-gradient(circle at top left, #22c55e22, #020617ee);
        color: #f9fafb;
        font-size: 0.8rem;
        padding: 0.4rem 0.7rem;
        transition: all 0.16s ease-out;
    }
    .stButton>button:hover {
        border-color: #22c55e;
        box-shadow: 0 0 0 1px #22c55e77, 0 8px 20px rgba(15,23,42,0.9);
        transform: translateY(-1px);
        background: radial-gradient(circle at top left, #22c55e33, #020617ee);
    }

    section[data-testid="stSidebar"] {
        background: radial-gradient(circle at top left, #22c55e11, #020617 60%);
        border-right: 1px solid #111827;
    }
    .sidebar-title { font-size: 15px; font-weight: 600; color: #e5e7eb; margin-bottom: 6px; }
    .sidebar-item { font-size: 13px; color: #9ca3af; margin-bottom: 6px; }
    .sidebar-footer { font-size: 11px; color: #6b7280; margin-top: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Haan ji bhai, kaise ho? Main HITESH-GPT hoon. Aaj kis topic pe baat karni hai? 🙂",
        }
    ]

if "history" not in st.session_state:
    st.session_state.history = []

if "last_cost" not in st.session_state:
    st.session_state.last_cost = 0.0

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>💬 Recent questions</div>", unsafe_allow_html=True)
    if st.session_state.history:
        for i, q in enumerate(reversed(st.session_state.history[-12:]), start=1):
            st.markdown(f"<div class='sidebar-item'>{i}. {q}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='sidebar-item'>Abhi tak koi question nahi. Start a chat on the right side. 👈</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---", unsafe_allow_html=True)
    st.markdown(
        f"<div class='sidebar-footer'>"
        f"Last reply approx cost: <b>${st.session_state.last_cost:.5f}</b><br/>"
        f"HITESH-GPT • AI full-stack mentor."
        f"</div>",
        unsafe_allow_html=True,
    )

# ---------- HEADER ----------
st.markdown(
    "<h1 style='text-align:center; margin-bottom:0.1rem;' class='neon-text'>HITESH-GPT</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p class="subtitle-quote" style="text-align:center;">
      <span>"Code sikhna mushkil nahi hai, mushkil consistency aur discipline hai."</span>
    </p>
    """,
    unsafe_allow_html=True,
)

left_header, right_header = st.columns([4, 1])

with left_header:
    st.markdown(
        """
        <div class="header-card">
          <div style="display:flex; flex-direction:column; gap:4px;">
            <div class="header-badge">
              <span class="pulse-dot"></span>
              HITESH-GPT • AI Full-Stack Mentor
            </div>
            <div class="header-text-main">
              Coding, career, mindset — sab ke liye ek hi jagah. Hinglish mein zero se hero tak.
            </div>
            <div class="chip-row">
              <div class="chip">React & Frontend</div>
              <div class="chip">Backend & APIs</div>
              <div class="chip">Gen AI & LLMs</div>
              <div class="chip">Roadmaps</div>
              <div class="chip">Motivation</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_header:
    if st.button("🧹 New chat / Clear"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Haan ji bhai, kaise ho? Main HITESH-GPT hoon. Aaj kis topic pe baat karni hai? 🙂",
            }
        ]
        # keep history so you can still see old questions
        st.rerun()

# ---------- EXAMPLE PROMPTS ----------
example_prompt = None
st.markdown(
    """
    <div style="margin-top:0.3rem; margin-bottom:0.4rem; font-size:12px; color:#9ca3af;">
      Jaldi start karna hai? Inme se koi bhi prompt try karo:
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("React kaise start karu?"):
        example_prompt = "React kaise start karu?"
with c2:
    if st.button("Gen AI kaha se padhu?"):
        example_prompt = "Gen AI kaha se padhu?"
with c3:
    if st.button("Burnout feel ho raha hai, kya karu?"):
        example_prompt = "Burnout feel ho raha hai, kya karu?"
with c4:
    if st.button("Consistency kaise banaye rakhu?"):
        example_prompt = "Consistency kaise banaye rakhu?"

st.markdown("<hr style='border-color:#111827;'/>", unsafe_allow_html=True)

# ---------- CHAT HISTORY DISPLAY ----------
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------- CHAT INPUT ----------
user_prompt = st.chat_input("Hitesh-style AI full-stack mentor se kuch bhi puchhiye...")
final_prompt = user_prompt or example_prompt

if final_prompt:
    st.session_state.history.append(final_prompt)

    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)

    recent_messages = st.session_state.messages[-8:]

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": persona},
                *recent_messages,
            ],
            max_tokens=600,  # safety cap
        )
        bot_reply = response.choices[0].message.content
        usage = response.usage  # should contain input_tokens & output_tokens

        input_tokens = getattr(usage, "prompt_tokens", 0)
        output_tokens = getattr(usage, "completion_tokens", 0)
        st.session_state.last_cost = estimate_cost(input_tokens, output_tokens)

    except Exception as e:
        bot_reply = (
            "Arre bhai, kuch error aa gaya 😅\n\n"
            f"`{e}`\n\nConfig ya network ek baar check kar lo."
        )
        st.session_state.last_cost = 0.0

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
