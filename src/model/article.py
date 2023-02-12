class Article:
    def __init__(self, Type: str, Author: str, Date: str):
        self.Type = Type
        self.Author = Author
        self.Date = Date

    def to_json(self):
        return {
            "Type": self.Type,
            "Author": self.Author,
            "Date": self.Date
        }

    @staticmethod
    def from_json(json_obj: dict):
        return Article(
            Type=json_obj["Type"],
            Author=json_obj["Author"],
            Date=json_obj["Date"]
        )
