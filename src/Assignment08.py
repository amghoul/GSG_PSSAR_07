
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import kaggle
import logging

log = logging.getLogger(__name__)

def save_csv(df: pd.DataFrame, path)-> None:
    """ save downloaded datasets to a csv file in the local
    """
    df.to_csv(path,index=False)
    log.info(f" The {path} dataset was Successfully saved!")
def download_load_datasets(csv_save_location: str)-> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame,pd.DataFrame]:
    """Download neflix dataset from Kaggle website, download annual and monthly tempreature datasetrs 
    from two distinct urls and save them as csv file, also load chess dataset from local
    """
    # netflix-shows dataset
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        'shivamb/netflix-shows',
        path=csv_save_location, unzip=True
    )
    log.info("The netflix dataset downloaded successfully")
    netflix = pd.read_csv(os.path.join(csv_save_location,'netflix_titles.csv'))
    # chess_games dataset
    chess = pd.read_csv(os.path.join(csv_save_location,'chess_games.csv'))
    # temp dataset
    temp = pd.read_csv(
    'https://raw.githubusercontent.com/datasets/global-temp/main/data/annual.csv'
    )
    temp_monthly = pd.read_csv(
        "https://raw.githubusercontent.com/datasets/global-temp/main/data/monthly.csv")
    
    save_csv(temp,os.path.join(csv_save_location,'annual.csv'))
    save_csv(temp,os.path.join(csv_save_location,'monthly.csv'))
    return chess, netflix,temp, temp_monthly

def main():
    print("This is for session 8: Visualizations")
    csv_save_location = os.path.join("data","raw")
    charts_save_location = os.path.join("output","charts")
    chess, netflix,temp, temp_monthly = download_load_datasets(csv_save_location)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    main()