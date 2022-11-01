import time
import hmac
import hashlib
import base64
import urllib.parse
# use dingding API
import dingtalk.api

SECRET="SEC4871dbff8d46589bbb3c000cdae2a5ae8f416a278efb4fd596785b1cec8c8445"
WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=0f60b54f89d54904cda0a2c46d3013d28d04d7de09025f8afd42c9664adcdb0e&timestamp={}&sign={}"


def send_msg(content_txt):
    timestamp = str(round(time.time() * 1000))
    secret_enc = SECRET.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, SECRET)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    webhook = WEBHOOK.format(timestamp,sign)
    request = dingtalk.api.OapiRobotSendRequest(webhook)
    request.msgtype = 'text'
    request.text = {
        "content": content_txt
    }
    # atMobiles:钉钉群中所对应的成员手机号
    # isAtAll：当设置为True时，发送消息时@所有人
    # request.at = {
    #         "atMobiles":["13*****4538"],
    #         "isAtAll": True
    #     }

    response = request.getResponse()
    return response


def send_msg_at(content_txt):
    timestamp = str(round(time.time() * 1000))
    secret_enc = SECRET.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, SECRET)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    webhook = WEBHOOK.format(timestamp,sign)
    request = dingtalk.api.OapiRobotSendRequest(webhook)
    request.msgtype = 'text'
    request.text = {
        "content": content_txt
    }
    # atMobiles:钉钉群中所对应的成员手机号
    # isAtAll：当设置为True时，发送消息时@所有人
    request.at = {
            "atMobiles":["15383469010"],
            "isAtAll": False
        }

    response = request.getResponse()
    return response

# if __name__ == '__main__':
#     send_msg()