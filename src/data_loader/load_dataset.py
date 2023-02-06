from dataclasses import dataclass

import pandas as pd

from src.crawler.instagram import InstaCrawler
from src.crawler.wikipedia import WikiCrawler
from src.google_trends.g_trends import GTrends


@dataclass
class DataLoader:
    """This class is used as I/O manager"""
    BASE_PATH: str

    def load(self) -> pd.DataFrame:
        """
        Load data from local folder.

        :return:
        """
        participants: pd.DataFrame = pd.read_csv(f"{self.BASE_PATH}/participants.csv", sep=";")
        songs: pd.DataFrame = pd.read_csv(f"{self.BASE_PATH}/songs.csv", sep=";")
        collaboration: pd.DataFrame = pd.read_csv(f"{self.BASE_PATH}/collaboration.csv", sep=";")

        quote: pd.DataFrame = pd.read_csv(f"{self.BASE_PATH}/quote.csv", sep=";")

        df = participants.merge(songs, left_on="Interprete", right_on="Artista")
        df = df.merge(collaboration, left_on="Artista", right_on="Artista")
        df = df.merge(quote, left_on='Artista', right_on='Artista')

        return df.drop(columns=["Interprete"])


class DataEnricher:
    """Enrich dataframe with additional info"""

    @staticmethod
    def normalize_info_column(all_info_df):
        """
        Adjust columns names.

        :param all_info_df:
        :return:
        """
        selected_info = all_info_df[['0.Nazionalità', '0.Paese d\'origine',
                                     '0.Genere', '0.Genere[1]',
                                     '0.Periodo di attività musicale',
                                     '0.Etichetta', '0.Studio', '0.Raccolte', '0.Strumento']].rename(
            columns={'0.Periodo di attività musicale': 'Periodo di attività musicale'}
        )
        selected_info = selected_info.rename(columns={col: col.replace('0.', '') for col in selected_info.columns})
        if 'Pasese d\'origine' in selected_info.columns and 'Nazionalità' in selected_info.columns:
            selected_info['Nazionalità'] = selected_info['Nazionalità'].combine_first(
                selected_info['Pasese d\'origine'])
            selected_info = selected_info.drop(columns=['Pasese d\'origine'])
        if 'Genere[1]' in selected_info.columns and 'Genere' in selected_info.columns:
            selected_info['Genere'] = selected_info['Genere'].combine_first(selected_info['Genere[1]'])
            selected_info = selected_info.drop(columns=['Genere[1]'])
        return selected_info

    @staticmethod
    def enrichment_pipeline(data: pd.DataFrame,
                            google_trends_enricher: bool = True,
                            wiki_enricher: bool = True,
                            ig_enricher: bool = True) -> pd.DataFrame:
        """
        Enrich original data with more data.

        :param ig_enricher:
        :param wiki_enricher:
        :param google_trends_enricher:
        :param data:
        :return:
        """
        if ig_enricher:
            data = DataEnricher.ig_enricher(data)
        if wiki_enricher:
            data = DataEnricher.wikipedia_enricher(data)
        if google_trends_enricher:
            data = DataEnricher.google_trends_enricher(data)
        return data

    @staticmethod
    def wikipedia_enricher(data: pd.DataFrame) -> pd.DataFrame:
        """
        Use the WikiCrawler to get artist info.

        :param data:
        :return:
        """
        # wikipedia enricher
        data['info'] = data['Artista'].apply(lambda x: WikiCrawler.get_artist_info(x))
        all_info_df = pd.json_normalize(data['info'])
        selected_info = DataEnricher.normalize_info_column(all_info_df)
        data = pd.concat([data, selected_info], axis=1)
        return data

    @staticmethod
    def ig_enricher(data: pd.DataFrame) -> pd.DataFrame:
        """
        Use the InstaCrawler for get instagram followers.

        :param data:
        :return:
        """
        # ig enricher
        data['ig_follower'] = data['Artista'].apply(lambda x: InstaCrawler.get_follower(x))
        data['ig_follower_ospite'] = data['Ospite'].apply(lambda x: InstaCrawler.get_follower(x))
        return data

    @staticmethod
    def google_trends_enricher(data: pd.DataFrame) -> pd.DataFrame:
        """
        Use the GTrends class for get Google Trends info.

        :param data:
        :return:
        """
        all_artists: list[str] = list(data['Artista'].unique())
        g_trends_obj: GTrends = GTrends(keywords=all_artists, smooth=True)
        gtrends_df: pd.DataFrame = g_trends_obj.trends.T
        gtrends_df = gtrends_df.rename(columns={year: f"gtrend_{year}" for year in gtrends_df.columns})
        data = data.set_index("Artista").join(gtrends_df).reset_index()
        return data


class Dataset:
    """
    This class is used as a main class for get the dataset.
    """

    columns: list[str] = [
        'Artista',
        'Nazionalità',
        'Studio',
        'Raccolte',
        'Periodo di attività musicale',
        'Etichetta',
        'Genere',
        'Ospite',
        'ig_follower',
        'ig_follower_ospite',
        'Ultime partecipazioni al Festival',
        'gtrend_2018',
        'gtrend_2019',
        'gtrend_2020',
        'gtrend_2021',
        'gtrend_2022',
        'gtrend_2023',
        'Quota']

    @staticmethod
    def get():
        """
        Get the dataset, loading data from folder and running the enrichment pipeline.

        :return:
        """
        data: pd.DataFrame = DataLoader('../data').load()
        data: pd.DataFrame = DataEnricher.enrichment_pipeline(data)
        return data[Dataset.columns]
