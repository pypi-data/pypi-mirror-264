#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------
# @Time    : 2024/3/21 17:01
# @Version : 1.0
# @Author  : lvzhidong
# @For : 
# -------------------
import base64
import re

from apollo.jasypt.utils import get_md5_derived_key, des_decrypt

algorithm_block_size = 8
key_obtention_iterations = 1000


def decrypt(message, password):
    # Base64 decoding
    encrypted = base64.b64decode(message)

    salt = encrypted[:algorithm_block_size]
    encrypted = encrypted[algorithm_block_size:]

    iv = encrypted[:algorithm_block_size]
    encrypted = encrypted[algorithm_block_size:]

    dk, iv = get_md5_derived_key(password, salt, key_obtention_iterations)
    text = des_decrypt(encrypted, dk, iv)

    # Remove control characters
    text = re.sub(r"[\x01-\x08]", "", text.decode())

    return text