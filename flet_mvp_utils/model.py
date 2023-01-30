from pydantic import BaseModel


class MvpModel(BaseModel):
    class Config:
        allow_mutation = False

    pass
