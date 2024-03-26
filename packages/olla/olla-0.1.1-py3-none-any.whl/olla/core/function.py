import io
import re
import sys
from datetime import datetime
from pytz import timezone

from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.document_loaders import WebBaseLoader


class Function:
    @property
    def desc(self):
        raise NotImplementedError()

    @property
    def args(self):
        raise NotImplementedError()

    @property
    def name(self):
        return type(self).__name__

    @property
    def help(self):
        return f"{self.name}: {self.desc}. Input arguments: {self.args}\n"

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class NoFunction(Function):
    @property
    def desc(self):
        return "Using it when there's no need to use any other tools or get the answer you want"

    @property
    def args(self):
        return {}

    def __call__(self, kwargs):
        return "No need to use any tools, I should offer user the final answer"


class WikiSearch(Function):
    def __init__(self):
        self.wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

    @property
    def desc(self):
        return "Using this tool to search Wiki content."

    @property
    def args(self):
        return {"query": "the search string. Be simple."}

    def __call__(self, kwargs):
        return self.wikipedia.run(kwargs["query"])


class DuckDuckGoSearch(Function):
    def __init__(self):
        self.search = DuckDuckGoSearchRun()

    @property
    def desc(self):
        return "Using this tool to access internet and search things that you don't know"

    @property
    def args(self):
        return {"query": "the search keyword. Be procise"}

    def __call__(self, kwargs):
        return self.search.run(kwargs["query"])


class CurrTime(Function):
    @property
    def desc(self):
        return "Using this tool to get the current time"

    @property
    def args(self):
        return {"timezone": "the timezone string. Default value should be 'Asia/Shanghai'."}

    def __call__(self, kwargs):
        tz = timezone(kwargs.get('timezone', 'Asia/shanghai'))
        return datetime.now().astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")


class GetUserInput(Function):
    @property
    def desc(self):
        return "When you are confused with user's question, you can use this tool to ask user for more details"

    @property
    def args(self):
        return {"prompt": "the prompt that you want to ask for more details."}

    def __call__(self, kwargs):
        user_input = input(kwargs["prompt"])
        return user_input

class WebCrawler(Function):
    @property
    def desc(self):
        return "Using this tool to get content from web url"

    @property
    def args(self):
        return {"url": "the web url"}

    def __call__(self, kwargs):
        loader = WebBaseLoader(kwargs["url"])
        document = loader.load()
        return re.sub(r"\n+", "\n", document[0].page_content)

