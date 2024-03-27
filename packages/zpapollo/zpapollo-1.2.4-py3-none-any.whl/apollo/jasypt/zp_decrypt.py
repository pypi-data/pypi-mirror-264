#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------
# @Time    : 2024/3/21 18:21
# @Version : 1.0
# @Author  : lvzhidong
# @For : 
# -------------------
import logging
import os
import re

from apollo.jasypt.decrypt import decrypt
from apollo.jasypt.utils import aes_base64_decrypt

log = logging.getLogger("Apollo")

defaultEncPrefix = "ZPENC("  # 默认加密前缀
defaultEncSuffix = ")ZPENC"  # 默认加密后缀
CRYPT_PASSWORD_SECRET_ENV = "CRYPT_PASSWORD_SECRET"  # 密码加密密文的环境变量名
CRYPT_KEY_IV_ENV = "CRYPT_KEY_IV"
password = ""  # 密码
initedPassword = False  # 密码是否已初始化标志


def init_zp_decrypt_password():
    """
    初始化密码
    """
    global initedPassword, password
    if initedPassword:
        return True
    secret = os.getenv(CRYPT_PASSWORD_SECRET_ENV)
    if secret == "":
        log.error("InitCryptPassword secret is empty")
        return

    key_iv = os.getenv(CRYPT_KEY_IV_ENV)
    if not key_iv:
        log.error("InitCryptPassword key_iv is empty")
        return

    items = key_iv.split("-")
    if len(items) != 2:
        log.error("incorrect key_iv format")
        return
    key = items[0].encode()
    iv = items[1].encode()

    try:
        secret = aes_base64_decrypt(secret, key, iv)
    except Exception as e:
        log.error("get secret fail, please ensure env [{}] [{}] is right. err: {}"
                  .format(CRYPT_PASSWORD_SECRET_ENV, CRYPT_KEY_IV_ENV, e))
        return
    if secret is None:
        log.error("InitCryptPassword Decrypt error")
        return
    password = secret
    initedPassword = True
    log.info("InitCryptPassword successfully!")

    return True


def translate(encode):
    """
    替换函数
    """
    try:
        prefix_index = encode.find(defaultEncPrefix)
        suffix_index = encode.find(defaultEncSuffix)
        if prefix_index != 0 or suffix_index != len(encode) - len(defaultEncSuffix):
            return encode
        encode = encode.replace(defaultEncPrefix, "", 1)
        encode = encode.replace(defaultEncSuffix, "", 1)
        value = decrypt(encode, password=password)
        return value
    except Exception as e:
        log.error("decrypt error: {}, value: [ {} ], return the original value".format(e, encode))
        log.exception(e)
        return encode


def process_zp_decrypt(value):
    """
    解密处理函数
    """
    if isinstance(value, str) and "ZPENC(" in value:
        if not init_zp_decrypt_password():
            log.error("InitCryptPassword fail, ignore decrypt value: {}".format(value))
            return value

        log.debug("detect zp decrypt value")
        new_value_str = re.sub(r"ZPENC\(.*?\)ZPENC", lambda x: translate(x.group()), value)
        return new_value_str
    else:
        return value
