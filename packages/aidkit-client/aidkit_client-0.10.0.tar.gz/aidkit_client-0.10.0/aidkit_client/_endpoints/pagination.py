from pydantic import BaseModel


class PaginationParameters(BaseModel):
    limit: int = 100
    offset: int = 0
