import os
import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import warnings

warnings.simplefilter('ignore')


class MovieRecommender:
    def __init__(self, data_path='./data/'):
        self.data_path = data_path
        self.loaded = False  # Flag to indicate if data is loaded
        self.links_small = None
        self.md = None
        self.gen_md = None
        self.smd = None
        self.indices = None
        self.titles = None
        self.cosine_sim = None
        self.tfidf_matrix = None

    def load_data(self):
        if not self.loaded:
            links_small_path = os.path.join(self.data_path, 'links_small.csv')
            md_path = os.path.join(self.data_path, 'movies_metadata.csv')
            self.links_small = pd.read_csv(links_small_path)
            self.md = pd.read_csv(md_path)
            self.loaded = True

    def preprocess_data(self):
        self.md['genres'] = (self.md['genres'].fillna('[]')
                             .apply(literal_eval)
                             .apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else []))

        self.md['year'] = pd.to_datetime(self.md['release_date'], errors='coerce').apply(
            lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

    def calculate_weighted_rating(self, qualified, m, C):
        def weighted_rating(x):
            v = x['vote_count']
            R = x['vote_average']
            return (v / (v + m) * R) + (m / (m + v) * C)

        qualified['wr'] = qualified.apply(weighted_rating, axis=1)
        return qualified

    def build_chart(self, genre, percentile=0.85):
        df = self.gen_md[self.gen_md['genre'] == genre]
        vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
        vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
        C = vote_averages.mean()
        m = vote_counts.quantile(percentile)

        qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) &
                       (df['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity']]
        qualified['vote_count'] = qualified['vote_count'].astype('int')
        qualified['vote_average'] = qualified['vote_average'].astype('int')

        qualified = self.calculate_weighted_rating(qualified, m, C)
        qualified = qualified.sort_values('wr', ascending=False).head(250)

        return qualified

    def preprocess_and_build_chart(self):
        self.preprocess_data()

        s = self.md.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
        s.name = 'genre'
        self.gen_md = self.md.drop('genres', axis=1).join(s)
        self.gen_md = self.gen_md.reset_index(drop=True)  # Reset index


    def build_tfidf_matrix(self):
        self.smd['tagline'] = self.smd['tagline'].fillna('')
        self.smd['description'] = self.smd['overview'] + self.smd['tagline']
        self.smd['description'] = self.smd['description'].fillna('')

        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.0001, stop_words='english')
        self.tfidf_matrix = tf.fit_transform(self.smd['description'])

    def get_recommendations(self, title):
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:31]
        movie_indices = [i[0] for i in sim_scores]
        return self.titles.iloc[movie_indices]

    def get_recommendation(self, title):
        self.load_data()
        self.preprocess_and_build_chart()

        self.links_small = self.links_small[self.links_small['tmdbId'].notnull()]['tmdbId'].astype('int')
        self.md['id'] = self.md['id'].apply(convert_int)
        self.md = self.md.drop([19730, 29503, 35587])
        self.md['id'] = self.md['id'].astype('int')
        self.smd = self.md[self.md['id'].isin(self.links_small)]
        self.smd = self.smd.reset_index(drop=True)
        self.titles = self.smd['title']
        self.indices = pd.Series(self.smd.index, index=self.smd['title'])

        self.build_tfidf_matrix()

        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

        series = self.get_recommendations(title)
        df = series.to_frame().reset_index()
        df.columns = ['index', 'title']
        df = df.drop('index', axis=1)
        return df

    def get_genre(self, movie):
        if not self.loaded:
            self.load_data()
            self.preprocess_and_build_chart()
        return self.gen_md[self.gen_md['title'] == movie]['genre'].values[0]

    def get_random_action_movies(self, num_movies=30):
        if not self.loaded:
            self.load_data()
            self.preprocess_and_build_chart()

        action_movies = self.gen_md[self.gen_md['genre'] == 'Action']
        random_action_movies = action_movies.sample(n=num_movies)

        # Create dictionary with {title: genre}
        random_action_movies_dict = dict(zip(random_action_movies['title'], random_action_movies['genre']))

        return random_action_movies_dict

    def get_random_comedy_movies(self, num_movies=30):
        if not self.loaded:
            self.load_data()
            self.preprocess_and_build_chart()

        comedy_movies = self.gen_md[self.gen_md['genre'] == 'Comedy']
        random_comedy_movies = comedy_movies.sample(n=num_movies)

        # Create dictionary with {title: genre}
        random_comedy_movies_dict = dict(zip(random_comedy_movies['title'], random_comedy_movies['genre']))

        return random_comedy_movies_dict

    def get_random_drama_movies(self, num_movies=30):
        if not self.loaded:
            self.load_data()
            self.preprocess_and_build_chart()

        drama_movies = self.gen_md[self.gen_md['genre'] == 'Drama']
        random_drama_movies = drama_movies.sample(n=num_movies)

        # Create dictionary with {title: genre}
        random_drama_movies_dict = dict(zip(random_drama_movies['title'], random_drama_movies['genre']))

        return random_drama_movies_dict

    def get_random_romance_movies(self, num_movies=30):
        if not self.loaded:
            self.load_data()
            self.preprocess_and_build_chart()

        romance_movies = self.gen_md[self.gen_md['genre'] == 'Romance']
        romance_movies_movies = romance_movies.sample(n=num_movies)

        # Create dictionary with {title: genre}
        random_romance_movies_dict = dict(zip(romance_movies_movies['title'], romance_movies_movies['genre']))

        return random_romance_movies_dict

    def get_random_horror_movies(self, num_movies=30):
        if not self.loaded:
            self.load_data()
            self.preprocess_and_build_chart()

        horror_movies = self.gen_md[self.gen_md['genre'] == 'Horror']
        random_horror_movies = horror_movies.sample(n=num_movies)

        # Create dictionary with {title: genre}
        random_horror_movies_dict = dict(zip(random_horror_movies['title'], random_horror_movies['genre']))

        return random_horror_movies_dict


def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan

