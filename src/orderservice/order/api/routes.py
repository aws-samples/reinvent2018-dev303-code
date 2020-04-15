#
# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import requests

from flask import Blueprint, current_app, jsonify, request

api = Blueprint('api', 'api', url_prefix='/api/v1', static_url_path=None)

@api.route('/order', methods=['POST'])
def post():
    """Create order"""
    args = request.get_json(force=True)

    if len(args) < 10:
        return jsonify({"order_id": "", "code": 500, "status": "Incomplete arguments provided"}), 500

    if 'address2' in args:
        address2 = args["address2"]
    else:
        address2 = ''

    order_details = {
        "name": args["name"],
        "email": args["email"],
        "address": args["address"],
        "address2": address2,  # optional
        "country": args["country"],
        "state": args["state"],
        "zip": args["zip"],
        "city": args["city"],
        "paymentMethod": args["paymentMethod"],
        "cart_id": args['cart_id'],
        "user_id": args['user_id']
    }

    # Get Cart for products
    url = 'http://' + \
        current_app.config['CART_ENDPOINT'] + \
        '/api/v1/cart/' + args['cart_id']

    r = requests.get(url, timeout=1)
    if r.status_code != 200:
        return jsonify({"order_id": "", "code": 500, "status": "Failed to get cart"}), 500

    cart_details = r.json()

    product_detail_list = []
    if len(cart_details['items']) < 1:
        return jsonify({"order_id": "", "code": 500, "status": "Cart is empty"}), 500

    s = requests.Session()
    for p in cart_details['items']:
        # Get Cart for products
        url = 'http://' + \
            current_app.config['CATALOG_ENDPOINT'] + '/api/v1/product/' + p
        r = s.get(url, timeout=1)
        if r.status_code != 200:
            # Cart contained invalid products.
            return jsonify({"order_id": "", "code": 500, "status": "Failed to fetch products"}), 500

        product_info = r.json()
        product_detail_list.append(product_info)
    s.close()

    order = {
        "shipping": order_details,
        "cart": cart_details,
        "products": product_detail_list,
    }

    return jsonify({"order_id": "1234567890", "code": 200, "status": "Order created", "data": json.dumps(order)}), 200

@api.route('/healthz')
def health():
    """Health check"""
    return 'OK'
