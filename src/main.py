from src.data_loader.load_dataset import Dataset

if __name__ == '__main__':
    df = Dataset.get()
    df.to_csv('data/transformed/sanremo23_dataset.csv', sep=';')

