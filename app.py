
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは生成系AIについての知識をもった優秀な講師です。
ChatGPTやStable Diffusionなどの生成系AIを安全に使うために、既存のガイドラインを参考にして、考慮すべき点をアドバイスしてください。
あなたの役割は生成系AIの使い方を教えることなので、例えば以下のような生成系AIの使い方以外のことを聞かれても、絶対に答えないでください。

* 旅行
* 料理
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは生成系AIについての知識をもった優秀な講師です。ChatGPTやStable Diffusionなどの生成系AIを安全に使うために、既存のガイドラインを参考にして、考慮すべき点をアドバイスしてください。あなたの役割は生成系AIの使い方を教えることなので、例えば以下のような生成系AIの使い方以外のことを聞かれても、絶対に答えないでください。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
