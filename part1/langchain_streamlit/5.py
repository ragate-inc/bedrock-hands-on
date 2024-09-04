import streamlit as st
from langchain_aws import ChatBedrock
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import boto3

boto3.setup_default_session(profile_name='your profile name') # TODO: プロファイル名を指定してください(DynamoDBChatMessageHistoryでboto3を使用する為)

# ページに表示するタイトルを設定します。
st.title("Amazon Bedrock")

# セッションIDを定義します。セッションIDは、各ユーザーのチャット履歴を区別するために使用されます。
if "session_id" not in st.session_state:
    st.session_state.session_id = "session_id"

# チャット履歴をAmazon DynamoDBに保存するためのDynamoDBChatMessageHistoryオブジェクトを定義します。
if "history" not in st.session_state:
    st.session_state.history = DynamoDBChatMessageHistory(
        table_name="BedrockChatSessionTable",  # TODO: Amazon DynamoDBのテーブル名を指定してください。
        session_id=st.session_state.session_id
    )

# チャットボットの処理を行うChainオブジェクトを定義します。
if "chain" not in st.session_state:
    # プロンプトを定義します。プロンプトは、AIがどのように応答するかを制御するために使用されます。
    # ここでは、AIの役割を「質問に誠実かつ明確に答えること」と設定し、過去のメッセージと現在のメッセージをプレースホルダーとして使用しています。
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたの役割は、質問に誠実かつ明確に答えることです。"),
            MessagesPlaceholder(variable_name="messages"),  # 過去のメッセージのプレースホルダー
            MessagesPlaceholder(variable_name="human_message"),  # 現在のメッセージのプレースホルダー
        ]
    )

    # Amazon Bedrockとやり取りするためのChatBedrockオブジェクトを定義します。
    chat = ChatBedrock(
        model_id="the model id of Amazon Bedrock",  # TODO: BedrockのモデルIDを指定して下さい。例：anthropic.claude-v2
        model_kwargs={"max_tokens": 800},  # モデルに渡す追加のパラメータを設定します。ここでは、生成する最大トークン数を指定しています。
        credentials_profile_name='the profile name',  # TODO: プロファイル名を指定して下さい。認証情報が格納されているプロファイルを指定します。例：'default' ~/.aws/credentials or ~/.aws/config files.
        streaming=True,  # ストリーミングモードを有効にします。これにより、応答を逐次的に受け取ることができます。
        region_name="us-east-1",
    )

    # プロンプトとChatBedrockオブジェクトを組み合わせて、Chainオブジェクトを生成します。
    chain = prompt | chat
    st.session_state.chain = chain

# "履歴クリア"ボタンを表示し、クリックされた場合はチャット履歴をクリアします。
if st.button("履歴クリア"):
    st.session_state.history.clear()

# 過去のメッセージをチャット画面に表示します。
for message in st.session_state.history.messages:
    with st.chat_message(message.type):
        st.markdown(message.content)

# ユーザーがチャットで入力したテキストを取得します。
if prompt := st.chat_input("質問してください。"):
    # ユーザーの入力をチャット画面に表示します。
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chainオブジェクトを使って、AIに回答を生成させます。
    with st.chat_message("assistant"):
        # stream()メソッドを使って、ストリーミングモードでモデルを実行します。
        # これにより、応答が逐次的に表示されます。
        response = st.write_stream(
            st.session_state.chain.stream(
                {
                    "messages": st.session_state.history.messages,  # 過去のメッセージを渡します。
                    "human_message": [HumanMessage(content=prompt)],  # ユーザーの入力を渡します。
                },
                config={"configurable": {"session_id": st.session_state.session_id}},  # セッションIDを渡します。
            )
        )

    # ユーザーの入力とAIの応答をチャット履歴に追加します。
    st.session_state.history.add_user_message(prompt)
    st.session_state.history.add_ai_message(response)