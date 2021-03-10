import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt 
import seaborn as sns 
import lightgbm as lgb
import numpy as np
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer 


@st.cache(allow_output_mutation=True) 
def get_data():
    url = 'simple_data.csv'
    return pd.read_csv(url)

columnTransformer = ColumnTransformer([('encoder', OneHotEncoder(), [1])], remainder='passthrough')

#Build dataset
df = get_data()
df['position'] = df['position'].str.extract(r'(\w+),?')

X = df.drop(columns=['all_star'])

X = columnTransformer.fit_transform(X)
y = df.all_star

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99)

st.title('NBA All Star Predictor')
st.empty()
st.header('Select the stats for your player on the left.')
#st.dataframe(df.head())

#SIDEBAR
st.sidebar.title('PARAMETER SELECTION')
st.sidebar.header('Player Basics')
pos = st.sidebar.selectbox('Position:', ['PG', 'SG', 'SF', 'PF', 'C'])
age = st.sidebar.slider('Age:', min_value=18, max_value=45, step=1)

st.sidebar.header('Season Stats')
st.sidebar.subheader('Games & Minutes')
gp = st.sidebar.slider('Games Played:', min_value=0, max_value=82, step=1)
if gp == 0:
    gs = st.sidebar.slider('Games Started:', min_value=0, max_value=82, step=1)
else:
    gs = st.sidebar.slider('Games Started:', min_value=0, max_value=gp, step=1)

mpg = st.sidebar.slider('Minutes Played Per Game:', min_value=0.0, max_value=48.0, step=0.1)
minutes = round(mpg*gp)

st.sidebar.subheader('In Game Stats')
# fga = st.sidebar.number_input('Total Field Goals Attempted', value=0, step=1)
# fg = st.sidebar.number_input('Total Field Goals Made:', value=0, step=1, max_value=fga)

# tga = st.sidebar.number_input('Threes Attempted:', value=0, step=1)
# tm = st.sidebar.number_input('Threes Made:', value=0, step=1, max_value=tga)

# fta = st.sidebar.number_input('Free Throws Attempted:', value=0, step=1)
# ft = st.sidebar.number_input('Free Throws Made:', value=0, step=1, max_value=fta)

ppg = st.sidebar.slider('Points per Game:', min_value=0.0, max_value=40.0, step=0.1)
ppg = round(ppg * gp)
rpg = st.sidebar.slider('Rebounds per Game:', min_value=0.0, max_value=20.0, step=0.1)
rpg = round(rpg * gp)
apg = st.sidebar.slider('Assists per Game:', min_value=0.0, max_value=20.0, step=0.1)
apg = round(apg * gp)
spg = st.sidebar.slider('Steals per Game:', min_value=0.0, max_value=5.0, step=0.1)
spg = round(spg * gp)
bpg = st.sidebar.slider('Blocks per Game:', min_value=0.0, max_value=5.0, step=0.1)
bpg = round(bpg * gp)
tpg = st.sidebar.slider('Turnovers per Game:', min_value=0.0, max_value=10.0, step=0.1)
tpg = round(tpg * gp)
fpg = st.sidebar.slider('Fouls per Game:', min_value=0.0, max_value=6.0, step=0.1)
fpg = round(fpg * gp)
if gp == 0:
    tbl = st.sidebar.slider('Triple Doubles:', min_value=0, max_value=82, step=1)
else:
    tbl = st.sidebar.slider('Triple Doubles:', min_value=0, max_value=gp, step=1)


stats = [age, pos, gp, gs, minutes, rpg, apg, spg, bpg, tpg, fpg, ppg, tbl]

temp = pd.DataFrame(columns=['age', 'position', 'games_played', 'games_started', 'minutes',
       'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'fouls',
       'points', 'trip_dbl'])
temp.loc[0] = stats


temp[['age', 'games_played', 'games_started', 'minutes',
       'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'fouls',
       'points', 'trip_dbl']] = temp[['age', 'games_played', 'games_started', 'minutes',
       'rebounds', 'assists', 'steals', 'blocks', 'turnovers', 'fouls',
       'points', 'trip_dbl']].apply(pd.to_numeric)

temp = columnTransformer.transform(temp)

#Build Model
# mod_data = lgb.Dataset(X_train, y_train)
# model = lgb.train(params={'objective':'binary'}, train_set=mod_data)
model = LGBMClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

st.subheader("Model Training Accuracy")
st.text(accuracy_score(y_test, predictions))
st.code(classification_report(y_test, predictions))
st.code(model.feature_importances_)

st.title('Input Prediction')
prediction = model.predict(temp)
proba = model.predict_proba(temp)
if prediction == 1:
    st.header('Your player will be an All Star!')
    st.subheader(f'Probability: {proba[0][1] * 100}')
else:
    st.header('Your player will not be an All Star.')
    st.subheader(f'Probability: {proba[0][1] * 100}')