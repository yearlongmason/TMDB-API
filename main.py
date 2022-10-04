import requests
import sys
import os

def movie_info():
    """
    This function should get the id from a movie search api and then use the id to use in a different api link that can get more data on the movie such as title, genres, overview, release date, vote average, vote count, runtime in minutes, budget, and revenue 
    """

    movie = input("Enter the name of a movie: ")
    print("\n")
    get_id_url = "https://api.themoviedb.org/3/search/movie?api_key=33a038fe556ff18c114a019113807e0f&language=en-US&query="+movie+"&page=1&include_adult=false"
    api_get_id = requests.get(get_id_url)
    json_get_id = api_get_id.json()#Gets the id from the TMDB api

    if 'errors' in json_get_id: #Checks for errors. Primarily entering nothing. It'll usually say that a query needs to be provided
        print(json_get_id)

    elif json_get_id['total_results'] > 0: #If there are results that come back this should give the data for the first result
        movie_id = json_get_id['results'][0]['id']
       
        movie_details_url = "http://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=33a038fe556ff18c114a019113807e0f&language=en-US"
        api_movie_details = requests.get(movie_details_url)
        json_movie_data = api_movie_details.json() #Puts the movie id into a different api to get movie data
        
        cast_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/credits?api_key=33a038fe556ff18c114a019113807e0f&language=en-US"
        api_get_cast = requests.get(cast_url)
        json_cast = api_get_cast.json() #Uses movie id to use a different api for the cast of the movie

        title = json_movie_data['title']
        overview = json_movie_data['overview']
        release_date = json_movie_data['release_date']
        rating = json_movie_data['vote_average']
        amount_of_votes = json_movie_data['vote_count']
        runtime = json_movie_data['runtime']
        budget = json_movie_data['budget']
        revenue = json_movie_data['revenue']
        genres = ""
        cast = ""
        writer = ""
        director = ""
        for i in range(len(json_movie_data['genres'])): #Gets genres and puts them into a string
            if i == (len(json_movie_data['genres'])-1):
                genres = genres + json_movie_data['genres'][i]['name'] + " "
            else:
                genres = genres + json_movie_data['genres'][i]['name'] + ", "
        for i in range(3): #Gets top 3 cast members and their character and puts them into a string
            if i == 2:
                cast = cast + json_cast['cast'][i]['name'] + " (" + json_cast['cast'][i]['character'] + ") "
            else:
                cast = cast + json_cast['cast'][i]['name'] + " (" + json_cast['cast'][i]['character'] + "), "
        for i in json_cast['crew']: #Searches for the writer
            if i['department'] == "Writing":
                writer = i['name']
                break
            if i == len(json_cast['crew']) - 1:
                writer = "Unknown"
        for i in json_cast['crew']: #Searches for the director
            if i['department'] == "Directing":
                director = i['name']
                break
            if i == len(json_cast['crew']) - 1:
                director = "Unknown"

        print("Title: " + title)
        print("Director: " + director)
        print("Writer: " + writer)
        print("Cast: " + cast)
        print("Genres: " + genres)
        print("Overview: " + overview)
        print("Runtime: " + str(runtime))
        print("Released: " + release_date)
        print("Rating: " + str(rating)+"/10 based on " + str(amount_of_votes) + " ratings")
        print("Budget:  $" + str(budget))
        print("Revenue: $" + str(revenue))
        print("Movie ID: " + str(movie_id))

    else: #Should only happen when no movies are found
        print("Movie not found. Check your spelling (It's also possible that movie is not in the database)")

def person_info():
    """
    This function should get info from an api based on a person's name that the user enters. Should return the Name, known for department, date and location of birth, date of death,  a short bio, movies they're known for
    """
    person = input("Enter a name: ")

    search_person_url = "https://api.themoviedb.org/3/search/person?api_key=33a038fe556ff18c114a019113807e0f&query=" + person + "&language=en-US&page=1&include_adult=false"
    api_search_person = requests.get(search_person_url)
    json_search_person = api_search_person.json() #Should return data on a person that is searched including a person's id (which is needed for half of the data that is not in this api), the name, known for department, and moveis they're known for

    if 'errors' in json_search_person:
        print(json_search_person)

    elif len(json_search_person['results']) > 0:
        name = json_search_person['results'][0]['name']# Should get data from the search person api
        person_id = json_search_person['results'][0]['id']
        department = json_search_person['results'][0]['known_for_department']
        known_for = ""
        for i in range(len(json_search_person['results'][0]['known_for'])): # Puts together the titles of what the person is known for. The try/except is in case one of the things they are known for is a show, there is no 'title', it's listed as 'name'
            if i != len(json_search_person['results'][0]['known_for']) - 1:
                try:
                    known_for = known_for + json_search_person['results'][0]['known_for'][i]['title'] + ", "
                except KeyError:
                    known_for = known_for + json_search_person['results'][0]['known_for'][i]['name'] + ", "
            else:
                try:
                    known_for = known_for + json_search_person['results'][0]['known_for'][i]['title']
                except KeyError:
                    known_for = known_for + json_search_person['results'][0]['known_for'][i]['name']

        person_details_url = "https://api.themoviedb.org/3/person/" + str(person_id) + "?api_key=33a038fe556ff18c114a019113807e0f&language=en-US"
        api_person_details = requests.get(person_details_url)
        json_person_details = api_person_details.json() #Should return the other half of data that requires the person id including the  date and location of birth, date of death, and the short bio

        bio = json_person_details['biography'] # Gets the rest of the data from the person details api which uses the person id which was gotten from the search person api
        birthday = json_person_details['birthday']
        birth_location = json_person_details['place_of_birth']
        deathday = json_person_details['deathday']
        if deathday == "null":
            deathday = None

        print("\nName: " + name) 
        print("Department: " + department)
        print("Born on " + birthday + " in " + birth_location)
        if deathday != None:
            print("Died on: " + deathday)
        print("Known for: " + known_for)
        print("Bio: " + bio)
        print("ID: " + str(person_id))

    else:
        print("Person not found. Check your spelling (It's also possible that person is not in the database)")

def end_program():
    """
    This function should do nothing except end the program
    """
    sys.exit()

menu_dict = {'1': movie_info,
             '2': person_info,
             '3': end_program}
menu_text = """
What would you like to do:
1. Get info on a movie
2. Get info on a person
3. Quit program
Please enter a number (1-3)
"""

while True:
    user_choice = input(menu_text)
    if user_choice in menu_dict and menu_dict[user_choice]:
        os.system('clear')
        menu_dict[user_choice]()
    else:
        print('Not a valid choice')