import pandas as pd
from bs4 import BeautifulSoup

from src.crawler.generic_crawler import Crawler


class WikiCrawler(Crawler):
    """
    The class collect methods for retrieve information from Wikipedia
    """

    @staticmethod
    def get_artist_info(person_name: str) -> dict[str, object]:
        """
        The method provide
         - genre
         - album published
         - studio album
         - live album
         - starting career year

        :param person_name:
        :return:
        """
        search_list = [f'{person_name} cantante periodo di attività musicale wikipedia',
                       f'{person_name} cantante wikipedia',
                       f'{person_name} wikipedia']
        if person_name == 'Olly':
            search_list = []  # no wikipedia page for Olly
        wiki_result = None
        for search in search_list:
            if wiki_result := WikiCrawler.get_html_page_of_first_duckduckgo_result(search):
                break
        bs = BeautifulSoup(wiki_result, 'html.parser')

        # class "infobox sinottico" contains html table with artist summary
        try:
            infobox = bs.find(class_='infobox sinottico')
            table_df = pd.concat(pd.read_html(str(infobox)))

            # data cleaning
            columns_dict = table_df.T.iloc[0].to_dict()
            result = table_df.T.iloc[[1]].rename(columns=columns_dict)
            result = result.reset_index().rename(columns={'index': 'Artista'})
            result['Artista'] = result['Artista'].apply(lambda x: x.split('.')[0])
            return result.to_dict(orient='index')
        except ValueError:
            return {}
