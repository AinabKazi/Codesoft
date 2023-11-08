import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import requests


st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon=":movie_camera:",
    layout="wide",
    initial_sidebar_state="collapsed",
)
@st.cache(suppress_st_warning=True)
def set_custom_style():
    st.markdown(
    """
    <style>
    body {
        background-color: black !important;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
    )


movies = pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')

movies = movies.merge(credits)

movies =movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)
#print(movies.duplicated().sum)
#print(movies.iloc[0].genres)

def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L


def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job'] =='Director':
             L.append(i['name'])
             break
    return L

movies['genres'] =movies['genres'].apply(convert)
movies['keywords'] =movies['keywords'].apply(convert)
movies['cast'] =movies['cast'].apply(convert3)
movies['crew'] =movies['crew'].apply(fetch_director)

movies['overview']=movies['overview'].apply(lambda  x:x.split())

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])


movies['tags']= movies['overview']+movies['genres']+movies['cast']+movies['crew']

newdf= movies[['movie_id','title','tags']]

newdf['tags'] =newdf['tags'].apply(lambda x:" ".join(x))
newdf['tags'] =newdf['tags'].apply(lambda x:x.lower())
cv=CountVectorizer(max_features=5000,stop_words='english')
vectors= cv.fit_transform(newdf['tags']).toarray()

ps= PorterStemmer()
def stem(text):
    y=[];
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

newdf["tags"]=newdf['tags'].apply(stem)

similarty= cosine_similarity(vectors)

def recommend(movie):
    movieIndex= newdf[newdf['title'] == movie].index[0]
    distances=similarty[movieIndex]
    movieList=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    for i in movieList:
        print(newdf.iloc[i[0]].title)

def recommender(movie):
    recommendedMovies = []
    recommendedMoviesPosters = []
    movieIndex = newdf[newdf['title'] == movie].index[0]
    distances = similarty[movieIndex]

    movieList = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in movieList:
        movieID = movies.iloc[i[0]].movie_id
        recommendedMovie = newdf.iloc[i[0]].title
        poster = fetchposter(movieID)
        if poster:
            recommendedMovies.append(recommendedMovie)
            recommendedMoviesPosters.append(poster)

    return recommendedMovies, recommendedMoviesPosters

def fetchposter(movieID):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3758d25981c51d1e42e96b57e9b02e82&language=en-US'.format(movieID))
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        return full_path
    else:
        return None


st.title('Movie Recommendation System')
SelectedMovieName = st.selectbox('What would you like to watch?', newdf['title'].values)

if st.button('Find Similar Movies'):
    columns = st.columns(5)
    names, posters = recommender(SelectedMovieName)

    if len(names) >= 5 and len(posters) >= 5:
        with columns[0]:
            st.text(names[0])
            st.image(posters[0], width=200)
        with columns[1]:
            st.text(names[1])
            st.image(posters[1], width=200)
        with columns[2]:
            st.text(names[2])
            st.image(posters[2], width=200)
        with columns[3]:
            st.text(names[3])
            st.image(posters[3], width=200)
        with columns[4]:
            st.text(names[4])
            st.image(posters[4], width=200)
    else:
        st.warning("Not enough similar movies found.")