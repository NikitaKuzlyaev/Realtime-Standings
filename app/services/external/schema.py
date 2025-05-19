import time

from pydantic import BaseModel, Field


class ParamsInContestStatus(BaseModel):
    contestId: int
    apiKey: int
    time_: int = Field(alias="time", default=time.time())
    from_: int = Field(alias="from", default=1)
    count: int = Field(default=10)

    class Config:
        allow_population_by_field_name = True
