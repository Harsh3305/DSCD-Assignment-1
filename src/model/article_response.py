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
