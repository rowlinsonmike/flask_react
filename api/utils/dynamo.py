import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeDeserializer
deserializer = TypeDeserializer()
from os import environ

# https://www.trek10.com/blog/dynamodb-single-table-relational-modeling/


def deserialize(values):
    d = lambda x: {k: deserializer.deserialize(v) for k, v in x.items()}
    return [d(v) for v in values]

TABLE_TEMPLATE = {
    'KeySchema':[
            {
                'AttributeName': 'pk',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'sk',
                'KeyType': 'RANGE'
            },
    ],
    'AttributeDefinitions':[
            {
                'AttributeName': 'pk',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'sk',
                'AttributeType': 'S'
            },
            {
            'AttributeName': 'data',
            'AttributeType': 'S'
            }
    ],
    'GlobalSecondaryIndexes':[
        {
            'IndexName': 'gsi_1',
            'KeySchema': [
                    {
                        'AttributeName': 'sk',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'data',
                        'KeyType': 'RANGE'
                    },
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            }
        },
    ],
    'BillingMode':'PAY_PER_REQUEST'
}

class DynamoTable(object):
    def __init__(self,app):
        self.client = boto3.client('dynamodb',region_name=app.config.get("AWS_REGION"))
        self._table = app.config.get("DYNAMO_USER_TABLE")
        self.resource = boto3.resource('dynamodb',region_name=app.config.get("AWS_REGION")).Table(self._table)
        ...
    def create_table(self):
        self.client.create_table(TableName=self._table,**TABLE_TEMPLATE)
    def delete_table(self):
        self.client.delete_table(TableName=self._table)
    def load(self,key,**kwargs):
        elements = key.split(":")
        if len(elements) < 3:
            pk,sk = key.split(":")
            resp = self.resource.put_item(
                Item={
                    'pk':pk,
                    'sk': sk,
                    **kwargs
                }
            )
        else:
            pk,sk,data = elements
            resp = self.resource.put_item(
                Item={
                    'pk':pk,
                    'sk': sk,
                    'data':data,
                    **kwargs
                }
            )
    def delete(self,key):
        try:
            pk,sk = key.split(":")
            resp = self.resource.delete_item(Key={'pk': pk, 'sk': sk})
        except Exception as e: 
            print(e)
    def query(self,key):
        #gsi_1 index
        if key[0] == ":":
            elements = key.split(":")
            if len(elements) == 2:
                #no data key
                resp = self.resource.query(IndexName='gsi_1',KeyConditionExpression=Key('sk').eq(elements[1]))
            else:
                resp = self.resource.query(IndexName='gsi_1',KeyConditionExpression=Key('sk').eq(elements[1]) & Key('data').eq(elements[2]))
        #primary index
        else:
            elements = key.split(":")
            if len(elements) == 1:
                #no data key
                resp = self.resource.query(KeyConditionExpression=Key('pk').eq(elements[0]))
            else:
                resp = self.resource.query(KeyConditionExpression=Key('pk').eq(elements[0]) & Key('sk').eq(elements[1]))
        return resp['Items']

class Dynamo(object):
    def __init__(self,app=None):
        """
        Initialize this extension.
        :param obj app: The Flask application (optional).
        """
        self.app = app
        if app is not None:
            self.init_app(app)
    def init_app(self, app):
        """
        Initialize this extension.
        :param obj app: The Flask application.
        """
        self._init_settings(app)
        app.extensions['dynamo'] = self
        self.table = DynamoTable(app)
    @staticmethod
    def _init_settings(app):
        """Initialize all of the extension settings."""
        app.config.setdefault('DYNAMO_TABLE', app.config.get("DYNAMO_USER_TABLE"))
        app.config.setdefault('DYNAMO_ENABLE_LOCAL', app.config.get("DYNAMO_ENABLE_LOCAL"))
        app.config.setdefault('AWS_REGION', app.config.get("AWS_REGION",'us-east-1'))



# conn = DynamoST(Table="Testing")

# conn.load("my nox group:enabled:123123123#us-east-1")
# print(conn.load('my nox group:GROUP:enabled'))
# print(conn.load('i-12123123:INSTANCE:my nox group'))
# print(conn.load('i-11111113:INSTANCE:my test group#started'))
# print(conn.load('mike:USER:admin'))
# print(conn.query('my nox group'))
# print(conn.query(':INSTANCE:my nox group'))

# group groupId "GROUP" 
# instance instanceId "INSTANCE" groupId
# instanceId, name, cost, state
# user userId "USER" createDate
# name, type

