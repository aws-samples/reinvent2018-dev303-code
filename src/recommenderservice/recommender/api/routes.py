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
import requests
import random

from aws_xray_sdk.core import xray_recorder

from flask import Blueprint, current_app, jsonify

# Static product list
ean_list = [
    "0983976883313",
    "1051094507639",
    "3103748076140",
    "3377807835348",
    "3480077496703",
    "4618701513994",
    "5147991444866",
    "6392888360364",
    "6464865908071",
]

# Build list of recommendations
recommendations = {
    "0983976883313": random.sample(ean_list, 3),
    "1051094507639": random.sample(ean_list, 3),
    "3103748076140": random.sample(ean_list, 3),
    "3377807835348": random.sample(ean_list, 3),
    "3480077496703": random.sample(ean_list, 3),
    "4618701513994": random.sample(ean_list, 3),
    "5147991444866": random.sample(ean_list, 3),
    "6392888360364": random.sample(ean_list, 3),
    "6464865908071": random.sample(ean_list, 3),
}

api = Blueprint('api', 'api', url_prefix='/api/v1')

@api.route('/recommender/<string:product_id>')
def get(product_id):
    '''Get recommendations'''

    if product_id is None:
        return jsonify({"recommendations": {}, "status": 404}), 404

    if product_id not in recommendations:
        return jsonify({"recommendations": {}, "status": 404}), 404

    products = []

    s = requests.Session()
    for rec in recommendations[product_id]:
        # Get Cart for products
        url = 'http://' + \
            current_app.config['CATALOG_ENDPOINT'] + \
            '/api/v1/product/' + rec
        r = s.get(url, timeout=1)
        if r.status_code == 200:
            products.append(r.json())
    s.close()

    if len(products) > 0:
        return jsonify({"recommendations": products, "status": 200}), 200
    else:
        return jsonify({"recommendations": {}, "status": 404}), 404

@api.route("/healthz")
def health():
    """Health check"""
    return 'OK'
