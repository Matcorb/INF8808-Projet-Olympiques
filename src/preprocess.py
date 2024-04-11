import pandas as pd

def get_top5_medals(dataframe, type):
    if type == "official":
        sorted_df = dataframe.sort_values(by=["Order"], ascending=True).head(5)
    elif type == "total medals":
        sorted_df = dataframe.sort_values(by=["Order by Total"], ascending=True).head(5)
    elif type == "gold":
        sorted_df = dataframe.sort_values(by=["Gold"], ascending=False).head(5)
    elif type == "silver":
        sorted_df = dataframe.sort_values(by=["Silver"], ascending=False).head(5)
    elif type == "bronze":
        sorted_df = dataframe.sort_values(by=["Bronze"], ascending=False).head(5)
    
    return sorted_df
