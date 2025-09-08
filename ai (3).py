from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import difflib
import pyttsx3 
import speech_recognition as sr
import datetime
import webbrowser

movies_data = pd.read_csv('movies.csv')

selected_features = ['genres',
                     'keywords',
                     'tagline', 
                     'cast',
                     'director']

def speak(audio):
    text_to_speech = pyttsx3.init()
    voices = text_to_speech.getProperty('voices')
    text_to_speech.setProperty('voice', voices[1].id)  
    text_to_speech.say(audio)
    text_to_speech.runAndWait()

def wishMe():
    
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        
        speak("Good Morning!")
        
    elif hour >= 12 and hour < 18:
        
        speak("Good Afternoon!") 
        
    else:
        
        speak("Good Evening!")
    speak("I am your Movie Assistant")
    speak("I Was Created By a group of students to help suggest movies to users based on their preferences , How can i help you today ?")

def takeCommand():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        
        print("Recognizing...") 
        query = r.recognize_google(audio,
                                   language = 'en-in')
        
        print(f"User said: {query}\n")
        
    except Exception as e:
        
        print("Unable to Recognize your voice.") 
        return "None"
    
    return query

def get_movie_recommendations(movie_name, movies_data, selected_features):
    
    for feature in selected_features:
        
        movies_data[feature] = movies_data[feature].fillna('')
        
    combined_Features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' +movies_data['cast'] + ' ' +movies_data['director']
    vectorizer = TfidfVectorizer()
    feature_vector = vectorizer.fit_transform(combined_Features)
    similarity = cosine_similarity(feature_vector)
    list_of_titles = movies_data['title'].tolist()
    Find_Close_Match = difflib.get_close_matches(movie_name,
                                                 list_of_titles)
    
    if not Find_Close_Match:
        
        return ["No match found for the given movie name."]
    
    close_match = Find_Close_Match[0]
    movie_index = movies_data[movies_data.title == close_match].index[0]
    similarity_score = list(enumerate(similarity[movie_index]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], 
                                   reverse=True)
    recommended_movies = [movies_data.iloc[i[0]]['title'] 
                          for i in sorted_similar_movies[1:6]]
    
    speak("Here is some similar movie you might like")
    speak(recommended_movies)
    return recommended_movies

def suggest_movies_based_on_mood(mood, movies_data):
    
    mood_genre = {
        "happy": "Comedy",
        "sad": "Drama",
        "excited": "Action",
        "scared": "Horror",
        "romantic": "Romance",
    }
    
    genre = mood_genre.get(mood.lower())
    if genre:
        
        filtered_movies = movies_data[movies_data['genres'].fillna('').str.contains(genre, 
                                                                                    case=False)]
        if not filtered_movies.empty:
            
            speak('Here is some movies that matches your mood')
            speak(filtered_movies['title'].tolist()[:5])
            return filtered_movies['title'].tolist()[:5]
        else:
            
            return ["No movies found for the specified mood."]
        
    return ["Mood not recognized."]

def Get_Movie_Information(movie_name, movies_data):
    
    try:
        
        movie_index = movies_data[movies_data['title'].str.lower() == movie_name.lower()].index[0]
        movie_info = movies_data.iloc[movie_index]
        speak("Here's some information about the movie:")
        speak(movie_info['title'])
        speak(f"Release Date: {movie_info['release_date']}")
        speak(f'Director : {movie_info["director"]}')
        speak(f"Genre: {movie_info['genres']}")
        speak(f"Overview: {movie_info['overview']}")
        
        while True:
            
            speak("Do you need any additional information about the movie?")
            Answer = takeCommand()
            if Answer == 'yes':
                
                speak("Here is the movie's wikipedia page ")
                webbrowser.open(f"https://en.wikipedia.org/wiki/{movie_name}")
                break
            
            elif Answer == 'no':
                
                break
            else:
                
                speak('Can you say that again')
        return movie_info
    
    except IndexError:
        
        speak("I couldn't find any information about that movie.")
        return None   