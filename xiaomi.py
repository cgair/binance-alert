# <https://blog.csdn.net/weixin_39984952/article/details/112215453>
# [Flask](https://dormousehole.readthedocs.io/en/latest/quickstart.html#id1)
# [python-binance](https://python-binance.readthedocs.io/en/latest/overview.html)

from flask import Flask, request
from binance.client import Client

API_KEYS = {"lys": "EiBHoUOBSY2Ou9UekpxlhVslkxbSpsC71Z7HsGyJamDEitRkOn2HSc0QTcQsqNzo", "cg": ""}
API_SECRET = {"lys": "98jHttnRipKiH31X2KjnXe0eUmXLJOOzPOPDOByZsUZ4w2cln5qkvPAYSZ4JBQ2H", "cg": ""}

app = Flask(__name__)

@app.route("/call", methods=['POST'])
def call():
    if request.method == 'POST':
        content = request.get_json().get('text').get('content')
        app.logger.debug(content)
        msg = {
            "msgtype": "text",
            "text": {
                "content": "你说的是:  {0}".format(content)             
                },             
            "at": {
                "atMobiles": [],
                "isAtAll": False
                }         
            }        
        return msg
    else:
        return {
            "msgtype": "text",
            "text": {
                "content": "GET"             
                },             
            "at": {
                "atMobiles": [],
                "isAtAll": False
                }         
            }        

##################################################################
# Convert a Python double/float into an ES6/V8 compatible string #
##################################################################
class Account:
    """
    
    """
    def __init__(
        self,
        client
        ):
        self.client = client

    """https://python-binance.readthedocs.io/en/latest/account.html#id8
    """
    def account_info(self):
        info = client.get_account()
        print(info)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8888, debug=True)
    client = Client(API_KEYS["lys"], API_SECRET["lys"])

    res = client.get_account()
    print(client.response)
