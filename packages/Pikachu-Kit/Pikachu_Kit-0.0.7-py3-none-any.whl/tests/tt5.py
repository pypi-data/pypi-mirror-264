# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: tt5.py
@time: 2023/12/20 17:02 
@desc: 

"""
from gradio import networking
import secrets
from flask import Flask
import traceback

def toshared(host,port):
    """

    :param host:
    :param port:
    :return:
    """
    try:
        share_token = secrets.token_urlsafe(32)
        print(f"share_token: {share_token}")
        share_url = networking.setup_tunnel(local_host=host, local_port=port, share_token=share_token)
        print(f"share_url:{share_url}")
    except :
        print(traceback.format_exc())


app = Flask(__name__)
@app.route("/")
def index():
    return "gradio server"


if __name__ == '__main__':
    host = "0.0.0.0"
    port = 8080

    toshared(host,port)
    app.run(host,port,debug=True)