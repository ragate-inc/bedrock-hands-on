import streamlit as st
from langchain_aws import ChatBedrock
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Amazon Knowledge Basesから情報を検索するためのRetrieverオブジェクトを定義します。
retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id="the knowledge bases id",  # TODO: ここにナレッジベースIDを指定してください。例：'abcd-1234'
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 10}},  # 検索の設定。ここでは、最大10件の結果を取得するように設定しています。
)

# チャットボットが回答を生成するためのプロンプトテンプレートを定義します。
# このテンプレートは、検索結果とユーザーの質問を組み合わせて、チャットボットが理解しやすい形式に整形します。
prompt = ChatPromptTemplate.from_template(
    "以下のcontextに基づいて回答してください: {context} / 質問: {question}"
)

# Amazon Bedrockとやり取りするためのChatBedrockオブジェクトを定義します。
model = ChatBedrock(
    model_id="the model id of Amazon Bedrock",  # TODO: BedrockのモデルIDを指定して下さい。例：anthropic.claude-v2
    model_kwargs={"max_tokens": 800},  # モデルに渡す追加のパラメータを設定します。ここでは、生成する最大トークン数を指定しています。
    credentials_profile_name='the profile name',  # TODO: プロファイル名を指定して下さい。認証情報が格納されているプロファイルを指定します。例：'default' ~/.aws/credentials or ~/.aws/config files.
)

# 検索、プロンプト作成、LLM呼び出し、結果取得の一連の流れを定義します。
# このチェーンは、ユーザーの質問を受け取り、検索結果に基づいて回答を生成します。
chain = (
    {"context": retriever, "question": RunnablePassthrough()}  # 検索を実行し、結果とユーザーの質問を次のステップに渡します。
    | prompt  # 検索結果とユーザーの質問を使ってプロンプトを生成します。
    | model  # 生成されたプロンプトをLLMに渡して回答を生成します。
    | StrOutputParser()  # LLMからの回答を文字列に変換します。
)

# Streamlitアプリケーションのフロントエンドを定義します。
st.title("Amazon Bedrock")  # アプリケーションのタイトル
question = st.text_input("質問を入力")  # ユーザーが質問を入力するためのテキスト入力欄を表示します。
button = st.button("質問する")  # 質問を送信するためのボタンを表示します。

# ボタンがクリックされた場合に、チャットボットの回答を生成して表示します。
if button:
    st.write(chain.invoke(question))  # チェーンを実行し、結果を表示します。