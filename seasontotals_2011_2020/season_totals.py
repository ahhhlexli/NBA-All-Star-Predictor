from basketball_reference_web_scraper import client 
from basketball_reference_web_scraper.data import Location
import pandas as pd 


df = pd.DataFrame()
for year in range(2011, 2021):

    basic = client.players_season_totals(season_end_year=year)
    advanced = client.players_advanced_season_totals(season_end_year=year)
    df_basic = pd.DataFrame(basic)
    df_advanced = pd.DataFrame(advanced)

    df_overall = pd.concat([df_basic, df_advanced], axis=1)
    df_overall = df_overall.loc[:, ~df_overall.columns.duplicated()]
    df_overall['season'] = year

    df = df.append(df_overall)
    print(len(df))


df = df.set_index('name')
df.positions = df.positions.astype(str).str.extract(r'.*\.(\w+):').replace(r'_', value=' ', regex=True)
df.team = df.team.astype(str).str.extract(r'.*\.(\w+)').replace(r'_', value=' ', regex=True)

df['points_off_threes'] = df['made_three_point_field_goals'].apply(lambda x: x*3)
df['points_off_twos'] = (df['made_field_goals'] - df['made_three_point_field_goals']) * 2

df.to_csv('bball_stats.csv')