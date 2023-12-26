import fire
from tinydb import TinyDB, Query
import search_api

db = TinyDB('db.json')
User = Query()


def search(name='luke'):
  characters = search_api.search(name)
  if characters is not None:
    check_db(characters)
  else:
    print(f'Cannot find the character "{name}"')

def parse_char(char):
  char_name = search_api.parse_name(char)
  planet= search_api.parse_planet(char)
  film_list = search_api.parse_films(char)
  titles = search_api.format_titles(film_list)
  description = search_api.person_description(char_name, planet, titles)
  db.insert({'name':char_name, 'planet':planet, 'titles':titles})
  return description



# def parse_char(char):
#   char_name = search_api.parse_name(char)
#   planet= search_api.parse_planet(char)
#   film_list = search_api.parse_films(char)
#   titles = search_api.format_titles(film_list)
#   description = search_api.person_description(char_name, planet, titles)
#   return description

# def parse_char_list(chars):
#   for char in chars:
#     char_name = search_api.parse_name(char)
#     planet= search_api.parse_planet(char)
#     film_list = search_api.parse_films(char)
#     titles = search_api.format_titles(film_list)
#     description = search_api.person_description(char_name, planet, titles)
#     print(description)


def check_db(chars):
  for char in chars:
    char_name = search_api.parse_name(char)
    results = db.search(User.name == char_name)
    if not results:
      description = parse_char(char)
    else:
      name = results[0]['name']
      planet = results[0]['planet']
      titles = results[0]['titles']
      description = search_api.person_description(name, planet, titles)
    print(description)



if __name__ == '__main__':
  fire.Fire(search)