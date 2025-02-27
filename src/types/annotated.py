import re

from typing import Annotated

from pydantic import Field


__all__ = ["PasswordStr", "JWTStr"]


PasswordStr = Annotated[
    str,
    Field(
        pattern=re.compile(pattern=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[!-~]+$"),
        min_length=8,
        max_length=64,
        examples=["VeryStrongPassword1!"],
    ),
]
JWTStr = Annotated[
    str,
    Field(
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
            "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        ]
    ),
]
