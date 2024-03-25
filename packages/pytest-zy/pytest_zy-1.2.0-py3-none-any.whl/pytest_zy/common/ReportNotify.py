import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
from .log import log


def dingding_notify(msg, webhook, secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(
        secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f"{webhook}&timestamp={timestamp}&sign={sign}"
    data = {"msgtype": "text", "text": {"content": "通知:" + msg}}
    res = requests.post(url, json=data)
    log.info(f"钉钉报告发送成功！响应：{res}")
