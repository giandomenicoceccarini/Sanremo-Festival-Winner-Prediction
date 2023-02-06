import numpy as np
import pandas as pd
from pytrends.request import TrendReq


class GTrends:
    trends: pd.DataFrame

    def __init__(self, keywords: list[str], smooth=True):
        self.trend_req = TrendReq()
        list_of_trends = []
        search_suffix = ' cantante'
        for group_of_artists in np.array_split(keywords, max(len(keywords), 5) / 5):
            if len(group_of_artists) > 0:
                self.trend_req.build_payload(kw_list=[f"{x}{search_suffix}" for x in group_of_artists], geo='IT')
                trends = self.trend_req.interest_over_time()
                trends = trends.rename(columns={x: x.replace(search_suffix, '') for x in trends.columns})
                if smooth:
                    trends = self.smoother_trends_over_year(trends)
                list_of_trends.append(trends)
        self.trends = pd.concat(list_of_trends, axis=1)

    @staticmethod
    def smoother_trends_over_year(trends: pd.DataFrame) -> pd.DataFrame:
        smoothed = trends.copy().drop(columns='isPartial').reset_index()
        smoothed['year'] = smoothed['date'].dt.year
        smoothed = smoothed.groupby('year').mean(numeric_only=True)
        return smoothed
