"""
@author chenge
"""
# Specify the currency and specify the alarm price to trigger (multiple currencies and prices can be set at the same time) 
# The example of the message body is as follows:
# "ETHUSDT Crossing 1111.74"
import logging
import demjson
import websocket

from dingding_client import send_msg, send_msg_at
from start import CROSSING_FMT, VOLUME_FMT

KLINE = 'wss://fstream.binance.com/ws/{}@kline_1m' # TODO interval should be configurable
CONF = None
SYMBOLS = []
reconnect_count = 0

#################################################
# Subscribe to k-line information in real time. #
#################################################
def start_websocket(
    conf,
    symbol
    ):
    global KLINE_URL
    kline_url = KLINE.format(symbol.lower())
    _set_global(conf, symbol)
    start(kline_url)


def on_message(ws, message):
    """
    on_message: function
        Callback object which is called when received data.
        on_message has 2 arguments.
        The 1st argument is this class object.
        The 2nd argument is utf-8 data received from the server.
    """
    message = demjson.decode(message)
    logging.debug(f"RCVD: {message}")
    global CONF
    global SYMBOLS
    config = CONF.config['specify']
    for value in config.values():
        sb = value['symbol'] if 'symbol' in value.keys() else 'ETHUSDT'
        if sb in SYMBOLS:
            support_position = value['support_position'] if 'support_position' in value.keys() else None
            resistance_point = value['resistance_point'] if 'resistance_point' in value.keys() else None
            volume = value['volume'] if 'volume' in value.keys() else None
            logging.debug(f"CONFIG: symbol = {sb}, support_position = {support_position}, resistance_point = {resistance_point}, volume = {volume}")        

            if resistance_point:
                _is_crossing(message, resistance_point)
            if support_position:
                _is_crossing(message, support_position)
            if volume:
                _is_surpassing(message, volume)


def on_close(ws, close_status_code, close_msg):
    """
    on_close: function
        Callback object which is called when connection is closed.
        on_close has 3 arguments.
        The 1st argument is this class object.
        The 2nd argument is close_status_code.
        The 3rd argument is close_msg.
    """
    logging.debug(f"CLOSED: {close_status_code} - {close_msg}")
    global KLINE_URL
    start(KLINE_URL)


def on_error(ws, error):
    """
    on_error: function
        Callback object which is called when we get error.
        on_error has 2 arguments.
        The 1st argument is this class object.
        The 2nd argument is exception object.
    """
    global reconnect_count, KLINE_URL
    if type(error)==ConnectionRefusedError or type(error)==websocket._exceptions.WebSocketConnectionClosedException:
        logging.info(f"Attempting to reconnect {reconnect_count}")
        reconnect_count += 1
        if reconnect_count < 100:
            start(KLINE_URL)
    else:
        logging.error("encounter other error!")


def start(url):
    ws = websocket.WebSocketApp(
            url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close)

    try:
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()  
    except:
        ws.close() 

    # work around https://github.com/websocket-client/websocket-client/issues/777
    # ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly


def _set_global(conf, symbol):
    global CONF, SYMBOLS
    CONF = conf
    SYMBOLS.append(symbol)


def _is_surpassing(message, volume):
    symbol = message['s']
    tx_num = message['k']['v'] # Transaction numbers during this K line
    last_tx_price = message['k']['c']# The last transaction price of this K-line period
    if float(tx_num) >= float(volume):
        content = VOLUME_FMT.format(symbol, 1, volume, tx_num, last_tx_price)
        send_msg_at(content)

def _is_crossing(message, critical_price):
    symbol = message['s']
    tx_price_h = message['k']['h']    # The highest transaction price during this K line
    tx_price_l = message['k']['l']    # The lowest transaction price during this K line
    if float(tx_price_h) > float(critical_price) and float(tx_price_l) < float(critical_price):
        content = CROSSING_FMT.format(symbol, critical_price)
        logging.debug(f"alerting message: {content}")
        send_msg(content)