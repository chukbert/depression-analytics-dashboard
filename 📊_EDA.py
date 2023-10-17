import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Depression Dashboard", page_icon="😥", layout="wide")

@st.cache_data
def get_data():
    df = pd.read_pickle("cleaned_data.pkl")
    return df

df = get_data()

def plot_depression():
    depressed_counts = df['depressed'].value_counts().reset_index()
    depressed_counts.columns = ['depressed', 'count']
    fig_a = px.bar(depressed_counts, x='depressed', y='count', title='Population Depressed People in Rural Zone', text_auto=True)
    fig_b = px.pie(depressed_counts, values='count', names='depressed', title='Percentage of Depressed People in Rural Zone')
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_a, use_container_width=True)
    right_column.plotly_chart(fig_b, use_container_width=True)

def plot_1_cat(features):
    features.append('depressed')
    df_cat_counts = df.groupby(features).size().reset_index(name='count')
    fig_a = px.histogram(df_cat_counts, 
            x=features[0], 
            y="count", 
            color="depressed", 
            barmode='group', 
            title=f"Depression by {features[0]}", 
            text_auto=True)
    
    df_cat_counts_percent = df_cat_counts.groupby(features[0]).apply(lambda x: x.assign(count=x['count']/x['count'].sum()*100))
    fig_b = px.bar(df_cat_counts_percent, 
                        x=features[0], 
                        y="count", 
                        color="depressed", 
                        text=df_cat_counts_percent['count'].apply(lambda x: '{0:1.2f}%'.format(x)),
                        title=f"Percent Depression by {features[0]}")
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_a, use_container_width=True)
    right_column.plotly_chart(fig_b, use_container_width=True)

def plot_1_num(features):
    fig = px.histogram(df, 
                        x=features[0], 
                        color="depressed",
                        marginal="box",
                        title=f"Distribution Depression by {features[0]}")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def plot_1(features):
    if df[features[0]].dtype == 'category':
        plot_1_cat(features) 
    else:
        plot_1_num(features)

def plot_2_cat(features):
    features.append('depressed')
    df_count = df.groupby(features).size().reset_index(name='count')
    fig = px.icicle(df_count,
                    path=[px.Constant("all"), *features],
                    values='count')
    fig.update_traces(root_color='black')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def plot_2_num(features):
    fig_a = px.scatter(df,
                    x=features[0],
                    y=features[1],
                    color='depressed')
    features.append('depressed')
    df_count = df.groupby(features).size().reset_index(name='count')
    df_count = df_count[df_count['count']>0]
    fig_b = px.scatter_3d(df_count,
                        x=features[0],
                        y=features[1],
                        z='count',
                        color='depressed',
                        log_z=True)
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_a, use_container_width=True)
    right_column.plotly_chart(fig_b, use_container_width=True)

def plot_1_1(features):
    fig = px.box(df,
                x=features[0],
                y=features[1],
                color="depressed")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def plot_2(features):
    if df[features[0]].dtype == 'category':
        if df[features[1]].dtype == 'category':
            plot_2_cat(features)
        else:
            plot_1_1(features)
    else:
        if df[features[1]].dtype == 'category':
            plot_1_1(features) 
        else:
            plot_2_num(features)
    
# ---- SIDE BAR ----
show_features = df.columns.tolist()
show_features = [feat for feat in show_features if feat!='depressed']
first_feat = st.sidebar.selectbox(
    'Select the feature to analyze:',
    show_features,
    index=None,)

# ---- MAINPAGE ----
st.title("🥺😥😭 Depression Dashboard")
st.header("Introduction")
st.markdown('''
            Depression affects millions of individuals worldwide and is a crippling illness. It can make people feel unhappy, struggling to live normal lives, and, 
            at worst, suicide deaths. Despite lacking specialized training to manage mental health problems like depression, using the dataset from 
            [kaggle](https://www.kaggle.com/datasets/diegobabativa/depression) can give us new analysis about the illness. The data was consists as a study about the 
            life conditions of people who live in rurales zones.
            
            This dashboard provides an interactive tool for users to explore the data. The figures may take a moment to update when changed. Try to look at the features
            and get some insight about the data. Scroll down for the whole.''')

if first_feat is None:
    plot_depression()   
    st.sidebar.markdown('''[Source](https://github.com/chukbert/depression-analytics-dashboard) ''')
    
    st.stop() # This will halt the app from further execution.
else:
    show_features = [feat for feat in show_features if feat!=first_feat]    
    second_feat = st.sidebar.selectbox(
        'Add another feature to analyze:',
        show_features,
        index=None,)
    st.sidebar.markdown('''[Source](https://github.com/chukbert/depression-analytics-dashboard) ''')

    if second_feat is None:
        plot_1([first_feat])
        st.stop()
    else:
        features = [first_feat, second_feat]
        plot_2(features)
        plot_1([first_feat])
        plot_1([second_feat])
        st.stop()
        
    

