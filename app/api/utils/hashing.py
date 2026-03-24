import hashlib
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password: str):
    print("Original password length::", len(password))
    hashed = hashlib.sha256(password.encode()).hexdigest()
    print("After SHA256 length::", len(hashed))
    return password_context.hash(hashed)

def verify_password(plain: str, hashed: str):
    plain_hashed = hashlib.sha256(plain.encode()).hexdigest()
    return password_context.verify(plain_hashed, hashed)