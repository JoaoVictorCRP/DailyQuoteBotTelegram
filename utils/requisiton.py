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
