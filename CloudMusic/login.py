#!/usr/bin/env python
# coding:utf-8
import os
import json
import requests
from Crypto.Cipher import AES
from cookielib import LWPCookieJar
import base64


modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7')
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'

# 站在巨人的肩膀上: https://github.com/stkevintan/Cube
# https://github.com/darknessomi/musicbox
def encrypted_request(text):
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {'params': encText, 'encSecKey': encSecKey}
    return data


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = pow(int(text.encode('hex'), 16), int(pubKey, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return (
        ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/search/',
    "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
        )
}

cookies = {'appver': '1.5.2'}
session = requests.Session()
session.cookies = LWPCookieJar('cookies')
session.cookies.load()
session.cookies.save()


def phone_login(username, password):
    action = 'https://music.163.com/weapi/login/cellphone'
    text = {
        'phone': username,
        'password': password,
        'rememberLogin': 'true'
    }
    data = encrypted_request(text)
    connect = session.post(action, data=data, headers=header, timeout=10)
    connect.encoding = 'UTF-8'
    return connect.content
