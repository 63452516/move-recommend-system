import streamlit as t
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url,timeout=5)
    data = data.json()
    
    try:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    except KeyError:
        full_path = None
    
    return full_path

movies= pickle.load(open("movies_list.pkl", 'rb'))
similarity= pickle.load(open("similarity.pkl", 'rb'))
movies_list= movies['title'].values

t.header("Movies Recommendation System")

selected_movie= t.selectbox("Select a movie:", movies_list)

import streamlit.components.v1 as components

def recommand(movie):
    index=movies[movies['title']==movie].index[0]
    dist= sorted(list(enumerate(similarity[index])), reverse=True , key = lambda vec:vec[1])
    recommend_movies= []
    recommend_poster= []
    for i in dist[1:6]:
        movie_id =movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
     
    return recommend_movies, recommend_poster

if t.button("Recommend"):
   movie_name, movie_poster = recommand(selected_movie)
   col1,col2,col3,col4,col5 = t.columns(5)
   with col1:
        t.text(movie_name[0])
        t.image(movie_poster[0])
   with col2:
        t.text(movie_name[1])
        t.image(movie_poster[1])
   with col3:
        t.text(movie_name[2])
        t.image(movie_poster[2])
   with col4:
        t.text(movie_name[3])
        t.image(movie_poster[3])
   with col5:
        t.text(movie_name[4])
        t.image(movie_poster[4])     