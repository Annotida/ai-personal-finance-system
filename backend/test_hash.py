from app.security.hashing import hash_password
from app.security.hashing import verify_password

password = "MyPassword123"

hashed = hash_password(password)

print("Hash:", hashed)

print(
    verify_password(
        password,
        hashed
    )
)