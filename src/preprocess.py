import pandas as pd
from datetime import datetime


def get_top5_medals_by_date(dataframe, day, type):
    date = datetime(year=2022, month=2, day=day)
    filtered_df = dataframe[dataframe["Date"] == date]
    if type == "official":
        sorted_df = filtered_df.sort_values(by=["Official"], ascending=False).head(5)
    elif type == "total medals":
        sorted_df = filtered_df.sort_values(by=["Total"], ascending=False).head(5)
    elif type == "gold":
        sorted_df = filtered_df.sort_values(by=["Gold"], ascending=False).head(5)
    elif type == "silver":
        sorted_df = filtered_df.sort_values(by=["Silver"], ascending=False).head(5)
    elif type == "bronze":
        sorted_df = filtered_df.sort_values(by=["Bronze"], ascending=False).head(5)
    return sorted_df


def extract_countries_from_athletes(dataframe):
    return (
        dataframe[["medal_type", "medal_date", "country", "event"]]
        .drop_duplicates()
        .drop(columns=["event"])
    )


def get_country_totals_per_date(dataframe):
    dataframe["Date"] = pd.to_datetime(dataframe["medal_date"])
    dataframe = dataframe.rename(columns={"country": "Country"})
    grouped_df = (
        dataframe.groupby(["Date", "Country", "medal_type"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    dates = get_dates(grouped_df)
    countries = grouped_df["Country"].unique()
    date_country_df = pd.DataFrame(
        [(date, country) for date in dates for country in countries],
        columns=["Date", "Country"],
    )
    merged_df = pd.merge(
        date_country_df, grouped_df, on=["Date", "Country"], how="left"
    ).fillna(0)
    merged_df["Gold"] = merged_df.groupby("Country")["Gold"].cumsum()
    merged_df["Silver"] = merged_df.groupby("Country")["Silver"].cumsum()
    merged_df["Bronze"] = merged_df.groupby("Country")["Bronze"].cumsum()

    merged_df["Total"] = merged_df["Gold"] + merged_df["Silver"] + merged_df["Bronze"]
    merged_df["Official"] = (
        merged_df["Gold"] * 10000 + merged_df["Silver"] * 100 + merged_df["Bronze"]
    )
    return merged_df[
        ["Country", "Gold", "Silver", "Bronze", "Total", "Official", "Date"]
    ]


def get_dates(dataframe):
    return pd.date_range(
        start=dataframe["Date"].min(), end=dataframe["Date"].max(), freq="D"
    )


def get_top_medals(dataframe, medal_type, graph_type, sort_method):
    # Remove hockey since it pollutes the data
    dataframe = dataframe[dataframe["discipline"] != "Ice Hockey"]

    dataframe = add_total_medals(dataframe, medal_type)

    sort_keys = [
        "discipline",
        medal_type,
        "athlete_name" if graph_type == "athlete" else "country",
    ]
    sort_ascending = [True, False, True]

    if medal_type == "total" and sort_method == ["weighted"]:
        dataframe["official"] = (
            dataframe["gold"] * 10000 + dataframe["silver"] * 100 + dataframe["bronze"]
        )
        sort_keys[1] = "official"

    dataframe = dataframe.sort_values(by=sort_keys, ascending=sort_ascending)

    dataframe = (
        dataframe.groupby("discipline")
        .apply(lambda x: x.sort_values(by=sort_keys[1], ascending=False))
        .reset_index(drop=True)
    )
    dataframe["position"] = dataframe.groupby("discipline").cumcount() + 1
    dataframe["percent"] = dataframe[medal_type] / dataframe["total_medals"] * 100
    dataframe["position_label"] = dataframe["position"].apply(lambda x: f"Top {x}")

    return dataframe


def add_total_medals(dataframe, medal_type):
    total_medals = (
        dataframe.groupby("discipline")[medal_type].sum().rename("total_medals")
    )
    return dataframe.merge(total_medals, on="discipline", how="inner")


# Viz 1
def athlete_age(athletes):
    athletes["birth_date"] = pd.to_datetime(athletes["birth_date"])
    age_timedelta = datetime.now() - athletes["birth_date"]
    athletes["age"] = age_timedelta // pd.Timedelta(365.25, unit="D")
    athletes = athletes.dropna(
        subset=["age"]
    )  # Remove athletes whose age is unknown (nan)
    return athletes


def medal_athlete_age(medals, athletes):
    medals["name"] = medals["athlete_name"]
    medals = pd.merge(
        medals[["name"]],
        athletes[["name", "gender", "discipline", "age"]],
        on="name",
        how="left",
    )
    return medals


# Viz 4
def line_bar_data(athletes, medals_total):

    # Preprocess athletes per country
    athletes_per_country = pd.DataFrame(athletes["country"].value_counts())

    # Preprocess medals per country
    medals_total.index = medals_total["Country"]
    medals_total.drop(
        columns=[
            "Order",
            "Country",
            "Gold",
            "Silver",
            "Bronze",
            "Order by Total",
            "Country Code",
        ],
        inplace=True,
    )

    # Create line-bar graph data
    line_bar_data = athletes_per_country.combine_first(medals_total).fillna(0)
    line_bar_data = line_bar_data.sort_values(by="count", ascending=False)
    line_bar_data["medals_per_100"] = round(
        100 * line_bar_data["Total"] / line_bar_data["count"], 1
    )
    return line_bar_data
