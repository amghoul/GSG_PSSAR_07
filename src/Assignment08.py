
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

def q3(df: pd.DataFrame, charts_save_location: str)-> None:
    """ Answering Q3
    GISTEMP annual → line + rolling(10) + fill_between(above/below zero). 
    Annotate the hottest year. Save at 150 dpi
    """
    gistemp = df[df['Source']=='GISTEMP'].copy()
    gistemp['rolling_10'] = gistemp['Mean'].rolling(10, min_periods=1).mean()
    fig, ax = plt.subplots(figsize=(12, 5))
    # Raw annual · 10-year rolling · zero baseline
    ax.plot(gistemp['Year'], gistemp['Mean'], color='#C9A84C', alpha=0.4, label='Annual')
    ax.plot(gistemp['Year'], gistemp['rolling_10'], color='#C0392B', linewidth=2.5, label='10yr avg')
    ax.axhline(y=0, color='grey', linewidth=0.8, linestyle='--')
    # Shade above/below the baseline
    ax.fill_between(gistemp['Year'],0,gistemp['Mean'], where=gistemp['Mean']>0, alpha=0.15, color='#C0392B')
    ax.fill_between(gistemp['Year'],0,gistemp['Mean'], where=gistemp['Mean']<=0, alpha=0.15, color='#3D6B4F')

    ax.set_title('Global Temperature Anomaly 1880–2024', fontsize=13)
    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('Anomaly vs 1951–1980 (°C)', fontsize=11)
    ax.legend(frameon=False, loc='upper left')
    ax.spines[['top','right']].set_visible(False)

    # Annotation
    max_mean = gistemp.sort_values(by='Mean', ascending=False)[['Year', 'Mean']].head(1)['Mean'].iloc[0]
    year_max_mean = gistemp.sort_values(by='Mean', ascending=False)[['Year', 'Mean']].head(1)['Year'].iloc[0]
    ax.annotate(str(year_max_mean)+':'+ str(max_mean.round(2))+'°C',
    xy=(year_max_mean, max_mean), xytext=(2000,
    1.1),
    arrowprops=dict(arrowstyle='->',
    color='black'))
    plt.savefig(os.path.join(charts_save_location,'AQ3.png'), dpi=150, bbox_inches='tight')
    log.info(f"The Q3's chart is saved in {os.path.join(charts_save_location,'AQ3.png')} ")

def q4_a(df: pd.DataFrame, charts_save_location: str)-> None:
    """ Answering AQ4-a
    (a) Histogram of movie duration for netflix dataset
    """
    chart_name = 'AQ4-a_netflix_movie_duration_histogram.png'
    movies = df[df['type']=='Movie']
    movies = movies.dropna(subset=['duration'])
    movies['duration_min'] = movies['duration'].str.replace(' min','').astype(int)
    plt.figure(figsize=(10, 6))

    sns.histplot(
        data=movies, 
        x='duration_min', 
        bins=30,            
        kde=True,           
        color='crimson',   
        edgecolor='black'
    )

    plt.title('Distribution of Netflix Movie Durations', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Duration (Minutes)', fontsize=12)
    plt.ylabel('Count of Movies', fontsize=12)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)

    plt.savefig(os.path.join(charts_save_location,chart_name), dpi=300, bbox_inches='tight')
    log.info(f"The Q4-a's chart is saved in {os.path.join(charts_save_location,chart_name)} ")
    #plt.show()

def q4_b(df: pd.DataFrame, charts_save_location: str)-> None:
    """ Answering AQ4-b
    (b) Top 10 countries (horizontal bar, multi-country split) for netflix dataset
    """
    chart_name = 'AQ4-b_netflix_top10_countries.png'
    countries = (df['country'].dropna()
    .str.split(', ', expand=True)
    .stack()
    .reset_index(drop=True)
    .rename('country').to_frame())
    top10 = countries['country'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(
    top10.index[::-1],
    top10.values[::-1],
    color='#3D6B4F'
    )
    ax.bar_label(bars, padding=5, fontsize=10)
    ax.set_xlabel('Number of Titles', fontsize=11)
    ax.spines[['top','right','left']].set_visible(False)
    ax.tick_params(left=False)
    plt.savefig(os.path.join(charts_save_location,chart_name), dpi=300, bbox_inches='tight')
    log.info(f"The Q4-b's chart is saved in {os.path.join(charts_save_location,chart_name)} ")
    #plt.show()

def q4_c(df: pd.DataFrame, charts_save_location: str)-> None:
    """ Answering AQ4-c
    (c) Stacked bar 2013–2021. for netflix dataset
    """
    chart_name = 'AQ4-c_netflix_stacked_bar.png'
    df['year_added'] = pd.to_datetime(
    df['date_added'].str.strip(),
    errors='coerce').dt.year
    added = (df[df['year_added'].between(2013,2021)]
    .groupby(['year_added','type']).size()
    .reset_index(name='count'))
    wide = added.pivot(
    index='year_added', columns='type',
    values='count').fillna(0)
    fig, ax = plt.subplots(figsize=(9, 5))
    wide.plot(kind='bar', stacked=True, ax=ax,
    color=['#C9A84C','#3D6B4F'],
    edgecolor='white')
    ax.set_xlabel('Year'); ax.set_ylabel('Titles Added')
    ax.tick_params(axis='x', rotation=0)
    ax.legend(title='Type', frameon=False)
    ax.spines[['top','right']].set_visible(False)
    plt.savefig(os.path.join(charts_save_location,chart_name), dpi=300, bbox_inches='tight')
    log.info(f"The Q4-c's chart is saved in {os.path.join(charts_save_location,chart_name)} ")
    #plt.show()

def q5(df: pd.DataFrame, charts_save_location: str)-> None:
    """ Answering AQ5
    Monthly temp → pivot_table(month × decade) → 
    sns.heatmap(cmap='RdYlBu_r', center=0). Use years ≥ 1950.
    """
    chart_name = 'AQ5_temp_heatmap.png'
    temp_m2 = df.copy()
    temp_m2['date'] = pd.to_datetime(temp_m2['Year'], format='%Y-%m')
    temp_m2['year'] = temp_m2['date'].dt.year
    temp_m2['month'] = temp_m2['date'].dt.month
    temp_m2['decade'] = (temp_m2['year'] // 10) * 10
    gm = temp_m2[temp_m2['Source']=='GISTEMP']
    pivot = gm.pivot_table(index='month', columns='decade', values='Mean', aggfunc='mean')
    pivot.index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    fig, ax = plt.subplots(figsize=(14, 5))
    sns.heatmap(pivot[[c for c in pivot.columns if c>=1950]],
    annot=True, fmt='.2f', cmap='RdYlBu_r', center=0,
    linewidths=0.3, ax=ax, cbar_kws={'label':'Anomaly (°C)'})
    ax.set_title('Temperature Anomaly: Month × Decade', fontsize=13)
    ax.set_xlabel('Decade'); ax.set_ylabel('')
    plt.savefig(os.path.join(charts_save_location,chart_name), bbox_inches='tight')
    log.info(f"The Q5's chart is saved in {os.path.join(charts_save_location,chart_name)} ")
    #plt.show()


def main():
    print("This is for session 8: Visualizations")
    csv_save_location = os.path.join("data","raw")
    charts_save_location = os.path.join("output","charts")
    chess, netflix,temp, temp_monthly = download_load_datasets(csv_save_location)
    q1(chess,charts_save_location)
    q2(chess,charts_save_location)
    q3(temp,charts_save_location)
    q4_a(netflix,charts_save_location)
    q4_b(netflix,charts_save_location)
    q4_c(netflix,charts_save_location)
    q5(temp_monthly,charts_save_location)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    main()