import streamlit as st
from streamlit.logger import get_logger
import keras
import json
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import random
from recommend_model.model import MovieRecommender
import pprint


LOGGER = get_logger(__name__)

lemmatizer = WordNetLemmatizer()

# load words object
words = pickle.load( open('words.pkl', 'rb'))

# load classes object
classes = pickle.load( open('classes.pkl', 'rb'))
model = keras.models.load_model('chatbot_model.h5')

@st.cache_data()
def render_left_ui():
    return {
        'fav_comedy': None,
        'fav_action': None,
        'fav_drama': None,
        'fav_romance': None,
        'fav_horror': None}

@st.cache_resource
def init_recommender():
    st.session_state.recommender = MovieRecommender()

def run():
    st.set_page_config(
        page_title="Movie Bot",
        page_icon="👋",
    )
    st.title("Movie Bot")

    with open("intents.json") as file:
        intents = json.load(file)

    # Create recommender model
    # TODO this doesn't seem right, but probably good enough
    while not hasattr(st.session_state, 'recommender'):
        init_recommender()

    left_ui = render_left_ui()
    comedies = list(st.session_state.recommender.get_random_comedy_movies(250).keys())
    actions = list(st.session_state.recommender.get_random_action_movies(250).keys())
    dramas = list(st.session_state.recommender.get_random_drama_movies(250).keys())
    horrors = list(st.session_state.recommender.get_random_horror_movies(250).keys())
    romances = list(st.session_state.recommender.get_random_romance_movies(250).keys())
    with st.sidebar:
        st.title("Choose Your Favorite Movies!")
        left_ui['fav_comedy'] = st.selectbox("Favorite Comedy", comedies)
        left_ui['fav_action'] = st.selectbox("Favorite Action", actions)
        left_ui['fav_drama'] = st.selectbox("Favorite Drama", dramas)
        left_ui['fav_romance'] = st.selectbox("Favorite Romance", romances)
        left_ui['fav_horror'] = st.selectbox("Favorite Horror", horrors)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message['movie_list']:
                st.code(message['movie_list'])

    # React to user input
    if prompt:= st.chat_input("Hey! Here are some movie recommendations for you. What are you in the mood for?"):
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, 'movie_list': ''})
        ints = predict_class(prompt)
        result, movie_list = get_response(ints, intents, left_ui)
        with st.chat_message("assistant"):
            st.markdown(result)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant",
                                          "content": result,
                                          "movie_list": movie_list})

        # If we have a recommended list, add the movie list in a code block
        if movie_list:
            st.code(movie_list)

@st.cache_resource
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

@st.cache_resource
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

@st.cache_resource
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

@st.cache_resource
def get_response(intents_list, intents_json, left_ui):
    try:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        result = ''
        movies = ''
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                if i['tag'] in ['comedy', 'action', 'drama', 'horror', 'romance']:
                    fav_comedy = str(left_ui['fav_comedy'])
                    fav_action = str(left_ui['fav_action'])
                    fav_drama = str(left_ui['fav_drama'])
                    fav_romance = str(left_ui['fav_romance'])
                    fav_horror = str(left_ui['fav_horror'])

                    comedy_recommendations = st.session_state.recommender.get_recommendation(fav_comedy)
                    action_recommendations = st.session_state.recommender.get_recommendation(fav_action)
                    drama_recommendations = st.session_state.recommender.get_recommendation(fav_drama)
                    romance_recommendations = st.session_state.recommender.get_recommendation(fav_romance)
                    horror_recommendations = st.session_state.recommender.get_recommendation(fav_horror)
                    recommendations = {'comedy': comedy_recommendations,
                                       'action': action_recommendations,
                                       'drama': drama_recommendations,
                                       'romance': romance_recommendations,
                                       'horror': horror_recommendations}

                    movies = pprint.pformat(recommendations[i["tag"]])
                break
    except:
        result = "I'm sorry, I don't understand"
        movies = ''
    return result, movies

if __name__ == "__main__":
    run()