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

from flask import Blueprint, Response, current_app, jsonify, json

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert a DynamoDB item to JSON."""

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


api = Blueprint('api', 'api', url_prefix='/api/v1')


@api.route('/product/<string:product_id>')
def get_product(product_id):
    try:
        res = current_app.config['db'].get_item(
            Key={
                'id': product_id
            }
        )
    except ClientError as e:
        return jsonify({"code": 500, "status": e.response['Error']['Message']}), 500
    else:
        if "Item" in res:
            # , 200, 'application/json'
            return json.dumps(res["Item"], cls=DecimalEncoder)
        else:
            return jsonify({"code": 404, "status": "Failed to fetch product"}), 404


@api.route('/products')
def get_products():
    """Single object resource"""
    data = {}

    try:
        res = current_app.config['db'].scan()

        if res['ResponseMetadata']['HTTPStatusCode'] != 200:
            return jsonify({"code": 500, "status": res['ResponseMetadata']}), 500

        if "Items" in res:
            data = res['Items']

        while 'LastEvaluatedKey' in res:
            res = g.db.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])

            if "Items" in res:
                data.extend(res['Items'])

        return json.dumps(data, cls=DecimalEncoder)  # , 200 'application/json'

    except ClientError as e:
        return jsonify({"code": 500, "status": e.message}), 500


@api.route("/healthz")
def health():
    return 'OK'
