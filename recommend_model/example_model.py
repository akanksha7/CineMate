from model import MovieRecommender

def main():
    recommender = MovieRecommender()
    title = 'The Dark Knight'
    df = recommender.get_recommendation(title)
    print(df)
    titles = df['title'].values
    print(titles)

    genre_dict = {}
    for i in titles:
        genre_dict.update({i:recommender.get_genre(i)})
    print("dict:",genre_dict)
    # Example usage of get_genre
    movie_title = 'The Dark Knight'
    genre = recommender.get_genre(movie_title)
    print(f"The genre of '{movie_title}' is: {genre}")

    print(f"action movies {recommender.get_random_action_movies()}")
    print(f"comedy movies {recommender.get_random_comedy_movies()}")
    print(f"drama movies {recommender.get_random_drama_movies()}")
    print(f"romance movies {recommender.get_random_romance_movies()}")
    print(f"horror movies {recommender.get_random_horror_movies()}")


if __name__ == '__main__':
    main()


'''
create a dict {title: genre}
----------------------------------------------------------------------------------------
dropdown1: comedy     |   ChatBot:
dropdown2: action     |   Hi, I am a chatbot. I can help you with movie recommendations.
dropdown3: drama      |   Me: I am looking for a movie to watch.
dropdown4: horror     |   ChatBot: Based on your preferences, I recommend you to watch: 
dropdown5: romance    |   comedy[0], action[0], drama[0], horror[0], romance[0]:
                      |   Me: I want to want a comedy movie.
                      |   ChatBot: Based on your preferences, I recommend you to watch:
                      |   dict[comedy]
----------------------------------------------------------------------------------------


dropdown1: comedy (frontend) - > user puts favorite comedy (frontend) - > five recommendations (backend)
dropdown2: action (frontend) - > user puts favorite action (frontend) - > five recommendations (backend)
dropdown3: drama (frontend) - > user puts favorite drama (frontend) - > five recommendations (backend)
dropdown4: horror (frontend) - > user puts favorite horror (frontend) - > five recommendations (backend)
dropdown5: romance (frontend) - > user puts favorite romance (frontend) - > five recommendations (backend)

by the end - we will have 25 recommendations (in the backend)
{title : genre} - length 25
'''