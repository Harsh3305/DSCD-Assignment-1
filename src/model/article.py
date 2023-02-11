from datetime import datetime


class Article:
    def __init__(self, Type: str, Author: str, Date: datetime):
        datetime.now()
        self.Type = Type
        self.Author = Author
        self.Date = Date
