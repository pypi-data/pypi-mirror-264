#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/02/20 17:39:31
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

from xagents.util import format_prompt

def test_format_prompt():
    prompt = "hello {name}"
    prompt = format_prompt(template=prompt, name="world", age=12)
    print(prompt)
    
    