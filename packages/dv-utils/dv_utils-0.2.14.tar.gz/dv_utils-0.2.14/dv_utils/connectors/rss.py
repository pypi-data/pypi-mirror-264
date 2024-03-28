from dv_utils.connectors.connector import Configuration
from urllib.parse import urlparse
import copy
import feedparser


class RssConfiguration(Configuration):
    schema_file = "rss.json"
    url = None

class RssConnector():
    config: RssConfiguration

    def __init__(self, config: RssConfiguration) -> None:
        self.config = copy.copy(config)

    def get(self):
        # TODO: handle HTTP status code

        # TODO: handle bozo exception
        return feedparser.parse(self.config.url)
