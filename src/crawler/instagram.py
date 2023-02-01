from typing import Optional

import requests as requests
from duckduckgo_search import ddg

from src.numerizor.numerize import numerize


class InstaCrawler:
    @staticmethod
    def get_follower(person_name: str) -> Optional[int]:
        keywords = f"{person_name.replace(' ', '+')}+instagram"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        }
        results = ddg(keywords, region='it-it', safesearch='Off', time='n')
        followers = None
        if ig_url := results[0].get('href'):
            ig_page = requests.get(url=ig_url, headers=headers)
            followers = ig_page.text.split('Followers')[0][-10:].split("=")[1].replace('"', "").replace("'", "").strip()
            followers = numerize(followers)
        return followers
