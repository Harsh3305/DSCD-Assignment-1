from src.model.article import Article


class ArticleResponse(Article):
    MAX_CONTENT_SIZE = 200

    def __init__(self, Content: str):
        if len(Content) > self.MAX_CONTENT_SIZE:
            raise Exception("Content size must be less than")
        else:
            self.Content = Content
