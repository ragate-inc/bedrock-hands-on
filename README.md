# About part 1

## langchain_streamlit

```shell
# install packages
pip install -r ./part1/langchain_streamlit/requirements.txt

# run langchain_streamlit
streamlit run ./part1/langchain_streamlit/1.py --server.port 8080
streamlit run ./part1/langchain_streamlit/2.py --server.port 8080
streamlit run ./part1/langchain_streamlit/3.py --server.port 8080
streamlit run ./part1/langchain_streamlit/4.py --server.port 8080
streamlit run ./part1/langchain_streamlit/5.py --server.port 8080
```

# About part 2

## knowledge_bases

```shell
# install packages
pip install -r ./part2/knowledge_bases/requirements.txt

# run knowledge_bases
streamlit run ./part2/knowledge_bases/1.py --server.port 8080
```

## agent

```shell
# install packages
pip install -r ./part2/agent/requirements.txt

# run agent
streamlit run ./part2/agent/1.py --server.port 8080
```

# TIPS

## 端末への AWS クレデンシャル設定方法

```shell
aws configure
  AWS Access Key ID [None]: xxxx
  AWS Secret Access Key [None]: xxxx
  Default region name [None]: us-east-1
  Default output format [None]: yaml
```
