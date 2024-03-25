#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/03/19 16:24:43
@Author  :   ChenHao
@Description  : 文档处理对外接口
@Contact :   jerrychen1990@gmail.com
'''

import os
from loguru import logger
from typing import List, Type
from xagents.loader.pdf import PDFLoader
from xagents.loader.markdown import MarkDownLoader
from xagents.loader.structed import StructedLoader
from xagents.loader.common import Chunk, AbstractLoader

from xagents.loader.splitter import BaseSplitter
from snippets import flat

_EXT2LOADER = {
    "pdf": PDFLoader,
    "markdown": MarkDownLoader,
    "md": MarkDownLoader,
    "json": StructedLoader,
    "jsonl": StructedLoader,
    "csv": StructedLoader,
    "txt": MarkDownLoader,
    "": MarkDownLoader
}


def get_loader_cls(file_path: str) -> Type[AbstractLoader]:
    ext = os.path.splitext(file_path)[-1].lower().replace(".", "")
    loader_cls = _EXT2LOADER[ext]    
    return loader_cls

def load_file(file_path: str, **kwargs) -> List[Chunk]:
    loader_cls = get_loader_cls(file_path)
    loader: AbstractLoader = loader_cls(**kwargs)
    logger.debug(f"loading {file_path} with loader:{loader}")
    contents = loader.load(file_path)
    return contents

def convert2txt(file_path:str, dst_path:str=None, **kwargs)->str:
    """将原始文件转移成

    Args:
        file_path (str): 原始文件路径
        dst_path (str, optional): 目标路径，未传的话，和原始文件同目录. Defaults to None.

    Returns:
        str: 目标路径
    """
    chunks = load_file(file_path, **kwargs)
    if not dst_path:
        dst_path =file_path+".txt"
    with open(dst_path, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk.content)
    return dst_path







def parse_file(file_path: str,
               separator: str = '\n',
               max_len: int = 200,
               min_len: int = 10) -> List[Chunk]:
    """切分文档，并且按照jsonl格式存储在chunk目录下

    Args:
        kb_name (str): 知识库名称
        file_name (str): 文件名称
        separator (str, optional): 切分符. Defaults to '\n'.
        max_len (int, optional): 最大切片长度. Defaults to 200.
        min_len (int, optional): 最小切片长度. Defaults to 10.

    Returns:
        int: 切片数目
    """
    splitter = BaseSplitter(max_len=max_len, min_len=min_len, separator=separator)

    origin_chunks: List[Chunk] = load_file(file_path=file_path)
    logger.debug(f"load {len(origin_chunks)} origin_chunks")
    
    split_chunks = flat([splitter.split_chunk(origin_chunk) for origin_chunk in origin_chunks])
    logger.info(f"split {len(origin_chunks)} origin_chunks to {len(split_chunks)} chunks")
    return split_chunks