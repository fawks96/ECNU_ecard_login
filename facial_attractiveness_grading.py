# -*- coding:utf-8 -*-

import json
import re
import requests
import time
import os, shutil

if __name__ == '__main__':
    myheader = {
        'Host': 'kan.msxiaobing.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Origin': 'http://kan.msxiaobing.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://kan.msxiaobing.com/V3/Portal',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    }

    url1 = 'http://kan.msxiaobing.com/Api/Image/UploadBase64'
    url2 = 'http://kan.msxiaobing.com/Api/ImageAnalyze/Process?service=yanzhi&tid=52a90c91aaeb4af698bec8ae2106cb36'

    pattern = re.compile(r'\d+\.\d+')
    s = requests.Session()

    photo_path = '/Users/fawks96/PycharmProjects/login/88'
    for path, subdirs, files in os.walk(photo_path):
        print path, subdirs, files
        if path.find('man') != -1 or path.find('error') != -1 or path.find('beautiful') != -1: continue
        for img in files:

            with open(path + '/' + img, 'rb') as f:
                image_data = f.read()
                image_data = image_data.encode("base64")

            try:
                r = s.post(url1, data=image_data, headers=myheader)
                res = json.loads(r.text)
                data = {
                    'msgId': int(round(time.time() * 1000)),
                    'timestamp': int(time.time()),
                    'senderId': 'mtuId' + str(int(round(time.time() * 1000))),  # ot = "mtuId" + Date.now();
                    'content[imageUrl]': res['Host'] + res['Url']  # 上传文件放回来的
                }

                r = s.post(url2, data=data, headers=myheader)
                res = json.loads(r.text)
                match = pattern.search(res['content']['text'])
                score = float(match.group())
                print path + '/' + img, score
                if 1==1:
                    beautiful_path = path + '/beautiful'
                    if not os.path.exists(beautiful_path):
                        os.mkdir(beautiful_path)
                    shutil.move(path + '/' + img, beautiful_path + '/' + img)

            except Exception, e:
                error_path = path + '/ice_error'
                if not os.path.exists(error_path):
                    os.mkdir(error_path)
                shutil.move(path + '/' + img, error_path + '/' + img)