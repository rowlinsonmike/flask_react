from flask_dynamo import Dynamo

def flask_dynamo_app(app):
    app.config['DYNAMO_TABLES'] = [
            {
                "TableName":app.config.get("DYNAMO_USER_TABLE"),
                "KeySchema":[dict(AttributeName='username', KeyType='HASH')],
                "AttributeDefinitions":[dict(AttributeName='username', AttributeType='S')],
                "ProvisionedThroughput":dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
            }
        ]
    dynamo = Dynamo()
    dynamo.init_app(app)
    return app