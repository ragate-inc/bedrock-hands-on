import streamlit as st
from langchain_aws import ChatBedrock
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

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

# セッション状態にメッセージを保存するためのリストを初期化します。
# これにより、ページが再読み込みされても、過去のメッセージが保持されます。
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="あなたの役割は、質問に誠実かつ明確に答えることです。"),  # AIの役割を定義するシステムメッセージを初期化します。
    ]

# 過去のメッセージをチャット画面に表示します。
for message in st.session_state.messages:
    # システムメッセージは表示しないようにします。
    if message.type != "system":
        with st.chat_message(message.type):
            st.markdown(message.content)

# ユーザーがチャットで入力したテキストを取得します。
if prompt := st.chat_input("何でも聞いてください。"):
    # ユーザーの入力をセッション状態のメッセージリストに追加します。
    st.session_state.messages.append(HumanMessage(content=prompt))

    # ユーザーが入力したテキストをチャット画面に表示します。
    with st.chat_message("user"):
        st.markdown(prompt)

    # Amazon Bedrockモデルを呼び出し、結果をチャット画面に表示します。
    with st.chat_message("assistant"):
        # stream()メソッドを使って、ストリーミングモードでモデルを実行します。
        # これにより、応答が逐次的に表示されます。
        response = st.write_stream(chat.stream(st.session_state.messages))
    
    # モデルからの応答をセッション状態のメッセージリストに追加します。
    st.session_state.messages.append(AIMessage(content=response))