#!/usr/bin/env python
import logging
import threading

from binance.lib.utils import config_logging

from making_money import *
from dingding_client import send_msg
from utils import *
# from config import Config
import config

# SYMBOLS=["BTCUSDT", "ETHUSDT", "DOGEUSDT"]
QUOTATION_FMT="-------------------------\n[{}]\n{}: ${} U\n时间: {}\n过去1天的涨跌幅: {:.2%}\n"
CROSSING_FMT="{} 即将穿过(Crossing) {}."
VOLUME_FMT="{} {}分钟成交量超过{} 当前成交量为: {}, 这根K线期间末一笔成交价为: {}."

def job(conf):
    logging.debug("Starting job...")
    config = conf.config['specify']
    handler = []
    for value in config.values():
        symbol = value['symbol'] if 'symbol' in value.keys() else 'ETHUSDT'
        t = threading.Thread(target=start_websocket, args=(conf, symbol))
        t.start()
        handler.append(t)
    for h in handler:
        h.join()


def main():
    conf = config.Config()
    job(conf)

if __name__ == '__main__':
    config_logging(logging, logging.DEBUG)
    # config_logging(logging, logging.INFO)
    main()