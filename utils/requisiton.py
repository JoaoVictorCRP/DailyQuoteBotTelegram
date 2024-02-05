import requests

async def get_random_quote(theme_arg=None):
    if not theme_arg:
        theme_arg = 'famous-quotes|life|inspirational'

    url = f'https://api.quotable.io/quotes/random?tags={theme_arg}'

    print(f'QUOTE THEME IS: {theme_arg}')

    try:
        response = requests.get(url)
        response.raise_for_status() #Raise exception for HTTP errors
        data = response.json()[0]
        if not data:
            raise Exception('Invalid theme.')
        quote = data['content']
        author = data["author"]
        return [quote,author]
    
    except requests.exceptions.RequestException as e:
        print(f'Error while making API request: {e}')

async def get_quote_themes():
    url = 'https://api.quotable.io/tags'
    themes = []

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        for i in range(0,len(data)-2):
            tag_name = data[i]["name"]
            tag_size = data[i]['quoteCount']
            if tag_size>1: # Some of the tags in this API stores NO phrases at all... others just a single one. Let's filter this! 
                themes.append(f'\n- {tag_name}')
        
        themes.append(f'\n- Work') # There's a bug in the tag list that makes the 'Work' tag appears 2 times at the end of the list.
        return themes
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return []