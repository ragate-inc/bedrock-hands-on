import streamlit as st
from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# タイトル
st.title("Amazon Bedrock")

# ChatBedrockを定義
chat = ChatBedrock(
    model_id="the model id of Amazon Bedrock", # TODO: BedrockのモデルIDを指定して下さい
    model_kwargs={"max_tokens": 800},
    credentials_profile_name='the profile name', # TODO: プロファイル名を指定して下さい : ~/.aws/credentials or ~/.aws/config files.
    streaming=True,
)

# セッションにメッセージを定義
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="あなたの役割は、質問に誠実かつ明確に答えることです。"),
    ]

# メッセージを画面表示
for message in st.session_state.messages:
    if message.type != "system":
        with st.chat_message(message.type):
            st.markdown(message.content)

# チャット入力欄を定義
if prompt := st.chat_input("何でも聞いてください。"):
    # ユーザーの入力をメッセージに追加
    st.session_state.messages.append(HumanMessage(content=prompt))

    # ユーザーの入力を画面表示
    with st.chat_message("user"):
        st.markdown(prompt)

    # モデルの呼び出しと結果の画面表示
    with st.chat_message("assistant"):
        response = st.write_stream(chat.stream(st.session_state.messages))
        
    # モデルへAPIリクエスト結果をメッセージに追加
    st.session_state.messages.append(AIMessage(content=response))
