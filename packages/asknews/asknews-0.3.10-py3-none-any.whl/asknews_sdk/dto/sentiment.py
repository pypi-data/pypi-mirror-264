from __future__ import annotations

from typing import Annotated
from pydantic import AwareDatetime, BaseModel, Field

from asknews_sdk.dto.base import BaseSchema


class SentimentResponseTimeSeriesData(BaseModel):
    datetime: Annotated[AwareDatetime, Field(title='Datetime')]
    value: Annotated[int, Field(title='Value')]


class SentimentResponseTimeSeries(BaseModel):
    timeseriesData: Annotated[
        list[SentimentResponseTimeSeriesData], Field(title='Timeseriesdata')
    ]


class SentimentResponseData(BaseModel):
    getMetric: SentimentResponseTimeSeries


class SentimentResponse(BaseSchema):
    data: SentimentResponseData
