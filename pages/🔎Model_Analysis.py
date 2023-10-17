import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Depression Dashboard", page_icon="😥", layout="wide")

@st.cache_data
def get_data(filename):
    df = pd.read_pickle(filename)
    return df

feat_kn = get_data("data/features_kneighbor.pkl")
score_kn = get_data("data/score_kn.pkl")
feat_lgbm = get_data("data/features_lgbm.pkl")
score_lgbm = get_data("data/score_lgbm.pkl")
feat_log = get_data("data/features_log_reg.pkl")
score_log = get_data("data/score_log_reg.pkl")
feat_xgb = get_data("data/features_xgb.pkl")
score_xgb = get_data("data/score_xgb.pkl")

model = st.sidebar.selectbox(
    'Select model to analyze:',
    ('Logistic Regression Classifier', 'KNeighbor Classifier', 'XGBoost Classifier', 'LightGBM Classifier'),
    index=None,)

st.title("🤔💭❔ What is the Causes of Depression?")
st.markdown('''
            To gain insights into the causes of depression, we employ machine learning models. These models are 
            trained to recognize relationships between the features and the likelihood of experiencing depression. 
            By analyzing the models' outcomes, we can pinpoint the most influential features, which are the likely 
            culprits in causing depression. **Choose the model on the sidebar to get insight...**
            ''')

feat = None
if model == 'Logistic Regression Classifier':
    feat = feat_log
    accuracy = score_log['accuracy'][0]
    f1 = score_log['f1'][0]
elif model == 'KNeighbor Classifier':
    feat = feat_kn
    accuracy = score_kn['accuracy'][0]
    f1 = score_kn['f1'][0]
elif model == 'XGBoost Classifier':
    feat = feat_xgb
    accuracy = score_xgb['accuracy'][0]
    f1 = score_xgb['f1'][0]
elif model =='LightGBM Classifier':
    feat = feat_lgbm
    accuracy = score_lgbm['accuracy'][0]
    f1 = score_lgbm['f1'][0]
    
if model is not None :
    st.header(model)

    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Top 3 Causing Depression:")
        st.markdown(f'''
                    1. {feat.iloc[-1][0]}
                    2. {feat.iloc[-2][0]}
                    3. {feat.iloc[-3][0]}
                    ''')
    with right_column:
        a_column, b_column = st.columns(2)
        with a_column:
            st.subheader("Accuracy:")
            st.subheader("{:.2f}%".format(accuracy*100))
        with b_column:    
            st.subheader("F1 Score:")
            st.subheader("{:2f}".format(f1))    
    


if feat is not None:
    fig = px.bar(feat, x='Importance', y='Feature')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
# st.sidebar.markdown('''[Source](youtube.com) ''')