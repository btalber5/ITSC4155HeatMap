from itsdangerous import URLSafeTimedSerializer
import configparser

# Configuration
config = configparser.ConfigParser()
config.read('configuration.ini')
default = config['DEFAULT']
SECRET_KEY = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
SECURITY_PASSWORD_SALT = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email