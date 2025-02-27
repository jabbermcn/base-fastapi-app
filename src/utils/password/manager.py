from typing import AnyStr

from bcrypt import checkpw, gensalt, hashpw


__all__ = ["PasswordManager"]


class PasswordManager:
    """
    A utility class for hashing and verifying passwords using bcrypt.

    :attribute SALT_ROUNDS: Number of rounds for salt generation (default: 12).
    :attribute SALT_PREFIX: Prefix for the bcrypt hash format (default: b"2b").
    """

    SALT_ROUNDS: int = 12
    SALT_PREFIX: bytes = b"2b"

    @classmethod
    def hash(cls, plain_password: AnyStr) -> str:
        """
        Hashes a plain-text password using bcrypt.

        :param plain_password: The plain-text password (str or bytes).
        :return: The hashed password as a string.
        :raises ValueError: If the password is empty.
        :raises RuntimeError: If hashing fails.
        """

        if isinstance(plain_password, str):
            plain_password = plain_password.encode()

        return hashpw(
            password=plain_password,
            salt=gensalt(rounds=cls.SALT_ROUNDS, prefix=cls.SALT_PREFIX),
        ).decode()

    @classmethod
    def check(cls, plain_password: AnyStr, password_hash: AnyStr) -> bool:
        """
        Verifies a plain-text password against a hashed password.

        :param plain_password: The plain-text password (str or bytes).
        :param password_hash: The hashed password (str or bytes).
        :return: True if the password matches the hash, False otherwise.
        :raises ValueError: If the password or hash is empty.
        """

        if isinstance(plain_password, str):
            plain_password = plain_password.encode()

        if isinstance(password_hash, str):
            password_hash = password_hash.encode()

        return checkpw(password=plain_password, hashed_password=password_hash)
