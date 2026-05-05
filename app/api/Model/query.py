from pydantic import BaseModel


class qReq(BaseModel):
    query: str