#!/usr/bin/env python3

#importing necessary modules for data wragling and visulizations
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#=========TODO=========
#Read each csv files as pandas dataFrame 
df1 = pd.read_csv("./data/brasil-real-estate-1.csv")
df2 = pd.read_csv("./data/brasil-real-estate-2.csv")

def clean_data():
    """
    this function do every thing about cleaning the data
    this include:
        - droping null values in the data
        - creating new important columns from existing ones
        - removing unimportant characters from price_usd column
        - changing datatype of values to as to help us for math operations
        - removing uncessary columns after creating new ones

    """
    # drop 'NaN' values
    df1.dropna(inplace = True)
    df2.dropna(inplace = True)
    # get the state name from 'place_with_parent_names' column
    df1["state"] = df1["place_with_parent_names"].str.split("|", expand=True)[2]
    
    # put lat-lon column in separate 'lat' and 'lon' column
    df1[["lat", "lon"]] = df1["lat-lon"].str.split(",", expand=True)

    # remove the $ sign and comma (,) in price_usd col of df1
    df1["price_usd"] = (df1["price_usd"]
                        .str.replace("$", "")
                        .str.replace(",", "")
                        .astype(float))

    # change price_brl to price_usd for df2
    df2["price_usd"] = (df2["price_brl"] / 3.19).round(2)

    # drop uncessary columns from both data frames
    df1.drop(columns=["place_with_parent_names", "lat-lon"], inplace=True)
    df2.drop(columns=["price_brl"], inplace=True)
    
    # add price_per_m2 column

    df1["price_per_m2"] = (df1["price_usd"] / df1["area_m2"]).round(2)
    df2["price_per_m2"] = (df2["price_usd"] / df2["area_m2"]).round(2)

# concatinate both cleaned dataframes
def create_df(df1, df2):
    """return concaticated dataFrame from the existing data frames"""
    df = pd.concat([df1, df2], 0)
    return df


def correlate(df):
    correlation = df["area_m2"].corr(df["price_usd"])
    return correlation

def summary_stat(df):
    # Return summerized statistics about the data
    return df[["area_m2", "price_usd"]].describe()    


# the following 
def create_scatter_map(df):    
    fig = px.scatter_mapbox(
        df,
        lat=df["lat"],
        lon=df["lon"],
        center= {"lat": -14.2, "lon":-51.9},
        width=1080,
        height=720,
        hover_data=["price_usd"]
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.show()


def plot_hist(df):
    plt.hist(df["price_usd"])
    plt.xlabel("Price[USD]")
    plt.ylabel("Frequency")
    plt.title ( "Distribution of Home Prices")
    plt.show()

def plot_mean_price_m2(df):
    """this function plots the mean price per_square_meter Vs state
        this is the most convenient way to show which state is more expensive"""
    (df.groupby("state")["price_per_m2"]
    .mean().sort_values(ascending = True)
    .plot(kind="bar",
    xlabel = "state",
    ylabel = "mean price per m2")
    )
    plt.show()
    
def plot_mean_price_by_state(df):
    """plots the mean_price Vs state"""
    mean_price_by_state =  (df.groupby("state")["price_usd"]
            .mean().sort_values(ascending = False))
    mean_price_by_state.plot(
        kind = "bar",
        xlabel = "state",
        ylabel = "Mean price [USD]",
        title = "Mean home price by State"
    )
    plt.show()
    
    


def main():
    clean_data()
    df = create_df(df1, df2)
    plot_mean_price_m2(df)
   
if __name__ == "__main__":
    main()

