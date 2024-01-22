import requests

async def get_random_quote():
    url = 'https://api.quotable.io/quotes/random?tags=famous-quotes|life'

    try:
        response = requests.get(url)
        response.raise_for_status() #Raise exception for HTTP errors

        data = response.json()[0]
        quote = data['content']
        author = data["author"]
        return [quote,author]
    
    except requests.exceptions.RequestException as e:
        print(f'Error while making API request: {e}')