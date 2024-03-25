#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/12/11 16:40:25
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


from abc import abstractmethod
import enum
from typing import List, Optional

from pydantic import BaseModel, Field
from xagents.config import *



# 切片类型


class ContentType(str, enum.Enum):
    TABLE = "TABLE"
    TITLE = "TITLE"
    TEXT = "TEXT"
    PARSED_TABLE = "PARSED_TABLE"

# 切片


class Chunk(BaseModel):
    content: str = Field(description="chunk的内容")
    content_type: ContentType = Field(description="chunk类型", default=ContentType.TEXT)
    search_content: Optional[str] = Field(description="用来检索的内容", default=None)
    page_idx: int = Field(description="chunk在文档中的页码,从1开始")






class AbstractLoader:
    @abstractmethod
    def load(self, file_path: str) -> List[Chunk]:
        raise NotImplementedError
