from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

# Amazon Bedrockとやり取りを行うためのライブラリをインポートします
from langchain_aws import ChatBedrock
# ユーザーとAIのやり取りを管理するためのライブラリをインポートします
from langchain_core.messages import HumanMessage, SystemMessage

# ChatBedrockのインスタンスを作成します
chat = ChatBedrock(
    model_id="the model id of Amazon Bedrock", # TODO: BedrockのモデルIDを指定して下さい
    model_kwargs={"max_tokens": 800}, # モデルに渡すパラメータを設定します。ここでは生成する最大トークン数を指定しています
    credentials_profile_name='the profile name', # TODO: プロファイル名を指定して下さい : ~/.aws/credentials or ~/.aws/config files. # AWSの認証情報を指定します
    region_name="us-east-1",
)

# AIに送信するメッセージを設定します
messages = [
    SystemMessage(content="あなたの役割は、質問に誠実かつ明確に答えることです。"), # AIの役割を定義します
    HumanMessage(content="東京都の中央区にある日本橋は、いつの時代に作られましたか？"), # ユーザーの質問を設定します
]

# AIモデルにメッセージを送信し、応答を受け取ります
response = chat.invoke(messages)

# AIからの応答を表示します
print(response.content)