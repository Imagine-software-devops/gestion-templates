import os
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_dynamodb as dynamodb
from aws_cdk import core
import bcrypt
import jwt

class AuthStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # DynamoDB Table to store user credentials
        table = dynamodb.Table(
            self, "UsersTable",
            partition_key=dynamodb.Attribute(name="username", type=dynamodb.AttributeType.STRING)
        )

        # Lambda Function to verify login
        lambda_fn = _lambda.Function(
            self, "LoginHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "USERS_TABLE_NAME": table.table_name
            }
        )
        table.grant_read_data(lambda_fn)

        # Output the Lambda function ARN
        core.CfnOutput(
            self, "LoginHandlerFunctionArn",
            value=lambda_fn.function_arn
        )


app = core.App()
AuthStack(app, "AuthStack")
app.synth()
