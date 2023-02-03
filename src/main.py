import os
from datetime import datetime

from src.data_loader.load_dataset import Dataset

if __name__ == '__main__':
    df = Dataset.get()
    now = datetime.now().strftime('%Y%m%d_%H%M')
    df.to_csv(f'../data/transformed/sanremo23_dataset{now}.csv', sep=';')

