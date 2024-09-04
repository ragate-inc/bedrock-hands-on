import nest_asyncio
import streamlit as st
from bs4 import BeautifulSoup
from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_xml_agent
from langchain_aws import ChatBedrock
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage

nest_asyncio.apply()

# Web ページの内容を読み込む関数
def web_page_reader(url: str) -> str:
    loader = WebBaseLoader(url)
    content = loader.load()[0].page_content
    return content

# 検索ツールと Web ページ読み込みツールの設定
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name="duckduckgo-search",
        func=search.run,
        description="このツールは、ユーザーから検索キーワードを受け取り、Web上の最新情報を検索します。",
    ),
    Tool(
        name="WebBaseLoader",
        func=web_page_reader,
        description="このツールは、ユーザーからURLを渡された場合に内容をテキストを返却します。URLの文字列のみを受け付けます。",
    ),
]

# チャットモデルの設定
chat = ChatBedrock(
    model_id="the model id of Amazon Bedrock", # TODO: BedrockのモデルIDを指定して下さい
    model_kwargs={"max_tokens": 1500},
    credentials_profile_name='the profile name', # TODO: プロファイル名を指定して下さい : ~/.aws/credentials or ~/.aws/config files.
)

# エージェントの設定
agent = create_xml_agent(chat, tools, prompt=hub.pull("hwchase17/xml-agent-convo"))

agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# Streamlit アプリケーションの設定
st.title("Amazon Bedrock Agent")
messages = [SystemMessage(content="質問に対して必ず日本語で回答します。")]

# ユーザー入力の処理
prompt = st.chat_input("何でも聞いてください。")
if prompt:
    messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        # エージェント呼び出し
        result = agent_executor.invoke({"input": prompt})
        st.write(result["output"])
