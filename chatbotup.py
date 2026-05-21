import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Bry Polymer | Support", page_icon="💬", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');
html, body, [data-testid="stAppViewContainer"] { background: #EEF4F0; font-family: 'DM Sans', sans-serif; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stAppViewContainer"] > .main > div { padding-top: 2rem; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
.branding { text-align: center; padding: 2rem 0 1.5rem; }
.branding h1 { font-family: 'DM Serif Display', serif; font-size: 2rem; color: #1B75BC; margin: 0 0 .25rem; letter-spacing: -.5px; }
.branding p { font-size: .85rem; color: #5E8C2F; margin: 0; letter-spacing: .5px; text-transform: uppercase; font-weight: 600; }
.divider { width: 48px; height: 3px; background: linear-gradient(90deg, #1B75BC, #5E8C2F); border-radius: 2px; margin: .75rem auto 0; }
.msg-row { display: flex; margin-bottom: 1rem; align-items: flex-end; gap: .6rem; }
.msg-row.user { flex-direction: row-reverse; }
.avatar { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: .85rem; flex-shrink: 0; }
.avatar.bot { background: #1B75BC; color: #fff; font-weight: 700; }
.avatar.user { background: #5E8C2F; color: #fff; font-weight: 700; }
.bubble { max-width: 78%; padding: .75rem 1rem; border-radius: 16px; font-size: .92rem; line-height: 1.55; color: #1A1A1A; box-shadow: 0 1px 4px rgba(0,0,0,.07); }
.bubble.bot { background: #fff; border: 1px solid #D0E4F5; border-bottom-left-radius: 4px; }
.bubble.user { background: #1B75BC; color: #fff; border-bottom-right-radius: 4px; }
.chat-scroll { max-height: 54vh; overflow-y: auto; padding-right: 4px; margin-bottom: 1rem; }
.chat-scroll::-webkit-scrollbar { width: 4px; }
.chat-scroll::-webkit-scrollbar-thumb { background: #A8C8E8; border-radius: 4px; }
.stChatInput > div { border: 1.5px solid #B8D4E8 !important; border-radius: 12px !important; background: #fff !important; }
.stChatInput button { background: #1B75BC !important; border-radius: 8px !important; color: #fff !important; }
</style>
""", unsafe_allow_html=True)

API_KEY = "AIzaSyBBFUnkV28r5Ei9TzYIE17BhnwqJ7HK-kc"  # ← paste your key here

if "kb" not in st.session_state:
    try:
        with open("bry_polymer_dataset.txt", "r") as f:
            st.session_state.kb = f.read()
    except FileNotFoundError:
        st.error("⚠️ bry_polymer_dataset.txt not found. Place it in C:\\AI\\ and restart.")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("""
<div class="branding">
  <h1>Bry Polymer Industries</h1>
  <p>Customer Support</p>
  <div class="divider"></div>
</div>
""", unsafe_allow_html=True)  

chat_html = '<div class="chat-scroll">'
if not st.session_state.messages:
    chat_html += """<div class="msg-row"><div class="avatar bot">B</div>
    <div class="bubble bot">Hello! 👋 Welcome to <strong>Bry Polymer Industries</strong> support.<br>How can I assist you today?</div></div>"""
else:
    for msg in st.session_state.messages:
        role  = msg["role"]
        text  = msg["content"].replace("\n", "<br>")
        label = "B" if role == "assistant" else "U"
        side  = "bot" if role == "assistant" else "user"
        chat_html += f'<div class="msg-row {side}"><div class="avatar {side}">{label}</div><div class="bubble {side}">{text}</div></div>'
chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

user_input = st.chat_input("Ask about our products, pricing, availability…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner(""):

    system_prompt = f"""you are bry polymer industries customer care executive your job is to provide answers to the questions asked by the customers
you should answer them very politely, if there is any question out of the kb say you did not have that info, only refer kb and provide the answer
{st.session_state.kb}"""

    genai.configure(api_key="AIzaSyBBFUnkV28r5Ei9TzYIE17BhnwqJ7HK-kc")

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system_prompt
    )

    chat = model.start_chat()

    response = chat.send_message(user_input)

    reply = response.text

st.session_state.messages.append({"role": "assistant", "content": reply})

st.rerun()
