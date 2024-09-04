import nest_asyncio
import streamlit as st
from bs4 import BeautifulSoup
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_xml_agent
from langchain_aws import ChatBedrock
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage

# 非同期処理のための設定
nest_asyncio.apply()

# Web ページの内容を読み込む関数
def web_page_reader(url: str) -> str:
    """
    与えられたURLのWebページの内容を読み込み、テキストを返します。

    Args:
        url: WebページのURL

    Returns:
        Webページのテキストコンテンツ
    """
    loader = WebBaseLoader(url)  # Webページの読み込み
    content = loader.load()[0].page_content  # テキストコンテンツの抽出
    return content

# 検索ツールと Web ページ読み込みツールの設定
search = DuckDuckGoSearchRun()  # DuckDuckGo検索ツールのインスタンス化
tools = [
    Tool(
        name="duckduckgo-search",  # ツール名
        func=search.run,  # ツールの実行関数
        description="このツールは、ユーザーから検索キーワードを受け取り、Web上の最新情報を検索します。",  # ツールの説明
    ),
    Tool(
        name="WebBaseLoader",  # ツール名
        func=web_page_reader,  # ツールの実行関数
        description="このツールは、ユーザーからURLを渡された場合に内容をテキストを返却します。URLの文字列のみを受け付けます。",  # ツールの説明
    ),
]

# チャットモデルの設定
chat = ChatBedrock(
    model_id="the model id of Amazon Bedrock",  # TODO: BedrockのモデルIDを指定して下さい。例：anthropic.claude-v2
    model_kwargs={"max_tokens": 1500},  # モデルに渡す追加のパラメータ。ここでは、生成する最大トークン数を指定しています。
    credentials_profile_name='the profile name',  # TODO: プロファイル名を指定して下さい。認証情報が格納されているプロファイルを指定します。例：'default' ~/.aws/credentials or ~/.aws/config files.
)

# エージェントの設定
agent = create_xml_agent(chat, tools, prompt=hub.pull("hwchase17/xml-agent-convo"))  # XMLエージェントの作成

# エージェントの実行設定
agent_executor = AgentExecutor(
    agent=agent,  # 使用するエージェント
    tools=tools,  # 使用するツール
    verbose=True,  # 処理の詳細を表示するかどうか
    handle_parsing_errors=True  # パースエラーの処理方法
)

# Streamlit アプリケーションの設定
st.title("Amazon Bedrock Agent")  # アプリケーションのタイトル
messages = [SystemMessage(content="質問に対して必ず日本語で回答します。")]  # システムメッセージの初期化

# ユーザー入力の処理
prompt = st.chat_input("何でも聞いてください。")  # ユーザー入力を受け付けるチャット入力欄を表示
if prompt:  # ユーザーが入力した場合
    messages.append(HumanMessage(content=prompt))  # ユーザー入力をメッセージに追加
    with st.chat_message("user"):  # ユーザーの発言として表示
        st.markdown(prompt)
    with st.chat_message("assistant"):  # エージェントの応答として表示
        # エージェント呼び出し
        result = agent_executor.invoke({"input": prompt})  # エージェントを実行し、結果を受け取る
        st.write(result["output"])  # エージェントの応答を表示