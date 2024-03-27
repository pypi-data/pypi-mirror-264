#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------
# @Time    : 2024/3/21 17:41
# @Version : 1.0
# @Author  : lvzhidong
# @For : 
# -------------------
import base64
import os

from apollo.jasypt.utils import get_md5_derived_key, des_encrypt


def encrypt(message, password):
    algorithm_block_size = 8
    key_obtention_iterations = 1000

    salt = os.urandom(algorithm_block_size)
    iv = os.urandom(algorithm_block_size)

    dk, iv = get_md5_derived_key(password, salt, key_obtention_iterations)
    enc_text = des_encrypt(message.encode(), dk, iv)

    result = salt + iv + enc_text

    # Base64 encoding
    encoded_string = base64.b64encode(result).decode()
    return encoded_string