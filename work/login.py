import requests
import jwt
import bcrypt
import boto3

API_URL = 'https://api.example.com/login'  # Replace with the actual API login endpoint URL
SECRET_KEY = 'your-secret-key'  # Replace with a secret key for JWT encoding and decoding
LAMBDA_FUNCTION_NAME = 'LoginHandlerFunctionArn'  # Replace with the output of your CDK stack
DYNAMODB_TABLE_NAME = 'Users'  # Replace with your DynamoDB table name

def get_token(username, password):
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        token = response.json().get('token')
        return token
    else:
        print(f"Failed to authenticate. Status code: {response.status_code}")
        return None

def save_token_to_file(token):
    with open('token.txt', 'w') as f:
        f.write(token)

def load_token_from_file():
    try:
        with open('token.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def create_jwt_token(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_jwt_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_login_with_lambda(username, password):
    client = boto3.client('lambda')
    payload = {
        "username": username,
        "password": password
    }
    response = client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse',
        Payload=bytes(json.dumps(payload), encoding='utf-8')
    )
    result = json.loads(response['Payload'].read().decode('utf-8'))
    return result.get('is_authenticated', False)

def main():
    # Check if token exists in the file
    token = load_token_from_file()

    if token:
        decoded_token = decode_jwt_token(token)
        if decoded_token:
            print("User already authenticated.")
            print("Decoded token payload:", decoded_token)
        else:
            print("Invalid or expired token. Please log in again.")
            token = None  # Reset token to force reauthentication

    if not token:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Authenticate and get the token
        hashed_password = hash_password(password)  # Hash the provided password
        is_authenticated = verify_login_with_lambda(username, hashed_password)

        if is_authenticated:
            print("User authenticated successfully.")
            token_payload = {
                'username': username
            }
            token = create_jwt_token(token_payload)
            save_token_to_file(token)
            decoded_token = decode_jwt_token(token)
            print("Decoded token payload:", decoded_token)
        else:
            print("Authentication failed.")

    # Now, you can use the token to make authenticated API requests
    # Example: Call API using the token in the Authorization header

if __name__ == '__main__':
    main()
