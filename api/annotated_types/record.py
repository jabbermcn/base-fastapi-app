from typing import Annotated

from fastapi import Path
from pydantic import UUID4


RecordID = Annotated[
    UUID4,
    Path(
        title="Record ID",
        description="<p>Record unique identifier</p>",
        alias="id",
    ),
]
