from typing import Literal, Union, Annotated
from fastapi import Query
from pydantic import BaseModel, Field

class CommonQueryParams(BaseModel):
    page_size: int = Field(default=10, le=100, ge=1, description="Number of items returned")
    page_no: int = Field(default=1, ge=1, description="Number of page")
    sort_by: Union[Literal["created_at", "modified_at"], None] = None
    order: Literal["asc", "desc"] = "asc"

    @property
    def offset(self):
        return self.page_size * (self.page_no - 1)

CommonFilters = Annotated[CommonQueryParams, Query()]
