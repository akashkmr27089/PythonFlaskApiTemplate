from pydantic import BaseModel, Field
from typing import Optional, Union


class ResponseModel(BaseModel):
    data: Optional[Union[dict, list]]
    error: Optional[bool] = Field(False)
    message: Optional[str] = Field("")
    status_code: Optional[int] = Field(200)


class FrequentWordsModel:
    word: str
    meanings: [Optional[str]]
    message: Optional[str] = Field("")
