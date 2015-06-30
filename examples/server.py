#!/usr/bin/env python
# let's include the project directory to have access to the lib
# import sys
# sys.path.append('..')

import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse


import currencycloud

currencycloud.environment = currencycloud.ENV_DEMOSTRATION
currencycloud.login_id = 'rjnienaber@gmail.com'
currencycloud.api_key = 'ef0fd50fca1fb14c1fab3a8436b9ecb65f02f129fd87eafa45ded8ae257528f0'


class CurrencyCloudHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text-html')
        self.end_headers()

        self.wfile.write(self.__route())

    def __route(self):
        parsed_url = urlparse.urlparse(self.path)
        route = parsed_url.path.strip('/')
        route.replace('/', '_')

        params = urlparse.parse_qs(parsed_url.query)
        if hasattr(self, route):
            return getattr(self, route)(**params)

    def conversion(self, **params):
        try:
            conversion = currencycloud.Conversion.create(**params)
            return "Conversion Result: {data}".format(data=conversion.data)
        except Exception as e:
            return str(e)


def run():
    ADDRESS = os.environ.get('CC_ADDRESS', '127.0.0.1')
    PORT = int(os.environ.get('CC_PORT', 8080))

    print(
        'HTTP server is started at http://{address}:{port}'.format(address=ADDRESS, port=PORT))
    print(
        "Try: http://localhost:8080/conversion?buy_currency=GBP&sell_currency=USD&fixed_side=buy&amount=1000&reason=mortage&term_agreement=true")

    server_address = (ADDRESS, PORT)
    httpd = HTTPServer(server_address, CurrencyCloudHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
