from typing import Optional

import requests as requests
from duckduckgo_search import ddg
from requests import Response


class Crawler:
    @staticmethod
    def get_html_page_of_first_duckduckgo_result(search: str) -> Optional[str]:
        """
        Search on DuckDuckGo and return the html of the first result.

        :param search: keywords to search on duckduckgo
        :return:
        """
        keywords = f"{search.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                          "Version/16.3 Safari/605.1.15",
        }
        results = ddg(keywords, region='it-it', safesearch='Off')
        if results:
            if url_ := results[0].get('href'):
                page = requests.get(url=url_, headers=headers)
                if page.status_code == 200:
                    return page.text
        return None
