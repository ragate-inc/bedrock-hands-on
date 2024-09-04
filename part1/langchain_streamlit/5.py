import streamlit as st
from langchain_aws import ChatBedrock
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# タイトル
st.title("Amazon Bedrock")

# セッションIDを定義
if "session_id" not in st.session_state:
    st.session_state.session_id = "my_session_id"

# セッションに履歴を定義
if "history" not in st.session_state:
    st.session_state.history = DynamoDBChatMessageHistory(
        table_name="Amazon DynamoDB Table Name here", # TODO: Amazon DynamoDBのテーブル名を指定
        session_id=st.session_state.session_id
    )

# セッションにChainを定義
if "chain" not in st.session_state:
    # プロンプトを生成
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたの役割は、質問に誠実かつ明確に答えることです。"),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="human_message"),
        ]
    )

    # ChatBedrockを定義
    chat = ChatBedrock(
        model_id="the model id of Amazon Bedrock", # TODO: BedrockのモデルIDを指定して下さい
        model_kwargs={"max_tokens": 800},
        credentials_profile_name='the profile name', # TODO: プロファイル名を指定して下さい : ~/.aws/credentials or ~/.aws/config files.
        streaming=True,
    )

    # Chainを生成
    chain = prompt | chat
    st.session_state.chain = chain

# 履歴クリアボタンを画面表示
if st.button("履歴クリア"):
    st.session_state.history.clear()

# メッセージを画面表示
for message in st.session_state.history.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)

# チャット入力欄を定義
if prompt := st.chat_input("質問してください。"):
    # ユーザーの入力をメッセージに追加
    with st.chat_message("user"):
        st.markdown(prompt)

    # モデルの呼び出しと結果の画面表示
    with st.chat_message("assistant"):
        response = st.write_stream(
            st.session_state.chain.stream(
                {
                    "messages": st.session_state.history.messages,
                    "human_message": [HumanMessage(content=prompt)],
                },
                config={"configurable": {"session_id": st.session_state.session_id}},
            )
        )

    # 履歴に追加
    st.session_state.history.add_user_message(prompt)
    st.session_state.history.add_ai_message(response)
