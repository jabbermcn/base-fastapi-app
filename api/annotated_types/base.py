from typing import Annotated

from fastapi import Query


PageQuery = Annotated[int, Query(ge=1, description="<p>The page number, a positive integer value</p>")]
PageSizeQuery = Annotated[
    int,
    Query(
        ge=1,
        le=100,
        alias="pageSize",
        description="<p>The number of projects per page (from 1 to 100)</p>",
    ),
]
