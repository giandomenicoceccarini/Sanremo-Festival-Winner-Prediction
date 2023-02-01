from dataclasses import dataclass
import pandas as pd

from src.crawler.instagram import InstaCrawler


@dataclass
class DataLoader:
    BASE_PATH: str

    def load(self):
        participants: pd.DataFrame = pd.read_csv(f"{self.BASE_PATH}/participants.csv", sep=";")
        songs: pd.DataFrame = pd.read_csv(f"{self.BASE_PATH}/songs.csv", sep=";")
        collaboration: pd.DataFrame = pd.read_csv(f"{self.BASE_PATH}/collaboration.csv", sep=";")

        quote: pd.DataFrame = pd.read_csv(f"{self.BASE_PATH}/quote.csv", sep=";")

        df = participants.merge(songs, left_on="Interprete", right_on="Artista")
        df = df.merge(collaboration, left_on="Artista", right_on="Artista")
        df = df.merge(quote, left_on='Artista', right_on='Artista')

        return df.drop(columns=["Interprete"])


class Dataset:
    @staticmethod
    def get():
        data = DataLoader('../data').load()
        data['ig_follower'] = data['Artista'].apply(lambda x: InstaCrawler.get_follower(x))
        data['ig_follower_ospite'] = data['Ospite'].apply(lambda x: InstaCrawler.get_follower(x))
        return data[['Artista', 'Ospite', 'ig_follower', 'ig_follower_ospite', 'Ultime partecipazioni al Festival', 'Quota']]
