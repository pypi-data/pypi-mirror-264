#!/usr/bin/env python
import logging
from quantfreedom.exchanges.binance_exchange.binance_github.usdm_futures.um_futures import UMFutures
from quantfreedom.exchanges.binance_exchange.binance_github.usdm_futures.lib_usdm.utils import config_logging
from quantfreedom.exchanges.binance_exchange.binance_github.usdm_futures.error import ClientError

config_logging(logging, logging.DEBUG)

# HMAC authentication with API key and secret
key = ""
secret = ""

hmac_client = UMFutures(key=key, secret=secret)
logging.info(hmac_client.account(recvWindow=6000))

# RSA authentication with RSA key
key = ""
with open("/Users/john/private_key.pem", "r") as f:
    private_key = f.read()

rsa_client = UMFutures(key=key, private_key=private_key)

try:
    response = rsa_client.account(recvWindow=6000)
    logging.info(response)
except ClientError as error:
    logging.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )
