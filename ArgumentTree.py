from matplotlib.pyplot import tick_params
from ArticleMeta import ArticleMeta
import pandas as pd

class ArgTreeNode:
    def __init__(self, content=None, parent=None, level=None):
        self.level = level
        self.parent = parent
        self.content = content
        self.children = []

    def add_child(self, child):
        if child.level == None:
            child.level = self.level + 1
        child.parent = self
        self.children.append(child)

    def strip(self):
        for child in self.children:
            child.strip()
        self.content = self.content.strip()
        self.content = self.content.replace('\n', ' ')
        return self

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        indentation = self.level * "   "
        result = indentation + self.content + "--" + str(self.level) + "\n";
        for branch in self.children:
            result += branch.__str__()
        return result

    def toJson(self):
        return {
            'content': self.content,
            'children': [child.toJson() for child in self.children],
            'level': self.level
        }

    def append_to_df(self, df: pd.DataFrame, entry: ArticleMeta, idx: int):
        df.loc[len(df.index)] = [
                entry.title, entry.article_url, entry.focal_company,
                entry.ticker, entry.broker, entry.analyst,
                entry.date, self.content, self.level, idx
            ]
        for i in range(len(self.children)):
            self.children[i].append_to_df(df, entry, i)