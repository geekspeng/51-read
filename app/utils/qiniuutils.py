# -*- coding: utf-8 -*-
# @Time    : 2018/9/16 23:55
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
import requests
from flask import app
from qiniu import Auth, put_file


#  Access Key 和 Secret Key
access_key = app.config['QINIU_ACCESS_KEY']
secret_key = app.config['QINIU_SECRET_KEY']

# 构建鉴权对象
q = Auth(access_key, secret_key)

# 要上传的空间
bucket_name = app.config['QINIU_BUCKET_NAME']
bucket_domain = app.config['QINIU_DOMAIN']


def qiniu_upload_file(source_file, save_file_name):
    token = q.upload_token(bucket_name, save_file_name)
    ret, info = put_file(token, save_file_name, source_file.stream)
    if info.status_code == 200:
        return bucket_domain + save_file_name
    else:
        return None


def qiniu_download_file(file_name):
    base_url = 'http://%s/%s' % (bucket_domain, file_name)
    private_url = q.private_download_url(base_url)
    r = requests.get(private_url)
    if r.status_code == 200:
        return True
    else:
        return False
