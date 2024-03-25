#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 20:06:10 2023

@author: zhangte01
"""

import json
import re
import enum
from json import *


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, re.Pattern):
            return {"__regex_pattern__": obj.pattern}
        elif isinstance(obj, enum.Enum):
            return {"__enum__": obj.name}
        return super().default(obj)


def enhanced_decode(dct):
    if "__regex_pattern__" in dct:
        return re.compile(dct["__regex_pattern__"])
    elif "__enum__" in dct:
        # TODO: 没有考虑类型还原
        return dct["__enum__"]
    return dct


def dumps(obj, **kwargs):
    return json.dumps(obj, cls=EnhancedJSONEncoder, **kwargs)


def loads(s, **kwargs):
    return json.loads(s, object_hook=enhanced_decode, **kwargs)


__all__ = ["dumps", "loads", "JSONEncoder", "JSONDecodeError"] + [
    e for e in json.__all__ if e not in ["dumps", "loads"]
]
