from datetime import datetime

from src.model.article import Article


class ArticleResponse(Article):
    MAX_CONTENT_SIZE = 200

    def __init__(self, Content: str, Author: str, Date: str, Type: str):
        super().__init__(
            Author=Author,
            Date=Date,
            Type=Type
        )
        if len(Content) > self.MAX_CONTENT_SIZE:
            raise Exception("Content size must be less than")
        else:
            self.Content = Content

    def to_json(self):
        json_obj = super().to_json()
        json_obj["Content"] = self.Content
        return json_obj

    @staticmethod
    def from_json(json_obj: dict):
        return ArticleResponse(
            Type=json_obj["Type"],
            Author=json_obj["Author"],
            Date=json_obj["Date"],
            Content=json_obj["Content"],
        )
