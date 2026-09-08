import streamlit as st
from google import genai

st.title("会議メモ AI 構造化ツール")

st.write("Gemini APIとの接続テスト")

if st.button("Gemini APIをテストする"):
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="こんにちは。これはAPI接続テストです。短く返答してください。"
    )

    st.write(response.text)