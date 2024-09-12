import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide' , page_title = "Startup analysis")
df = pd.read_csv("startup_cleaned.csv")
df['date'] = pd.to_datetime(df['date'] , errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
def load_overall_analysis():
    st.title('Overall analysis')
    #total invested amount
    total = round(df['amount'].sum())
    #max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    #total funded startups
    num_startups = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'CR')
    with col2:
        st.metric('Max', str(max_funding) + 'CR')
    with col3:
        st.metric('Avg' , str(avg_funding) + 'CR')
    with col4:
        st.metric('Funded Startups' , num_startups)
    st.header('MoM graph')
    selected_option = st.selectbox('Select Type' , ['Total' , 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '_' + temp_df['year'].astype('str')

    fig4, ax4 = plt.subplots()
    ax4.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig4)

def load_investor_detail(investor):
    st.title(investor)
    #load the recent 5 investment of the investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date' , 'vertical' ,'city' , 'round' , 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)
    col1 , col2 = st.columns(2)
    with col1:
       #biggest investment
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending = False).head()
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(big_series.index , big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().head()
        st.subheader('Sector invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series , labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
    round_series = df[df['investors'].str.contains('investor')].groupby('round')['amount'].sum().head()
    st.subheader('Round')
    fig2, ax2 = plt.subplots()
    ax2.pie(round_series, labels=round_series.index, autopct="%0.01f%%")
    st.pyplot(fig2)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YOY investment')
    fig3, ax3 = plt.subplots()
    ax3.plot(year_series.index, year_series.values)
    st.pyplot(fig3)



st.sidebar.title('startup funding analysis')
option = st.sidebar.selectbox('select one' , ['overall analysis' , 'Startup' , 'Investor'])
if option == 'overall analysis':
        load_overall_analysis()
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup' , sorted(df["startup"].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select investor' , sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_detail(selected_investor)