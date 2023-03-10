from typing import Optional

from src.crawler.generic_crawler import Crawler
from src.numerizor.numerize import numerize


class InstaCrawler(Crawler):
    @staticmethod
    def get_follower(person_name: str) -> Optional[int]:
        if person_name == 'Articolo 31':
            search = 'https://www.instagram.com/j.axofficial/'
        elif person_name == 'Shari':
            search = 'https://www.instagram.com/sharinoioso/?hl=it'
        elif person_name == 'Will':
            search = 'https://www.instagram.com/will_buse/'
        else:
            search = f"{person_name} instagram"
        ig_page: str = InstaCrawler.get_html_page_of_first_duckduckgo_result(search)
        followers = None
        if ig_page:
            try:
                followers = ig_page.split('Followers')[0][-10:].split("=")[1].replace('"', "").replace("'", "").strip()
                followers = numerize(followers) if followers else None
            except IndexError:
                followers = None
        return followers
