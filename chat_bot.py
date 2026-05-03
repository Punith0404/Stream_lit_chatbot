import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Chatbot", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, how can I help you today?"}
    ]

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful assistant."

role_option = st.sidebar.selectbox(
    "Role",
    ["Expert", "Teacher", "Jovial"]
)

if role_option == "Teacher":
    st.session_state.system_prompt = "You are a teacher who explains concepts step by step."
elif role_option == "Jovial":
    st.session_state.system_prompt = "You are a Jovial conversational partner."
elif role_option == "Expert":
    st.session_state.system_prompt = "You are an expert programmer who writes clean code."
else:
    st.session_state.system_prompt = "You are a helpful assistant."

if st.sidebar.button("Reset Chat"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, how can I help you today?"}
    ]
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Enter your message")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    messages = [{"role": "system", "content": st.session_state.system_prompt}]
    messages.extend(st.session_state.messages)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)