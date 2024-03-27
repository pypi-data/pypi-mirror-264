#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -------------------
# @Time    : 2024/3/21 16:55
# @Version : 1.0
# @Author  : lvzhidong
# @For : 
# -------------------
import base64
import hashlib
import os

from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad


def get_md5_derived_key(password, salt, count):
    # key = hashlib.md5((password + salt.decode()).encode()).digest()
    key = hashlib.md5(password.encode() + salt).digest()
    for _ in range(count - 1):
        key = hashlib.md5(key).digest()
    return key[:8], key[8:]


def des_encrypt(orig_data, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_data = pad(orig_data, DES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return encrypted


def des_decrypt(encrypted, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    return unpad(decrypted, DES.block_size)


def aes_encrypt(orig_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(orig_data, AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return encrypted


def aes_decrypt(encrypted, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)
    return unpad(decrypted, AES.block_size)


def generate_salt(length_bytes):
    salt = os.urandom(length_bytes)
    return salt


def generate_iv(length_bytes):
    iv = os.urandom(length_bytes)
    return iv


def aes_base64_encrypt(in_str, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(in_str.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    encoded_data = base64.b64encode(encrypted_data).decode()
    return encoded_data


def aes_base64_decrypt(b, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = base64.b64decode(b)
    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode()
