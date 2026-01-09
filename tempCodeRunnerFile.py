ges = [
        {
            "role": "system",
            "content": "You are a user friendly sarcastic bot, Always answer in a user friendly way but it has to includee sarcasm"
        }
    ]
query = ""
while(query != 'quit'):
    query = input('Query: ')
    if query == 'quit':
        print(messages)
    else:
        messages.append(
            {
                "role": "user",
                "content": query
            }
        )
        response = get_response(messages=messages)
        print(response)
    