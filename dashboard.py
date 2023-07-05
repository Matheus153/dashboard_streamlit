import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache_data
def get_data_from_excel():

    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=2000
    )

    # Add 'hour' column to dataframe
    df['hour'] = pd.to_datetime(df['Time'], format="%H:%M:%S").dt.hour
    return df


df = get_data_from_excel()

# __SIDEBAR__
st.sidebar.header('Please filter here:')

city = st.sidebar.multiselect(
    "Select city:",
    options=df["City"].unique(),
    default=df["City"].unique(),
)

customer_type = st.sidebar.multiselect(
    "Select the customer type:",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


# __MainPage__
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# Top KPI's
total_sales = int(df_selection["Total"].sum())

average_rating = round(5 * df_selection["Rating"].mean()/10, 1)
star_rating = ":star:" * int(round(average_rating, 0))

average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown(''' ### Total Sales:''')
    total_sales = f'{total_sales:_.2f}'
    total_sales = total_sales.replace('.', ',').replace('_', '.')
    st.subheader(f"U$ {total_sales}")
with middle_column:
    st.markdown(''' ### Rating:''')
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.markdown(''' ### Average Sales per Transaction:''')
    average_sale_by_transaction = f'{average_sale_by_transaction:_.2f}'
    average_sale_by_transaction = average_sale_by_transaction.replace('.', ',')
    st.subheader(f"U$ {average_sale_by_transaction}")


sales_by_product_line = (
    df_selection.groupby(by=['Product line']).sum()[
        ['Total']].sort_values(by='Total')
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line<b>",
    color_discrete_sequence=["#0083b8"] * len(sales_by_product_line)
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
with left_column:
    st.plotly_chart(fig_hourly_sales)
with right_column:
    st.plotly_chart(fig_product_sales)

st.dataframe(df_selection)
