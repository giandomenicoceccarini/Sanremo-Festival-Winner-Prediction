from dataclasses import dataclass
import pandas as pd

from src.crawler.instagram import InstaCrawler
from src.crawler.wikipedia import WikiCrawler


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
    columns: list[str] = [
        'Artista',
        'Nazionalità',
        'Studio',
        'Raccolte',
        'Periodo di attività musicale',
        'Etichetta',
        'Ospite',
        'ig_follower',
        'ig_follower_ospite',
        'Ultime partecipazioni al Festival',
        'Quota']

    @staticmethod
    def get():
        data = DataLoader('../data').load()
        data['ig_follower'] = data['Artista'].apply(lambda x: InstaCrawler.get_follower(x))
        data['ig_follower_ospite'] = data['Ospite'].apply(lambda x: InstaCrawler.get_follower(x))
        data['info'] = data['Artista'].apply(lambda x: WikiCrawler.get_artist_info(x))
        all_info_df = pd.json_normalize(data['info'])
        selected_info = Dataset.normalize_info_column(all_info_df)

        data = pd.concat([data, selected_info], axis=1)
        return data[Dataset.columns]

    @staticmethod
    def normalize_info_column(all_info_df):
        selected_info = all_info_df[['0.Nazionalità', '0.Paese d\'origine',
                                     '0.Genere', '0.Genere[1]',
                                     '0.Periodo di attività musicale',
                                     '0.Etichetta', '0.Studio', '0.Raccolte', '0.Strumento']].rename(
            columns={'0.Periodo di attività musicale': 'Periodo di attività musicale',}
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
