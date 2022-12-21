import streamlit as st # installing streamlit
import pandas as pd # installing panda
import numpy as np # it is for working with arrays
from matplotlib import pyplot
import matplotlib.pyplot as plt
import seaborn as sns; #sns.set(rc={'axes.facecolor':(0,0,0,0),'figure.facecolor':(0,0,0,0)}) # I think it is a new package we did use. It's for data visualization
from PIL import Image # This is also a new package we didn't use. I think

df_cars = pd.read_csv("usedcars.csv")

def run():

    # Defining Site Tab and Data Frame
    st.set_page_config(page_title="Craiglist Car Analytics", # Site tab title
                   page_icon="car", # site favicon (the site tab icon)
                   layout = "wide")
    st.title(":car: Car Dashboard")
    img = Image.open("craiglist.png")
    st.sidebar.image(img)
    st.sidebar.markdown("<h3 style='text-align: center; color: blue;'>Information Page</h3>",
                unsafe_allow_html=True)
    st.sidebar.markdown("<h5 style='text-align: center; color: blue;'>Welcome to Car Dashboard. This is a website for you to learn more about the car industry. There are two tabs on the webpage. The first tab is a tab that will assist you with filtering out data. The second tab is a tab that you can use to extract insights about a specific car manufacturer.</h5>",
                unsafe_allow_html=True)

    tabf, taba = st.tabs(["Filter Page","Analysis Page"])
    # ____SIDEBAR_____
    # Car brand selection
    tabf.header("Data Extraction")
    manufacturer = tabf.multiselect(
        "Select the car brand: ",
        options = list(df_cars["manufacturer"].unique()),
        default = sorted(list(df_cars[df_cars["manufacturer"].isna() != True]["manufacturer"].unique()))[4:6]
    )

    # Car year selection
    year = tabf.multiselect(
        "Select the car year: ",
        options=list(df_cars["year"].unique()),
        default= sorted(list(df_cars[df_cars["year"].isna() != True]["year"].unique()))[-3:]
    )

    # Car condition selection
    condition = tabf.multiselect(
        "Select the car condition: ",
        options= list(df_cars["condition"].unique()),
        default= sorted(list(df_cars[df_cars["condition"].isna() != True]["condition"].unique()))[:2]
    )

    df_selection = df_cars.query(
        "manufacturer == @manufacturer & year == @year & condition == @condition"
    )


    # Display site dataframe
    tabf.markdown("<h4 style='text-align: center; color: white;'>Data Frame for Cars</h4>",
                unsafe_allow_html=True)
    tabf.dataframe(df_selection)


    # ___MAIN PAGE___
    taba.header("Manufacturer Insights")
    manufacturer = taba.selectbox("Choose a manufacturer:", list(df_cars[df_cars["manufacturer"].isna() != True]["manufacturer"].unique()))
    def condition_price(manufacturer):
        df_cars_new = df_cars[df_cars["manufacturer"] == manufacturer]

        #condition = st.selectbox("Choose a condition:", list(df_cars[df_cars["condition"].isna() != True]["condition"].unique()))

        #df_cars_condition = df_cars_new[df_cars_new["condition"]==condition]
        df_cars_price = df_cars_new.groupby("condition", as_index = False)["price"].mean()

        return df_cars_price

    tab1, tab2, tab3, tab4,tab5 = taba.tabs(["Price Rankings", "Price Trend", "Geospatial Distribution", "Further Insights", "Variable Check"])
    df_car_use = condition_price(manufacturer)
    df_car_use = df_car_use.sort_values("price", ascending = False)

    fig, ax = plt.subplots(figsize=(12,8))
    sns.barplot(y="price", x="condition", data=df_car_use, color = "blue")
    ax.set_title("Price Rankings for %s"%(manufacturer),fontdict= {'fontsize': 20, 'fontweight':'bold'})
    ax.set_xlabel("Price")
    ax.set_ylabel("Condition")
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.title.set_color('black')
    #ax.tick_params(axis='x', colors='black')
    #ax.tick_params(axis='y', colors='black')
    tab1.pyplot(fig)

    df_trendprice = df_cars[(df_cars["manufacturer"] == manufacturer) & (df_cars["year"].isna() != True)].groupby("year", as_index = False)["price"].mean()
    fig2, ax2 = plt.subplots(figsize=(12,8))
    sns.lineplot(x="year", y="price", data=df_trendprice, color = "red")
    ax2.set_title("Price Trend for %s"%(manufacturer),fontdict= {'fontsize': 20, 'fontweight':'bold'})
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Price")
    ax2.xaxis.label.set_color('black')
    ax2.yaxis.label.set_color('black')
    ax2.title.set_color('black')
    #ax2.tick_params(axis='x', colors='black')
    #ax2.tick_params(axis='y', colors='black')
    tab2.pyplot(fig2)


    def geospatial_info(manufacturer="ford", condition ="excellent", year =2020.0):
        df_cars_new = df_cars[(df_cars["manufacturer"] == manufacturer) & (df_cars["condition"] == condition) & (df_cars["year"] == year)][["lat","long"]].dropna()
        df_cars_new = df_cars_new.rename(columns = {"long":"lon"})
        return df_cars_new



    condition = tab3.selectbox("Select a condition:", list(df_cars[df_cars["condition"].isna() != True]["condition"].unique()))
    year = tab3.selectbox("Choose a year:", list(df_cars[df_cars["year"].isna() != True]["year"].unique()))
    car_location = geospatial_info(manufacturer, condition, year)
    zoom_int = tab3.slider("Choose a number", 0, 4, value = 3)
    tab3.map(car_location, zoom = zoom_int)

    def optimal_solution(manufacturer):
        df_cars_excellent = df_cars[(df_cars["manufacturer"] == manufacturer) & (df_cars["condition"] == "excellent")]
        df_optimal = df_cars_excellent.sort_values("odometer", ascending = True).head(10)
        df_optimal["year"] = df_optimal["year"].astype(int)
        df_optimal["odometer"] = df_optimal["odometer"].astype(int)
        return df_optimal[["model", "year","price", "odometer"]]

    optimal_df = optimal_solution(manufacturer)
    tab4.markdown("<h4 style='text-align: center; color: blue;'>Car models with the lowest odometers</h4>",
                unsafe_allow_html=True)
    tab4.dataframe(optimal_df)

    def variable_check():
        for index,row in df_cars.iterrows():
            all_variables = []
            if row["manufacturer"] == "ford":
                all_variables.append(row)
            return all_variables

    tab5.markdown("<h4 style='text-align: center; color: blue;'>Here are all variables in the used data list</h4>",
                unsafe_allow_html=True)
    df_all_variables = variable_check(df_cars)
    print(df_all_variables)
    tab5.dataframe(df_all_variables)

if __name__ == "__main__":
    run()

