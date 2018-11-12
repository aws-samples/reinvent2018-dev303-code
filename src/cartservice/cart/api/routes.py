#
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import redis
import requests

from flask import Blueprint, current_app, jsonify, request

api = Blueprint('api', 'api', url_prefix='/api/v1')

@api.route('/cart/<string:cart_id>',methods=['GET'])
def get(cart_id):
    """Get Cart"""

    list = []
    cart = {"items": list, "size": 0}

    redis_cart = current_app.config['redis'].smembers(cart_id)

    if redis_cart:
        [list.append(x.decode()) for x in redis_cart]

        cart['size'] = len(list)

    return jsonify(cart), 200

@api.route('/cart',methods=['POST'])
def post():
    """Add item to cart"""
    redis = current_app.config['redis']

    args = request.get_json(force=True)

    product = args['product_id']
    user = args['cart_id']

    # Validate if product exists
    # Get Cart for products
    url = 'http://' + current_app.config['CATALOG_ENDPOINT'] + '/api/v1/product/' + product
    r = requests.get(url, timeout=1)
    if r.status_code != 200:
        return jsonify({"code": 404, "status": "Product does not exist"}), 404

    if redis.sismember(user, product):
        return jsonify({"message": "Product already in cart", "status": 200}), 200
    else:
        redis.sadd(user, product)

    return jsonify({"message": "Product added to Cart", "status": 200}), 200

@api.route("/cart/<string:cart_id>",methods=['DELETE'])
def delete(cart_id):
    """Empty cart"""

    if cart_id:
        current_app.config['redis'].delete(cart_id)

        return jsonify({"message": "Cart deleted", "status": 200}), 200
    else:
        return jsonify({"message": "Error", "status": 500}), 500

@api.route("/healthz")
def health():
    return 'OK'
