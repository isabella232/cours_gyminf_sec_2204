import csv  
from datetime import datetime, timedelta
import time, hashlib

films = [
    "The Shawshank Redemption (1994)",
    "The Godfather (1972)",
    "The Godfather: Part II (1974)",
    "The Dark Knight (2008)",
    "12 Angry Men (1957)",
    "Schindler's List (1993)",
    "The Lord of the Rings: The Return of the King (2003)",
    "Pulp Fiction (1994)",
    "The Good, the Bad and the Ugly (1966)",
    "The Lord of the Rings: The Fellowship of the Ring (2001)",
    "Fight Club (1999)",
    "Forrest Gump (1994)",
    "Inception (2010)",
    "The Lord of the Rings: The Two Towers (2002)",
    "Star Wars: Episode V - The Empire Strikes Back (1980)",
    "The Matrix (1999)",
    "Goodfellas (1990)",
    "One Flew Over the Cuckoo's Nest (1975)",
    "Seven Samurai (1954)",
    "Seven (1995)"
]

people_first = [
    "Andrea",
    "Antonio",
    "Arthur",
    "Christophe",
    "Corentin",
    "Enea",
    "Ericka",
    "Exupéry",
    "Frédéric",
    "Georges",
    "Julia",
    "Julien",
    "Laurence",
    "Manuel",
    "Marie",
    "Mathieu",
    "Mélissa",
    "Michelle",
    "Mohammed",
    "Mouhssine",
    "Murièle",
    "Nicolas",
    "Olivier",
    "Olivier Philippe",
    "Patrick",
    "Quentin",
    "Raphaël",
    "Sélim",
    "Simon",
    "Sylvain",
    "Thierry",
    "Yannick"
]

people_family = [
    "Franco",
    "Terra",
    "Dromard",
    "Dumas",
    "Rordorf",
    "Milio",
    "Olsen",
    "Badillo",
    "Montmollin",
    "Andoine",
    "Mutti",
    "Lavanchy",
    "Berclaz",
    "Fragnière",
    "Di Marco",
    "Tristan Kocher",
    "Nicolier",
    "Stella",
    "Bouriche",
    "Rami",
    "Jacquier",
    "Kunz",
    "La Spada",
    "Pravaz",
    "Rossi",
    "Zanoun",
    "Mérot",
    "Kairouani",
    "Verdan",
    "Rouge",
    "Gerez",
    "Mettreaux"
]

import random, math
from collections import Counter

imdb = []
netflix = []
films_imdb = 3
films_netflix = 4

# Returns unique films
def get_films(films: int, nbr: int):
    film_list = []
    for i in range(nbr):
        while True:
            film = films - math.floor(math.sqrt(random.randrange(films ** 2))) - 1
            if not film in film_list:
                film_list = film_list + [film]
                break
    return film_list

def uniq_choice(l) -> bool:
    choice_sorted = list(map(lambda e: sorted(e), l))
    choice_unique = []
    for user in choice_sorted:
        if not user in choice_unique:
            choice_unique.append(user)
            
    return len(choice_sorted) == len(choice_unique)

# the total number of netflix films is imdb + netflix
def create_list(films: int, people: int, imdb: int, netflix: int):
    imdb_list = []
    netflix_list = []
    
    for i in range(people):
        while True:
            film_list = get_films(films, imdb + netflix)
            imdb_list.append(film_list[:imdb])
            netflix_list.append(film_list)
            if not ( uniq_choice(imdb_list) and uniq_choice(netflix_list) ):
                imdb_list.pop()
                netflix_list.pop()
            else:
                break
                
    return [imdb_list, netflix_list]

def sort_list(l):
    movies_counted = Counter(sum(l, []))
    movies_sorted = sorted(movies_counted.items(), key =
             lambda kv:(kv[0], kv[1]))
    return list(map(lambda x: x[0], movies_sorted))

def get_name(i: int) -> str:
    return people_first[i // len(people_first)] + " " + people_family[i % len(people_first)]
   
def get_dates(nbr: int):
    date_to = time.mktime(datetime.today().timetuple())
    date_from = date_to - 3.141e7
    return list(map(lambda x: datetime.fromtimestamp(
                        random.randrange(date_from, date_to)).strftime("%Y-%m-%d"), 
                    range(nbr)))
    
def get_eval(movies):
    return list(map(lambda m: random.randrange(2) + math.floor(4 - m / len(films) * 4), movies))

def fill_lists(im_list, nf_list):
    im_clear = []
    nf_anon = []
    list_diff_len = len(nf_list[0]) - len(im_list[0])
    
    for i in range(len(im_list)):
        name = get_name(i)
        name_hash = hashlib.sha256(name.encode('utf-8')).hexdigest()[:8]
        movies = list(map(lambda i: films[i], nf_list[i]))
        movies_hash = list(map(lambda m: hashlib.sha256(m.encode('utf-8')).hexdigest()[:8], movies))
        dates = get_dates(len(movies))
        evals = get_eval(nf_list[i])
        for m in range(len(movies)):
            if m >= list_diff_len:
                im_clear.append([name, movies[m], dates[m], evals[m]])
            nf_anon.append([name_hash, movies_hash[m], dates[m], evals[m]])
            
    random.shuffle(im_clear)
    random.shuffle(nf_anon)
    return [im_clear, nf_anon]

def save_file(name: str, l):
    header = ['name', 'movie', 'date', 'rating']

    with open(name, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for data in l:
            writer.writerow(data)
            
    print("saved", name)

random.seed(123)
import os.path

if not os.path.isfile("imdb_small.csv"):
    [il, nl] = create_list(len(films), 5, 5, 1)
    [il_full, nl_full] = fill_lists(il, nl)
    save_file("imdb_small.csv", il_full)
    save_file("netflix_small.csv", nl_full)

if not os.path.isfile("imdb_big.csv"):
    print("Creating big db - this takes some time")
    [il, nl] = create_list(len(films), 32*32, 10, 2)
    [il_full, nl_full] = fill_lists(il, nl)
    save_file("imdb_big.csv", il_full)
    save_file("netflix_big.csv", nl_full)
