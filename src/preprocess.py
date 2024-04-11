import pandas as pd
from datetime import datetime

def get_top5_medals_by_date(dataframe, day, type):
    date = datetime(year=2022, month=2, day=day)
    filtered_df = dataframe[dataframe["Date"] == date]
    if type == "total medals":
        sorted_df = filtered_df.sort_values(by=["Total"], ascending=False).head(5)
    elif type == "gold":
        sorted_df = filtered_df.sort_values(by=["Gold"], ascending=False).head(5)
    elif type == "silver":
        sorted_df = filtered_df.sort_values(by=["Silver"], ascending=False).head(5)
    elif type == "bronze":
        sorted_df = filtered_df.sort_values(by=["Bronze"], ascending=False).head(5)
    return sorted_df

def extract_countries_from_athletes(dataframe):
    return dataframe[['medal_type', 'medal_date', 'country', 'event']].drop_duplicates().drop(columns=['event'])

def get_country_totals_per_date(dataframe):
    dataframe['Date'] = pd.to_datetime(dataframe['medal_date'])
    dataframe = dataframe.rename(columns={'country': 'Country'})
    grouped_df = dataframe.groupby(['Date', 'Country', 'medal_type']).size().unstack(fill_value=0).reset_index()
    
    dates = get_dates(grouped_df)
    countries = grouped_df['Country'].unique()
    date_country_df = pd.DataFrame([(date, country) for date in dates for country in countries], columns=['Date', 'Country'])
    merged_df = pd.merge(date_country_df, grouped_df, on=['Date', 'Country'], how='left').fillna(0)
    merged_df['Gold'] = merged_df.groupby('Country')['Gold'].cumsum()
    merged_df['Silver'] = merged_df.groupby('Country')['Silver'].cumsum()
    merged_df['Bronze'] = merged_df.groupby('Country')['Bronze'].cumsum()

    merged_df['Total'] = merged_df['Gold'] + merged_df['Silver'] + merged_df['Bronze']
    return merged_df[['Country', 'Gold', 'Silver', 'Bronze', 'Total', 'Date']]

def get_dates(dataframe):
    return pd.date_range(start=dataframe['Date'].min(), end=dataframe['Date'].max(), freq='D')
