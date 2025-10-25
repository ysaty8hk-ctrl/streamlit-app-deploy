import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# アドバイザーの役割オプション
advisor_options = {
    "まくら販売アドバイザー": "あなたは快眠をサポートするまくら販売アドバイザーです。まくらの選び方や寝具の工夫を中心に、安全で快適なアドバイスを提供してください。",
    "医師": "あなたは医師です。睡眠に関する医学的な観点から、安全で信頼できるアドバイスを提供してください。"
}

# Streamlit UI
st.title("睡眠アドバイザー")
st.write("睡眠に関する質問にお答えします。")

# ラジオボタンで役割選択
selected_role = st.radio("アドバイザーの役割を選んでください", list(advisor_options.keys()))

# ユーザーの質問入力
user_question = st.text_area("あなたの質問を入力してください：", height=100)

# 実行ボタン
if st.button("実行"):
    if user_question.strip():
        # system メッセージを選択
        system_message = advisor_options[selected_role]
        
        try:
            # OpenAI API 呼び出し
            with st.spinner("回答を生成中..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_question}
                    ],
                    temperature=0.5
                )
            
            # 結果表示
            st.subheader(f"【{selected_role}の回答】")
            st.write(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.warning("質問を入力してください。")
