from typing import Annotated

from fastapi import Path
from pydantic import UUID4


UserID = Annotated[
    UUID4,
    Path(
        title="User ID",
        description="<p>User unique identifier</p>",
        alias="id",
    ),
]
