import streamlit as st
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

# ページに表示するタイトルを設定します。
st.title("Amazon Bedrock")

# Amazon Bedrockとやり取りするためのChatBedrockオブジェクトを定義します。
chat = ChatBedrock(
    model_id="the model id of Amazon Bedrock",  # TODO: BedrockのモデルIDを指定して下さい。例：anthropic.claude-v2
    model_kwargs={"max_tokens": 800},  # モデルに渡す追加のパラメータを設定します。ここでは、生成する最大トークン数を指定しています。
    credentials_profile_name='the profile name',  # TODO: プロファイル名を指定して下さい。認証情報が格納されているプロファイルを指定します。例：'default' ~/.aws/credentials or ~/.aws/config files.
    streaming=True,  # ストリーミングモードを有効にします。これにより、応答を逐次的に受け取ることができます。
    region_name="us-east-1",
)

# 生成AIに最初に渡すメッセージを定義します。
# ここでは、AIの役割を「質問に誠実かつ明確に答えること」と設定しています。
messages = [
    SystemMessage(content="あなたの役割は、質問に誠実かつ明確に答えることです。"),
]

# ユーザーがチャットで入力したテキストを取得します。
if prompt := st.chat_input("何でも聞いてください。"):
    # ユーザーの入力をmessagesリストに追加します。
    messages.append(HumanMessage(content=prompt))

    # ユーザーが入力したテキストをチャット画面に表示します。
    with st.chat_message("user"):
        st.markdown(prompt)

    # Amazon Bedrockモデルを呼び出し、結果をチャット画面に表示します。
    with st.chat_message("assistant"):
        # stream()メソッドを使って、ストリーミングモードでモデルを実行します。
        # これにより、応答が逐次的に表示されます。
        st.write_stream(chat.stream(messages))