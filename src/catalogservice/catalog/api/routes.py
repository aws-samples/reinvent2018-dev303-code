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

import decimal
import json

from catalog.api.catalog import productdata

from flask import Blueprint, Response, current_app, jsonify, json

api = Blueprint('api', 'api', url_prefix='/api/v1')

@api.route('/product/<string:product_id>')
def get_product(product_id):
    try:
        p = productdata[product_id]
    except:
        return jsonify({"code": 500, "status": "Error getting product"}), 500
    else:
        # , 200, 'application/json'
        return json.dumps(p)

@api.route('/products')
def get_products():
    """Single object resource"""
    p = {}

    return json.dumps(productdata) #, 200 'application/json'


@api.route("/healthz")
def health():
    return 'OK'
