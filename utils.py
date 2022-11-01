import logging
from datetime import datetime
from dingding_client import send_msg

IP_LIMIT_FMT="limit usage: {}, IP access has been restricted!"


def to_beijingtime(timestamp):
    """
    convert 13 unix timestamp to Beijing time
    :return:
    """
    return datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')


def access_limit(limit_usage):
    logging.debug(f"limit usage = {limit_usage}")
    if int(limit_usage) > 428:
        warning = IP_LIMIT_FMT.format(limit_usage)
        send_msg(warning)