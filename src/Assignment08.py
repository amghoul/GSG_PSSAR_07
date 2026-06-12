
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

def q2(df: pd.DataFrame, charts_save_location: str)-> None:
    """Answering Q2
    Choose any player with 15+ games. Plot raw rating + rolling(5) + expanding avg. 
    Annotate their highest-rated game
    """
    white_games= df['white_id'].value_counts()
    player_name = white_games[white_games >=15].index[0]
    player = df[df['white_id']==player_name].sort_values('game_id').reset_index(drop=True)
    player['rolling_5_rating'] = player['white_rating'].rolling(window=5).mean()
    player['cum_avg_rating' ] =player['white_rating' ].expanding().mean()

    max_rating = player['white_rating'].max()
    max_game_index = player['white_rating'].idxmax()

    plt.figure(figsize=(12, 6))

    plt.plot(player.index, player['white_rating'], label='Raw Rating', color='lightgray', alpha=0.9, linestyle='--')
    plt.plot(player.index, player['rolling_5_rating'], label='5-Game Rolling Average', color='blue', linewidth=2)
    plt.plot(player.index, player['cum_avg_rating'], label='Cumulative Average', color='orange', linewidth=2)

    # Annotate the highest-rated -game
    plt.annotate(
        f'Peak Rating: {max_rating}', 
        xy=(max_game_index, max_rating),         
        xytext=(max_game_index + 2, max_rating + 15), 
        arrowprops=dict(
            facecolor='black',                    
            arrowstyle='->',                      #
            lw=1.5                                
        ),
        fontweight='bold',
        color='red'                               
    )

    plt.scatter(max_game_index, max_rating, color='red', s=50, zorder=5)
    # Add chart elements
    plt.title(f'Rating Progression Trends for Player: {player_name}', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Games Played')
    plt.ylabel('Rating')
    plt.legend(title='Rating Metrics')  # Explains which line is which
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(charts_save_location,'AQ2.png'), dpi=150, bbox_inches='tight')
    log.info(f"The Q2's chart is saved in {os.path.join(charts_save_location,'AQ2.png')} ")
    #plt.show()


def main():
    print("This is for session 8: Visualizations")
    csv_save_location = os.path.join("data","raw")
    charts_save_location = os.path.join("output","charts")
    chess, netflix,temp, temp_monthly = download_load_datasets(csv_save_location)
    q1(chess,charts_save_location)
    q2(chess,charts_save_location)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    main()