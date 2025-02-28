from typing import Annotated

from fastapi import Path
from pydantic import UUID4


ProjectID = Annotated[
    UUID4,
    Path(
        title="Project ID",
        description="<p>Project unique identifier</p>",
        alias="id",
    ),
]
