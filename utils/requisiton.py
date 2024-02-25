async def get_random_quote(theme_arg=None) -> list:
    import requests
    from config import quotes_api_token
    
    if not theme_arg:
        theme_arg = 'inspirational' #Default theme

    url = f'https://api.api-ninjas.com/v1/quotes?category={theme_arg}'
    print(f'QUOTE THEME IS: {theme_arg}')
    try:
        response = requests.get(url, headers={'X-Api-Key': quotes_api_token})
        response.raise_for_status() #Raise exception for HTTP errors
        data = response.json()[0]
        if not data:
            raise Exception('Invalid theme.')
        quote = data['quote']
        author = data['author']
        return [quote, author]
    
    except requests.exceptions.RequestException as e:
        print(f'Error while making API request: {e}')

async def get_quote_themes() -> list:
    themes = [
        "- Age\n", "- Alone\n", "- Amazing\n", "- Anger\n", "- Architecture\n", "- Art\n", "- Attitude\n", "- Beauty\n", 
        "- Best\n", "- Birthday\n", "- Business\n", "- Car\n", "- Change\n", "- Communication\n", "- Computers\n", 
        "- Cool\n", "- Courage\n", "- Dad\n", "- Dating\n", "- Death\n", "- Design\n", "- Dreams\n", "- Education\n", 
        "- Environmental\n", "- Equality\n", "- Experience\n", "- Failure\n", "- Faith\n", "- Family\n", "- Famous\n", 
        "- Fear\n", "- Fitness\n", "- Food\n", "- Forgiveness\n", "- Freedom\n", "- Friendship\n", "- Funny\n", "- Future\n", 
        "- God\n", "- Good\n", "- Government\n", "- Graduation\n", "- Great\n", "- Happiness\n", "- Health\n", "- History\n", 
        "- Home\n", "- Hope\n", "- Humor\n", "- Imagination\n", "- Inspirational\n", "- Intelligence\n", "- Jealousy\n", 
        "- Knowledge\n", "- Leadership\n", "- Learning\n", "- Legal\n", "- Life\n", "- Love\n", "- Marriage\n", "- Medical\n", 
        "- Men\n", "- Mom\n", "- Money\n", "- Morning\n", "- Movies\n", "- Success\n"
    ]
    return themes
    
help_text = 'Welcome to Quoach BOT, your personal motivational quote companion!\n\
      \nHere are the available commands:\
      \n/start - Start your journey with Quoach BOT by selecting your timezone. This is essential for scheduling your daily motivational quote.\
      \n/set - Set the hour to receive your daily dose of inspiration. Choose the time that suits you best and let Quoach BOT send you uplifting messages every day.\
      \n/unset - If you wish to change the scheduled time or stop receiving daily quotes, use this command to unschedule your quote timer.\
      \n/quote - Instantly receive a motivational quote! You can also specify a theme, such as "/quote love" for quotes related to love. If no theme is provided, a random quote will be sent.\
        \n\nExample usage:\
        \n- "/start" - Begin your Quoach experience.\
        \n- "/set 18:30" - Schedule your daily quote for 6:30 PM.\
        \n- "/unset" - Stop receiving daily quotes.\
        \n- "/quote" - Get an immediate inspirational quote.\
        \n- "/quote success" - Receive a motivational quote about success.'