class ArticleMeta:

    def __init__(self, title, date, broker, analyst, article_link, company,
                 ticker, article_path):
        self.title = title
        self.date = date
        self.broker = broker
        self.analyst = analyst
        self.article_url = article_link
        self.focal_company = company
        self.ticker = ticker
        self.article_path = article_path
        self.textual_arguments = []

    def __str__(self):
        return f"{self.title} {self.date} {self.broker} {self.analyst} {self.article_link} {self.ticker} {self.article_path}"

    def toJson(self):
        return self.__dict__
