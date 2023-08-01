import os
import json
import bcrypt
import jwt

USERS_TABLE_NAME = os.environ["USERS_TABLE_NAME"]

def lambda_handler(event, context):
    # Get username and hashed password from the event
    username = event["username"]
    hashed_password = event["password"]

    # Fetch the user's hashed password from DynamoDB
    # You need to implement the logic to fetch the data from DynamoDB here
    # For simplicity, we use a hardcoded hashed password in this example.
    user_password = "hashed_password_from_dynamodb"  # Replace with your code

    # Verify the provided password with the hashed password
    is_authenticated = bcrypt.checkpw(hashed_password.encode(), user_password.encode())

    return {
        "is_authenticated": is_authenticated
    }
