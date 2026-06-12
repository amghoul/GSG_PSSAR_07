
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

def q1(df: pd.DataFrame, charts_save_location: str)-> None:
    """Answering Q1 
    pivot_table(turns by victory_status × winner) → melt() → 
    sns.barplot(hue='winner'). Annotate the median for each group.
    """
    pivot_tabled_df = df.pivot_table(
    values = 'turns', 
    index = 'victory_status' , 
    columns = 'winner',
    aggfunc = 'median', 
    fill_value = 0,
    ).round(1)
    long = pivot_tabled_df.reset_index().melt(id_vars= 'victory_status' , var_name= 'winner', value_name= 'median_turns' )
    ax = sns.barplot(data=long, x= 'victory_status' , y='median_turns' , hue='winner')
    for container in ax.containers:
        labels = [f'{v.get_height():.1f}' for v in container]
        ax.bar_label(container, labels=labels, padding=2, fontsize=9)
    plt.title('Median Turns by Victory Status and Winner', fontsize=14, y=1.02)
    plt.savefig(os.path.join(charts_save_location,'AQ1.png'), dpi=150, bbox_inches='tight')
    #plt.show()
    log.info(f"The Q1's chart is saved in {os.path.join(charts_save_location,'AQ1.png')} ")

def main():
    print("This is for session 8: Visualizations")
    csv_save_location = os.path.join("data","raw")
    charts_save_location = os.path.join("output","charts")
    chess, netflix,temp, temp_monthly = download_load_datasets(csv_save_location)
    q1(chess,charts_save_location)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    main()