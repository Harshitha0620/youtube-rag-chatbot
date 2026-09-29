from pydantic import BaseModel, HttpUrl


class YouTubeRequest(BaseModel):

    url: HttpUrl