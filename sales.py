from cv2 import dft
from numpy import average
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Sales Dashboard", 
    page_icon=":bar_chart:",
    layout="wide"
)

@st.cache    
def getDataFromExcel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine='openpyxl',
        sheet_name="Sales",
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )

#hour column to dataframe
    df["hour"]=pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
df = getDataFromExcel()

print(df)

#SIDEBAR
st.sidebar.header("Filters: ")

city = st.sidebar.multiselect(
    "Select the city:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select Customer type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection =  df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

#MAIN PAGE
st.title(":bar_chart:  Sales dashboard")
st.markdown("##")

#TOP KPI's
total_sales  = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating  = ":star:" * int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)

left_column, middle_column, right_column =st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US ${total_sales:,}")
    with middle_column:
        st.subheader("Average Rating:")
        st.subheader(f"{average_rating}{star_rating}")
        with right_column:
            st.subheader("Average sales per transaction:")
            st.subheader(f"US ${average_sale_by_transaction}")
            st.markdown("---")

#BAR CHARTS
#SALES BY PRODUCT LINE 
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

barChart_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by product line</b>",
    color_discrete_sequence=["#0083b8"]*len(sales_by_product_line),
    template="plotly_white",
)

barChart_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#SALES BY HOUR
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
barChart_salesByHour = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083b8"]*len(sales_by_hour),
    template="plotly_white",
)

barChart_salesByHour.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)

left_column, right_column = st.column = st.columns(2)
left_column.plotly_chart(barChart_salesByHour, use_container_width=True)
right_column.plotly_chart(barChart_product_sales, use_container_width=True)

hideDefaultStyle = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header  {visibility: hidden;}
</style>
"""
st.markdown(hideDefaultStyle, unsafe_allow_html=True)
