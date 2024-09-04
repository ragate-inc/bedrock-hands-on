from langchain.globals import set_debug
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage

# デバッグモードを有効にする
set_debug(True)

# Amazon Bedrockとやりとりを行うためのChatBedrockオブジェクトを作成
chat = ChatBedrock(
    model_id="the model id of Amazon Bedrock", # TODO: 利用するBedrockのモデルIDを設定してください
    model_kwargs={"max_tokens": 800}, # モデルに渡すパラメータを設定します。ここでは生成する最大トークン数を指定しています
    credentials_profile_name='the profile name', # TODO: AWSの認証情報が記載されたプロファイル名を設定してください。認証情報は~/.aws/credentials や ~/.aws/config ファイルに記述されています。
)

# 生成AIに送信するメッセージを定義します
messages = [
    SystemMessage(content="あなたの役割は、質問に誠実かつ明確に答えることです。"), # AIの振る舞いを定義するシステムメッセージ
    HumanMessage(content="東京都の中央区にある日本橋は、いつの時代に作られましたか？"), # AIに投げかける質問
]

# 定義したメッセージを用いて、Bedrockのモデルに対してAPIリクエストを送信し、応答を受け取ります
response = chat.invoke(messages)

# 応答の内容を表示します
print(response.content)