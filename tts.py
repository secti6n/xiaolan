# -*- coding: utf-8 -*-
# 百度TTS
import sys
import os
import logging
import requests
import wave
import json
import pyaudio
import time
import shutil
import urllib2
import urllib
import base64
import md5
import random
import tempfile
from urllib import quote
import setting


class baidu_tts(object):
    def __init__(self):
        
        pass
        
    def get_token(self):
        
        selfset = setting.setting()
        AK = selfset['main_setting']['BAIDU_TTS_SET']['AK']
        SK = selfset['main_setting']['BAIDU_TTS_SET']['SK']
        URL = 'http://openapi.baidu.com/oauth/2.0/token'
        
        params = urllib.urlencode({'grant_type': 'client_credentials',
                                   'client_id': AK,
                                   'client_secret': SK})
        r = requests.get(URL, params=params)
        try:
            r.raise_for_status()
            token = r.json()['access_token']
            return token
        except requests.exceptions.HTTPError:
            self._logger.critical('Token request failed with response: %r',
                                  r.text,
                                  exc_info=True)
          
        
    def tts(self, saytext, token):
        bt = baidu_tts()
        data = {'tex': saytext,
                 'lan': 'zh',
                 'tok': token,
                 'ctp': 1,
                 'cuid': 'b0-10-41-92-84-4d',
                 'per': 4
                 }
        r = requests.post('http://tsn.baidu.com/text2audio',
                          data=data,
                          headers={'content-type': 'application/json'},stream=True)

        if r.status_code == 200:  
            with open(r"/home/pi/xiaolan/musiclib/say.mp3", 'wb') as f:  
                r.raw.decode_content = True  
                shutil.copyfileobj(r.raw, f)
        else:
            bt.tts('对不起，我的语言中枢出错了，我不能跟你说话了', tok)
            speaker.speak()

class youdao_tts(object):
    
    def __init__(self):
        
        pass
    
    def tts(self, saytext, lang):
        
        y = youdao_tts()
        selfset = setting.setting()
        appSecret = selfset['main_setting']['YOUDAO_TTS_SET']['appkey']
        appKey = selfset['main_setting']['YOUDAO_TTS_SET']['appid']
        data = {}
        salt = random.randint(1, 65536)

        sign = appKey + q + str(salt) + appSecret
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()

        data['appKey'] = appKey
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        data['langType'] = lang
        response = requests.post('http://openapi.youdao.com/ttsapi',
                                 data=data)

        contentType = response.headers['content-type']
        
        if contentType == "audio/mp3":
            filePath = "/home/pi/xiaolan/musiclib/" + 'say' + ".mp3"
            fo = open(filePath,'wb')
            fo.write(response.content)
            fo.close()
        else:
            y.tts('对不起，我的语言中枢出错了，我不能跟你说话了', 'zh-CHS')
            speaker.speak()
