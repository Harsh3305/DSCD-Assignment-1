from datetime import datetime


class Article:
    def __init__(self, Type: str, Author: str, Time: datetime):
        datetime.now()
        self.Type = Type
        self.Author = Author
        self.Time = Time
