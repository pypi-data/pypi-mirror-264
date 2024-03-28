from datetime import datetime
import hashlib
import hmac
import json
import requests

def gen_signature(data, credentials: dict):
    body = json.dumps(data, separators=(',', ':'))
    req_body = hashlib.sha256(body.encode()).hexdigest().lower()
    secret = credentials["api_key"]
    va = credentials["va"]
    string_to_sign = ("POST:" + va + ":" + req_body + ":" + secret).encode()

    return hmac.new(bytes(secret, "utf-8"), string_to_sign, hashlib.sha256).hexdigest()


def request(config, data, credentials: dict):
    signature = gen_signature(data, credentials)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    headers = {
        "Content-Type": "application/json",
        "va": credentials["va"],
        "signature": signature,
        "timestamp": timestamp,
    }

    return requests.post(config, headers=headers, data=json.dumps(data), verify=False)
