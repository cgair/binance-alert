# <https://blog.csdn.net/weixin_39984952/article/details/112215453>
# [Flask](https://dormousehole.readthedocs.io/en/latest/quickstart.html#id1)
# [python-binance](https://python-binance.readthedocs.io/en/latest/overview.html)

from flask import Flask, request
import json
import toml

CONFIG_PATH="./config/config.toml"
CONFIG=None

app = Flask(__name__)

##################################################################
# Call xiaomi to modify the configuration (i.e., position prices)#
##################################################################
@app.route("/call", methods=['POST'])
def call():
    global CONFIG
    if request.method == 'POST':
        content = request.get_json().get('text').get('content')
        conf_dict = json.loads(content)
        app.logger.debug(conf_dict)

        for symbol in conf_dict.keys():
            if symbol in CONFIG['category']['symbols']:
                for symboli in CONFIG['specify'].keys():
                    if symbol == CONFIG['specify'][symboli]["symbol"]:
                        CONFIG['specify'][symboli]['support_position'] = conf_dict[symbol]["支撑位"]
                        CONFIG['specify'][symboli]['resistance_point'] = conf_dict[symbol]["阻力位"]
            else:
                CONFIG['category']['symbols'].append(symbol)
                sum_symbol = len(CONFIG['specify'])
                new_symbol = "symbol{}".format(str(sum_symbol + 1))
                CONFIG['specify'][new_symbol] = {'symbol': new_symbol, 'support_position': conf_dict[symbol]["支撑位"], 'resistance_point': conf_dict[symbol]["阻力位"]}
        try:
            with open(CONFIG_PATH, 'w') as f:
                print(CONFIG)
                r = toml.dump(CONFIG, f)
                app.logger.error(r)
        except:
            msg = {
                "msgtype": "text",
                "text": {
                    "content": "配置文件更新发送错误: {}".format(r)
                    },             
                "at": {
                    "atMobiles": [],
                    "isAtAll": False
                    }         
                }        
        msg = {
            "msgtype": "text",
            "text": {
                "content": "配置文件已经更新成功"            
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
                "content": "不支持 GET"             
                },             
            "at": {
                "atMobiles": [],
                "isAtAll": False
                }         
            }        


if __name__ == '__main__':
    CONFIG = toml.load(CONFIG_PATH)
    app.run(host='0.0.0.0', port=8888, debug=True)