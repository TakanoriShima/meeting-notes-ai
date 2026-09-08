import streamlit as st
from google import genai
from pydantic import BaseModel, Field
import pandas as pd


# =========================
# Geminiから返してほしいデータ構造
# =========================

class Todo(BaseModel):
    task: str = Field(description="実施するタスク")
    owner: str = Field(description="担当者")
    due_date: str = Field(description="期限。分からない場合は空文字")


class MeetingNotes(BaseModel):
    summary: str = Field(description="会議内容の要約")
    decisions: list[str] = Field(description="会議で決定した事項")
    todos: list[Todo] = Field(description="会議で発生したタスク")


# =========================
# Streamlit画面
# =========================

st.title("会議メモ AI 構造化ツール")

st.write("会議メモを入力すると、Gemini APIで構造化します。")

meeting_text = st.text_area(
    "会議メモを入力してください",
    height=250,
    placeholder="例：\n田中さんと佐藤さんで営業会議を実施。\n新商品の発売日は10月1日に決定。\n田中さんが9月15日までに商品資料を作成する。"
)


# =========================
# Gemini API
# =========================

if st.button("会議メモを構造化する"):

    if not meeting_text.strip():
        st.warning("会議メモを入力してください。")
        st.stop()

    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

    prompt = f"""
以下の会議メモを分析し、指定された形式で整理してください。

会議メモ：
{meeting_text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": MeetingNotes.model_json_schema(),
        }
    )

    result = MeetingNotes.model_validate_json(response.text)

    st.subheader("構造化結果")

    st.write("### 要約")
    st.write(result.summary)

    st.write("### 決定事項")
    for decision in result.decisions:
        st.write(f"- {decision}")

    st.write("### TODO")
    for todo in result.todos:
        st.write(
            f"- **{todo.task}** / 担当：{todo.owner} / 期限：{todo.due_date}"
        )

    st.write("### JSON")
    st.json(result.model_dump())

    # JSONファイルとしてダウンロード
    json_data = result.model_dump_json(indent=2)

    st.download_button(
        label="JSONをダウンロード",
        data=json_data,
        file_name="meeting_notes.json",
        mime="application/json",
    )

    # CSV用のTODOデータを作成
    todo_data = [
        {
            "タスク": todo.task,
            "担当者": todo.owner,
            "期限": todo.due_date,
        }
        for todo in result.todos
    ]

    todo_df = pd.DataFrame(todo_data)

    st.write("### TODO一覧")

    st.dataframe(todo_df)

    # CSVに変換
    csv_data = todo_df.to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        label="CSVをダウンロード",
        data=csv_data,
        file_name="meeting_todos.csv",
        mime="text/csv",
    )    