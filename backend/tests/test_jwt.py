from app.security.jwt_handler import (
    create_access_token,
    verify_access_token
)

token = create_access_token(
    {
        "sub": "john@email.com"
    }
)

print(token)

print(
    verify_access_token(token)
)