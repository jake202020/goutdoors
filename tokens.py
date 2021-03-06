"""Create/confirm token for user email confirmation"""

from itsdangerous import URLSafeTimedSerializer
from secrets import SECURITY_PASSWORD_SALT, SECRET_KEY

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
