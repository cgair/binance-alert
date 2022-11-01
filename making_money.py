"""
@author chenge
"""
# Specify the currency and specify the alarm price to trigger (multiple currencies and prices can be set at the same time) 
# The example of the message body is as follows:
# "ETHUSDT Crossing 1111.74"
import logging
import demjson
import websocket
import time

from dingding_client import send_msg, send_msg_at
from start import CROSSING_FMT, VOLUME_FMT

KLINE = 'wss://fstream.binance.com/ws/{}@kline_1m' # TODO interval should be configurable


class UMWebsocketClient(object):
    def __init__(
        self, 
        conf,
        symbol, # a flag used to distinguish which conf should be hot-fixed
        url,
        ):
        self.ws = None
        self.conf = conf
        self.symbol = symbol
        self.url = url

    def on_message(self, obj, message):
        config = self.conf.config['specify']
        for value in config.values():
            symbol = value['symbol'] if 'symbol' in value.keys() else 'ETHUSDT'
            if symbol == self.symbol:
                support_position = value['support_position'] if 'support_position' in value.keys() else None
                resistance_point = value['resistance_point'] if 'resistance_point' in value.keys() else None
                volume = value['volume'] if 'volume' in value.keys() else None
                logging.debug(f"CONFIG: symbol = {symbol}, support_position = {support_position}, resistance_point = {resistance_point}, volume = {volume}")

        message = demjson.decode(message)
        logging.debug(f"received: {message}")
        if resistance_point:
            self._is_crossing(message, resistance_point)
        if support_position:
            self._is_crossing(message, support_position)
        if volume:
            self._is_surpassing(message, volume)
        time.sleep(60)

    def on_close(self, close_status_code, close_msg):
        logging.debug(f'closed: {close_status_code}, {close_msg}')
    
    def on_error(self, error):
        global reconnect_count
        if type(error)==ConnectionRefusedError or type(error)==websocket._exceptions.WebSocketConnectionClosedException:
            logging.info(f"Attempting to reconnect {reconnect_count}")
            reconnect_count += 1
            if reconnect_count < 100:
                self.start()
        else:
            logging.error("encounter other error!")
    
    def start(self):
        # if kind == 'kline':
        # Enable running status tracking. 
        # It is best to open it when debugging, so as to track and locate the problem.
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_close=self.on_close)
        try:
            self.ws.run_forever()
        except KeyboardInterrupt:
            self.ws.close()  
        except:
            self.ws.close() 

    def _is_surpassing(self, message, volume):
        symbol = message['s']
        tx_num = message['k']['v'] # Transaction numbers during this K line
        last_tx_price = message['k']['c']# The last transaction price of this K-line period
        if float(tx_num) >= float(volume):
            content = VOLUME_FMT.format(symbol, 1, volume, tx_num, last_tx_price)
            send_msg_at(content)

    def _is_crossing(self, message, critical_price):
        symbol = message['s']
        tx_price_h = message['k']['h']    # The highest transaction price during this K line
        tx_price_l = message['k']['l']    # The lowest transaction price during this K line
        if float(tx_price_h) > float(critical_price) and float(tx_price_l) < float(critical_price):
            content = CROSSING_FMT.format(symbol, critical_price)
            logging.debug(f"alerting message: {content}")
            send_msg(content)


def start_websocket(
    conf,
    symbol
    ):
    kline_url = KLINE.format(symbol.lower())
    umc = UMWebsocketClient(
        conf,
        symbol,
        kline_url
        )
    umc.start()


