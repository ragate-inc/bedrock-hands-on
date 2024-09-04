from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

# ChatBedrockを定義
chat = ChatBedrock(
    model_id="the model id of Amazon Bedrock", # TODO: BedrockのモデルIDを指定して下さい
    model_kwargs={"max_tokens": 800},
    credentials_profile_name='the profile name', # TODO: プロファイル名を指定して下さい : ~/.aws/credentials or ~/.aws/config files.
)

# 生成AIへ渡すメッセージを定義
messages = [
    SystemMessage(content="あなたの役割は、質問に誠実かつ明確に答えることです。"),
    HumanMessage(content="東京都の中央区にある日本橋は、いつの時代に作られましたか？"),
]

# モデルへAPIリクエスト
response = chat.invoke(messages)

print(response.content)