

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('startup_cleaned.csv')

st.set_page_config(layout="wide",page_title="Startup Dashboard")
st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select Type Of Analysis',['Overall','Investor'])
def load_investorDetails(investor):
    investor_df = df[df['investors'].str.contains(investor)]

    st.title(investor)
    st.subheader('Recent Investments')

    st.dataframe(df[df['investors'].str.contains(investor)][['startup','date','vertical','city','round','amount']])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investments')
        big_series = investor_df.groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        fig, ax = plt.subplots()

        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    with col2:
        st.subheader('Sector-Wise Investments')
        data=investor_df.groupby('vertical')['amount'].sum()
        fig, ax = plt.subplots()
        ax.pie( data.values,labels=data.index,autopct='%1.1f%%')
        st.pyplot(fig)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Stage-Wise Investments')
        data = investor_df.groupby('round')['amount'].sum()
        fig, ax = plt.subplots()
        ax.pie(data.values, labels=data.index, autopct='%1.1f%%')
        st.pyplot(fig)
        if investor_df['date'].notnull().sum() > 1:
            st.subheader('YoY Investments')
            data = investor_df.groupby('year')['amount'].sum()
            fig, ax = plt.subplots()
            ax.plot(data.index, data.values)
            # Add axis labels
            ax.set_xlabel('Year')  # X-axis represents the year
            ax.set_ylabel('Amount')
            st.pyplot(fig)
    with col2:
        st.subheader('City-Wise Investments')
        data = investor_df.groupby('city')['amount'].sum()
        fig, ax = plt.subplots()
        ax.pie(data.values, labels=data.index, autopct='%1.1f%%')
        st.pyplot(fig)

if option=='Overall':

    total=round(df['amount'].sum())
    avg=round(df.groupby('startup')['amount'].sum().mean())
    maxx=round(df.groupby('startup')['amount'].sum().max())
    count=len(set(((df['startup'].str.split(',').explode()))))
    year = st.sidebar.selectbox(
        'Select Year',
        (pd.Series(df['year'].unique()).dropna().astype(int).sort_values(ascending=True).values)
    )
    # btn=st.sidebar.button('Show Overall Analysis')
    st.title('Overall  Analysis')
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total)+' Cr')
    with col2:
        st.metric('Average',str(avg)+' Cr')
    with col3:
        st.metric('Max',str(maxx)+' Cr')
    with col4:
        st.metric('Funded Startups',count)
    col1,col2=st.columns(2)
    with col1:
        st.subheader('YoY Funding Analysis')
        # df['myear'] = df['month'].astype(str) + '-' + df['year'].astype(str)
        # y_axis=df.groupby(['year', 'month'])['amount'].sum()
        temp_df = df.groupby('year')['amount'].sum().reset_index()
        fig, ax = plt.subplots()
        ax.plot(temp_df['year'], temp_df['amount'])
        # Add axis labels
        ax.set_xlabel('Year')  # X-axis represents the year
        ax.set_ylabel('Amount')
        st.pyplot(fig)
    with col2:
        st.subheader(f'MoM Funding Analysis ({year}-{(year+1)})')
        if year:
            temp_df = df[df['year'] == year]
            temp_df = temp_df.groupby('month')['amount'].sum().reset_index()
            fig, ax = plt.subplots()
            ax.plot(temp_df['month'], temp_df['amount'])
            # Add axis labels
            ax.set_xlabel('Month')  # X-axis represents the Month
            ax.set_ylabel('Amount')
            st.pyplot(fig)

# if option=='Startup':
#     st.sidebar.selectbox('Select A Startup', df['startup'].unique())
#     st.title('Startup Analysis')
if option=='Investor':
    df['investors']=df['investors'].str.replace('& Others','Others')
    investors_list=sorted(set((df['investors'].str.split(',').sum())))
    investors_list=investors_list[1::1]
    investor=st.sidebar.selectbox('Select A Investor', investors_list)
    investor_df = df[df['investors'].str.contains(investor)]
    if df['investors'].str.contains(investor).sum()>1 and investor_df['amount'].sum()>0 :
        load_investorDetails(investor)
    else:
        st.title(investor)
        st.subheader('Recent Investments')
        st.dataframe(df[df['investors'].str.contains(investor)][
                         ['startup', 'date', 'vertical', 'city', 'round', 'amount']].head())
        st.subheader('Due To Less Investments, No Analysis Can Be Performed! ')

