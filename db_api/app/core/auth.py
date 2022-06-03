from passlib.hash import bcrypt_sha256


def hash_password(password: str) -> str:
    """
    Salts and hashes the given password.

    Args:
        password: the plaintext password to hash
    """

    # Securely hash and salt the password. Bcrypt_256 is used to get around the Bcrypt limitations
    # of silently truncating passwords longer than 72 characters as well as not handling NULL bytes.
    return bcrypt_sha256.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies that the given password matches the given hashed password.

    Args:
        password: the plaintext password
        hashed_password: the hashed password used to verify the plaintext password
    """

    return bcrypt_sha256.verify(password, hashed_password)
