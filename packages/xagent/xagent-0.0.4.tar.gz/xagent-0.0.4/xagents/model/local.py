#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/02/20 15:47:53
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''






from typing import List, Dict


import requests
from snippets import *
from xagents.model import LLM, EMBD

from loguru import logger

# model = SentenceTransformer(model_name_or_path='/Users/chenhao/Documents/zhipu/deploy/model/m3e-base')
MOCK_SN = "你好，这是一条mock信息"

def call_sn_chat(messages: List[Dict], temperature=0.01, top_p=0.7, max_new_token=1024, **kwargs):
    # data = dict(inputs=messages[0])
    # url = "http://10.0.251.202:8080/generate"
    # resp = requests.post(url=url, json=data)
    # resp.raise_for_status()
    # content = resp.json()["generated_text"]
    content = MOCK_SN
    return None, content

def call_sn_embedding(contents: List[str]):
    embeddings = []
    url = "http://localhost:8009/embd"
    resp = requests.post(url=url, data=dict(text=contents))
    resp.raise_for_status()
    return resp.json()["data"]

class SN_EMBD(EMBD):

    def __init__(self,  batch_size=16, norm=True):
        self.batch_size = batch_size
        self.norm = norm

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        logger.info(f"embedding {len(texts)} with {self.batch_size=}")

        embeddings = []
        from tqdm import tqdm
        
        for idx, batch in tqdm(enumerate(batchify(texts, self.batch_size))):
            try:
                embds = call_sn_embedding(contents=batch)
                embeddings.extend(embds)
                pct = idx*self.batch_size/len(texts)
                logger.info(f"{idx*self.batch_size}/{len(texts)} [{pct:2.2%}] embeddings done")
            except Exception as e:
                logger.error(f"embedding service error")
                logger.error(batch)

                raise e
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        embedding = call_sn_embedding(contents=[text])[0]
        return embedding

    @classmethod
    def get_dim(cls) -> int:
        return 768


class SN_LLM(LLM):
    @classmethod
    def list_versions(cls):
        return [
            "v1.0.0",
        ]

    def __init__(self, name="ZETA", version="v1.0.0"):
        super().__init__(name=name, version=version)

    def generate(self, prompt, history=[], stream=True,
                 temperature=0.01, **kwargs):
        messages = history + [dict(role="user", content=prompt)]
        response = call_sn_chat(messages=messages,
                                  temperature=temperature, **kwargs)
        resp_message = response
        return (e for e in resp_message) if stream else resp_message


if __name__ == "__main__":

    # zeta_llm = SN_LLM()
    # resp = zeta_llm.generate("你好", stream=False)
    # print(f"llm resp:{resp}")

    zeta_embd = SN_EMBD()
    contents = ["万得", "金融"]
    embds = zeta_embd.embed_documents(texts=contents)
    print(f"embd num {len(embds)}")
    print(f"embd dim {len(embds[0])}")
