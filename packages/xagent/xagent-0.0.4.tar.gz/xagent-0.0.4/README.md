# XAgents

XAgents项目为在大模型服务基础上的中间件，为了避免各个业务线重复开发，提供统一的程序接口，快速支持各种业务的需求

## 主要能力

- 接入各种模型服务，包括zhipu sdk, 本地LLM，embedding模型，rerank模型，NLU模型等
- 知识库的管理
- RAG的能力
- 工具调用的能力

具体设计参考[文档](https://zhipu-ai.feishu.cn/docx/Y78IdJZSmoESK0x0HZpc7vrWnde)

## 接入方式

### python SDK（python程序快速接入）

#### install

基于python3.10以上版本
  `pip install -U xagent`

#### 本地知识库

参考 tutorial/local_kb.py

#### 服务端知识库

参考 tutorial/remote_kb.py

#### http Service

  `curl --location --request POST 'http://117.50.174.44:8001/kb/list' \ --header 'Authorization: Basic emhpcHU6emhpcHU=' `

具体接口文档参考 http://117.50.174.44:8001/docs


## Release Note
