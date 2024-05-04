# Importing Libraries
import pandas as pd
import pymysql as sql
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo
import plotly.graph_objects as go


##import matplotlib.pyplot as plt
#import numpy as np

# Setting up page configuration
icon = Image.open("DATA/ICN.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By Jafar Hussain",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Sudesh*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":wave: :yellow[**Hello! Welcome to the dashboard**]")

# #To clone the Github Pulse repository use the following code
# Reference Syntax - Repo.clone_from("Clone Url", "Your working directory")
# Repo.clone_from("https://github.com/PhonePe/pulse.git", "Project_3_PhonepePulse/Phonepe_data/data")

# Creating connection with mysql workbench
mydb = sql.connect(host='127.0.0.1',
                    user='root',
                    password='Master5$',
                    database='phonepe_db_pulse'
                  )
mycursor = mydb.cursor()

def execute_query(query):
        mycursor.execute(query)
        result = mycursor.fetchall()
        return result

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","Questionarre","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", 
                                     "--hover-color": "#red"},
                        "nav-link-selected": {"background-color": "#green"}})

import time

# Function to simulate loading animation

def loading_animation():
    st.markdown("""
        <style>
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            .fade-out {
                animation: fadeOut 2s forwards;
            }
        </style>
    """, unsafe_allow_html=True)

    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        latest_iteration.text(f"Loading... {i+1}%")
        bar.progress(i + 1)
        time.sleep(0.05)
    latest_iteration.markdown('<div class="fade-out">Loading...<!div>',unsafe_allow_html=True)
    bar.empty()

# MENU 1 - HOME
if selected == "Home":
    loading_animation()
    st.image("phonepe1.jpg",width=700,use_column_width=False)
    st.markdown("# :green[Data Visualization and Exploration]")
    st.markdown("## :green[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="small")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :orange[Domain :] Fintech")
        st.markdown("### :orange[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :orange[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("DATA/home.png")
        

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    loading_animation()
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.markdown(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """
                )
        
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":

        col1, col2, col3 = st.columns([2,2,2],gap="small")


# Content for column 1 (State)
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"SELECT state, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM agg_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY Total DESC LIMIT 10")
            df_state = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
            fig_state = px.bar(df_state, x='State', y='Total_Amount', 
                            title='Top 10 States by Total Transaction Amount', 
                            color='Total_Amount', color_continuous_scale='Agsunset', 
                            labels={'Total_Amount': 'Total Transaction Amount'})
            st.plotly_chart(fig_state, use_container_width=True)

        # Content for column 2 (District)
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"SELECT district, SUM(Count) AS Total_Count, SUM(Amount) AS Total FROM map_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY district ORDER BY Total DESC LIMIT 10")
            df_district = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])
            fig_district = px.pie(df_district, values='Total_Amount', names='District', title='Top 10 Districts by Total Transaction Amount', color_discrete_sequence=px.colors.sequential.Agsunset, hover_data=['Transactions_Count'], labels={'Transactions_Count': 'Transactions Count'})
            fig_district.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_district, use_container_width=True)

        # Content for column 3 (Pincode)
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"SELECT pincode, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM top_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY pincode ORDER BY Total DESC LIMIT 10")
            df_pincode = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
            fig_pincode = px.pie(df_pincode, values='Total_Amount', names='Pincode', title='Top 10 Pincodes by Total Transaction Amount', color_discrete_sequence=px.colors.sequential.Agsunset, hover_data=['Transactions_Count'], labels={'Transactions_Count': 'Transactions Count'})
            fig_pincode.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pincode, use_container_width=True)
    # Top Charts - USERS
                
# Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    loading_animation()
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('DATA/Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('DATA/Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
            
            
# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('DATA/Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL USERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

#MENU if Option 4:Questionarre
if selected == "Questionarre":    
        loading_animation()    
        column1, column2 = st.columns([1, 1])
        questions = st.selectbox('Questions', [
                            'Click the question that you would like to query',
                            '1.How does the total transaction count vary across different states?',
                            '2.What are the top 10 districts with the highest transaction count, and how do they compare?',
                            '3.Is there any correlation between transaction count and pincode?',
                            '4.How does the transaction count vary by brand (e.g., PhonePe, Google Pay, Paytm)?',
                            '5.Are there any seasonal trends in transaction counts over different quarters of the year?',
                            '6.Which state has the highest average transaction count per quarter, and what might be the reasons behind it?',
                            '7.Can we identify any outliers or anomalies in transaction counts across different districts?',
                            '8.How does the distribution of transaction counts differ between urban and rural areas (based on pincode or district)?',
                            '9.Is there any association between transaction counts and specific brands within different quarters of the year?'
                            ])


        if questions == '1.How does the total transaction count vary across different states?':
                    transaction_trend_query = f"SELECT State, SUM(Count) AS total_transaction_count FROM map_trans GROUP BY State"
                    transaction_trend_data = execute_query(transaction_trend_query)
                    df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['State', 'Total_Transaction_count'])
                    fig_transaction_trend = px.bar(df_transaction_trend, x='State', y='Total_Transaction_count', 
                                                    title='Total Transaction Count by State', 
                                                    color='State', labels={'Total_Transaction_count': 'Total Transaction Count'})
                    st.plotly_chart(fig_transaction_trend, use_container_width=True)

        elif questions == '2.What are the top 10 districts with the highest transaction count, and how do they compare?':
                    transaction_trend_query = f"SELECT district, SUM(count) AS total_transaction_count FROM map_trans GROUP BY district ORDER BY total_transaction_count DESC LIMIT 10"
                    transaction_trend_data = execute_query(transaction_trend_query)
                    df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['District', 'Total_Transaction_Count'])
                    fig_transaction_trend = px.histogram(df_transaction_trend, x='District', y='Total_Transaction_Count', 
                                                    title='Top 10 Districts by Transaction Count', 
                                                    color='District', labels={'Total_Transaction_Count': 'Total Transaction Amount'})
                    st.plotly_chart(fig_transaction_trend, use_container_width=True)

        elif questions == '3.Is there any correlation between transaction count and pincode?':
                    transaction_trend_query = f"SELECT pincode, SUM(Transaction_count) AS total_transaction_count FROM top_trans GROUP BY pincode;"
                    transaction_trend_data = execute_query(transaction_trend_query)
                    df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['Pincode', 'Total_Transaction_Count'])
                    fig_transaction_trend = px.histogram(df_transaction_trend, x='Pincode', y='Total_Transaction_Count', 
                                                    title='Correlation between Transaction Count and Pincode:', 
                                                    color='Pincode', labels={'Total_Transaction_Count': 'Total Transaction Count'})
                    st.plotly_chart(fig_transaction_trend, use_container_width=True)

        elif questions == '4.How does the transaction count vary by brand (e.g., PhonePe, Google Pay, Paytm)?':
                    transaction_trend_query = f"SELECT brands, SUM(count) AS total_transaction_count FROM agg_user GROUP BY brands"
                    transaction_trend_data = execute_query(transaction_trend_query)
                    df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['Brand', 'Total_Transaction_Count'])
                    fig_transaction_trend = px.bar(df_transaction_trend, x='Brand', y='Total_Transaction_Count', 
                                                    title='Transaction Count by Brand:', 
                                                    color='Brand', labels={'Total_Transaction_Count': 'Total Transaction Count'})
                    st.plotly_chart(fig_transaction_trend, use_container_width=True)

        elif questions == '5.Are there any seasonal trends in transaction counts over different quarters of the year?':
                    transaction_trend_query = f"SELECT quarter, SUM(count) AS total_transaction_count FROM map_trans GROUP BY quarter"
                    transaction_trend_data = execute_query(transaction_trend_query)
                    df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['Quarter', 'Total_Transaction_count'])
                    fig_transaction_trend = px.bar(df_transaction_trend, x='Quarter', y='Total_Transaction_count', 
                                                    title='Seasonal Trends in Transaction Count', 
                                                    color='Quarter', labels={'Total_Transaction_count': 'Total Transaction Count'})
                    st.plotly_chart(fig_transaction_trend, use_container_width=True)

        elif questions == '6.Which state has the highest average transaction count per quarter, and what might be the reasons behind it?':
                    transaction_trend_query = f"SELECT state, AVG(Transaction_count) AS avg_transaction_count_per_quarter FROM phonepe_db_pulse.agg_trans GROUP BY state ORDER BY avg_transaction_count_per_quarter DESC LIMIT 1"
                    transaction_trend_data = execute_query(transaction_trend_query)
                    df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['State', 'Avg_Transaction_count_per_quarter'])
                    fig_transaction_trend = px.bar(df_transaction_trend, x='State', y='Avg_Transaction_count_per_quarter', 
                                                    title='State with Highest Average Transaction Count per Quarter', 
                                                    color='State', labels={'Avg_Transaction_count_per_quarter': 'Avg Transaction'})
                    st.plotly_chart(fig_transaction_trend, use_container_width=True)
                    st.write(df_transaction_trend)

        elif questions == '7.Can we identify any outliers or anomalies in transaction counts across different districts?':
                    transaction_trend_query = f"SELECT district, SUM(count) AS total_transaction_count FROM map_trans GROUP BY district HAVING total_transaction_count > (SELECT AVG(total_transaction_count) FROM (SELECT SUM(count) AS total_transaction_count FROM map_trans GROUP BY district) AS subquery);"
                    transaction_trend_data = execute_query(transaction_trend_query)
                    df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['District', 'Total_transaction_count'])
                    fig_transaction_trend = px.bar(df_transaction_trend, x='District', y='Total_transaction_count', 
                                                    title='Outliers or Anomalies in Transaction Counts by District', 
                                                    color='District', labels={'Total_transaction_count': 'Total Transaction Count'})
                    st.plotly_chart(fig_transaction_trend, use_container_width=True)

        elif questions == '8.How does the distribution of transaction counts differ between urban and rural areas (based on pincode or district)?':
                    transaction_trend_query = f"SELECT CASE WHEN district IN ('urban_district_1', 'urban_district_2') THEN 'Urban' ELSE 'Rural' END AS area_type, SUM(count) AS total_transaction_count FROM map_trans GROUP BY area_type"
                    transaction_trend_data = execute_query(transaction_trend_query)
                    df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['Area_type', 'Total_Transaction_count'])
                    fig_transaction_trend = px.bar(df_transaction_trend, x='Area_type', y='Total_Transaction_count', 
                                                    title='Transaction Count Distribution between Urban and Rural Areas:', 
                                                    color='Area_type', labels={'Total_Transaction_count': 'Total Transaction Count'})
                    st.plotly_chart(fig_transaction_trend, use_container_width=True)
                    st.write(df_transaction_trend)

        elif questions == '9.Is there any association between transaction counts and specific brands within different quarters of the year?':
                    transaction_trend_query = f"SELECT quarter, brands, SUM(count) AS total_transaction_count FROM agg_user GROUP BY quarter, brands"
                    transaction_trend_data = execute_query(transaction_trend_query)
                    df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['Quarter', 'Brands', 'Total_Transaction_count'])
                    fig_transaction_trend_3d = go.Figure(data=[     go.Scatter3d(
                                                                    x=df_transaction_trend['Quarter'],
                                                                    y=df_transaction_trend['Brands'],
                                                                    z=df_transaction_trend['Total_Transaction_count'],
                                                                    mode='lines+markers',
                                                                    marker=dict(size=6, color=df_transaction_trend['Quarter']),  # You can customize marker colors based on quarter
                                                                    line=dict(width=2, color=df_transaction_trend['Quarter'])  # You can customize line colors based on quarter
                                                                )])
                    fig_transaction_trend_3d.update_layout(
                                            title='Association between Transaction Counts and Brands within Quarters)',
                                            scene=dict(
                                                xaxis=dict(title='Quarter'),
                                                yaxis=dict(title='Brands'),
                                                zaxis=dict(title='Total Transaction Count'),
                                            ),
                                        )
                    st.plotly_chart(fig_transaction_trend_3d, use_container_width=True)
        # Content for column 1
        with column1:
            st.markdown("### :yellow[Transactions]")
            transaction_trend_query = f"SELECT year, quarter, SUM(count) AS Total_count, SUM(amount) AS Total_amount FROM map_trans GROUP BY year, quarter ORDER BY year, quarter"
            transaction_trend_data = execute_query(transaction_trend_query)
            df_transaction_trend = pd.DataFrame(transaction_trend_data, columns=['Year', 'Quarter', 'Total_count', 'Total_amount'])
            fig_transaction_trend = px.line(df_transaction_trend, x='Quarter', y='Total_amount', 
                                             title='Transaction Amount Trend Over Quarters', 
                                             color='Year', labels={'Total_amount': 'Total Transaction Amount'})
            st.plotly_chart(fig_transaction_trend, use_container_width=True)
            
            #transaction_spike_query = f"SELECT year, quarter, count, amount FROM map_trans WHERE (year = 2022 AND quarter = 2) OR (year = 2022 AND quarter = 3)"
            #transaction_spike_data = execute_query(transaction_spike_query)
            #df_transaction_spike = pd.DataFrame(transaction_spike_data, columns=['Year', 'Quarter', 'count', 'amount'])
            #st.write(df_transaction_spike)
            
            payment_method_query = "SELECT Transaction_type, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_Amount FROM agg_trans GROUP BY Transaction_type ORDER BY Total_Transactions DESC"
            payment_method_data = execute_query(payment_method_query)
            df_payment_method = pd.DataFrame(payment_method_data, columns=['Transaction_type', 'Total_Transactions', 'Total_Amount'])
            st.write(df_payment_method)

        # Content for column 2
        with column2:
            st.markdown("### :yellow[Geographical Analysis]")
            top_states_query = f"SELECT state, SUM(count) AS Total_count, SUM(amount) AS  Total_amount FROM map_trans GROUP BY state ORDER BY Total_amount DESC LIMIT 10"
            top_states_data = execute_query(top_states_query)
            df_top_states = pd.DataFrame(top_states_data, columns=['State', 'Total_count', 'Total_amount'])
            fig_top_states = px.bar(df_top_states, x='State', y='Total_amount', 
                                    title='Top 10 States by Total Transaction Amount', 
                                    color='Total_amount', color_continuous_scale='Agsunset', 
                                    labels={'Total_amount': 'Total Transaction Amount'})
            st.plotly_chart(fig_top_states, use_container_width=True)

        

# MENU 5 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.write("https://github.com/")
        st.write("**:violet[Image and content source]** ⬇️")
        st.write("https://www.prnewswire.com/in/news-releases/phonepe-launches-the-pulse-of-digital-payments-india-s-first-interactive-geospatial-website-888262738.html")
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("DATA/Pulseimg.jpg")