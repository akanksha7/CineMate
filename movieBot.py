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
from typing import Optional, List

import os

nltk_data_dir = "./resources/nltk_data_dir"
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.clear()
nltk.data.path.append(nltk_data_dir)
nltk.download("wordnet", download_dir=nltk_data_dir)
nltk.download("stopwords", download_dir=nltk_data_dir)
nltk.download('punkt', download_dir=nltk_data_dir)

LOGGER = get_logger(__name__)

lemmatizer = WordNetLemmatizer()


# load words object
words = pickle.load( open('words.pkl', 'rb'))

# load classes object
classes = pickle.load( open('classes.pkl', 'rb'))
model = keras.models.load_model('chatbot_model.h5')

@st.cache_resource
def render_left_ui():
    return {
        'comedy': None,
        'action': None,
        'drama': None,
        'romance': None,
        'horror': None}

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
        left_ui['comedy'] = st.selectbox("Favorite Comedy", comedies)
        left_ui['action'] = st.selectbox("Favorite Action", actions)
        left_ui['drama'] = st.selectbox("Favorite Drama", dramas)
        left_ui['romance'] = st.selectbox("Favorite Romance", romances)
        left_ui['horror'] = st.selectbox("Favorite Horror", horrors)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message['movie_list']:
                st.text(message['movie_list'])

    # React to user input
    if prompt:= st.chat_input("Hey! Here are some movie recommendations for you. What are you in the mood for?"):
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, 'movie_list': ''})
        ints = predict_class(prompt)
        result, movie_list = get_response(ints, intents, left_ui)

        # Add assistant response to chat history
        msg = {"role": "assistant", "content": result, "movie_list": movie_list}
        st.session_state.messages.append(msg)

        # Add assistant response to current chat
        with st.chat_message("assistant"):
            st.markdown(result)
            # If we have a recommended movie list, add the list to the chat
            if movie_list:
                st.text(movie_list)


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

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
                if i['tag'] in left_ui.keys():
                    fav_movie = left_ui[i['tag']]
                    recommendations = st.session_state.recommender.get_recommendation(fav_movie)[:10]
                    movies = pprint.pformat(recommendations)
                break
    except:
        result = "I'm sorry, I don't understand"
        movies = ''
    return result, movies

class GlobalsHelper:
    """Helper to retrieve globals.

    Helpful for global caching of certain variables that can be expensive to load.
    (e.g. tokenization)

    """

    _stopwords: Optional[List[str]] = None
    _nltk_data_dir: Optional[str] = None

    def __init__(self) -> None:
        """Initialize NLTK stopwords and punkt."""
        import nltk

        self._nltk_data_dir = os.environ.get(
            "NLTK_DATA",
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "_static/nltk_cache",
            ),
        )

if __name__ == "__main__":
    run()
