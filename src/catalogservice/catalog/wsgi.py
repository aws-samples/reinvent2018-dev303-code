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
import os

import boto3
import click

from faker import Factory
from faker.providers import barcode, lorem

from catalog.app import create_app

app = create_app()

def create_table(dynamodb):
    """Create DynamoDB table"""

    print("Creating table...")
    table = dynamodb.create_table(
        TableName='ProductCatalog',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 35,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()
    print("Table status:", table.table_status)

    return table


@app.cli.command()
def import_data():
    """create app resources: DynamoDB table with data"""

    fake = Factory.create()
    fake.add_provider(lorem)

    # Instantiate your dynamo client object
    client = boto3.client('dynamodb', region_name=app.config['AWS_REGION'])

    # Get an array of table names associated with the current account and endpoint.
    response = client.list_tables()

    dynamodb = boto3.resource(
        'dynamodb', region_name=app.config['AWS_REGION'])

    if 'ProductCatalog' not in response['TableNames']:
        create_table(dynamodb)

    table = dynamodb.Table('ProductCatalog')

    try:
        res = table.get_item(
            Key={
                'id': '3377807835348'
            }
        )
    except ClientError as e:
        return False
    else:
        if "Item" in res:
            # Data has been loaded
            return True

    with open("productcatalog.json") as json_file:
        products = json.load(json_file, parse_float=decimal.Decimal)

        print("Products loaded from json file")

        for product in products:
            item = {
                'id': product['id'],
                'name': product['name'],
                'description': fake.text(),
                'manufacturer': product['manufacturer'],
                'category': product['category'],
                'picture': product['picture'],
                'offer': product['offer']
            }

            table.put_item(Item=item)
