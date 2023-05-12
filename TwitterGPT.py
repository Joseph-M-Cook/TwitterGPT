import openai
import requests
from requests_oauthlib import OAuth1
import json
import gradio as gr

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
openai.api_key = ""

    
def get_search_query(query):
    messages = [{"role": "system",
                    "content": "You are an AI assistant that helps to convert text into a relevant Twitter search API query."
                            "You output only 1 query for the latest message and nothing else."

                            "Info:"
                            'Operator: keyword	Type: Standalone Example: pepsi OR cola OR "coca cola"'

                            'Examples:'
                            'Which NHL games are on tonight?: ("nhl news" OR "nhl tonight" OR "hockey games" OR "hockey tonight") -is:retweet lang:en -has:links -is:reply'
                            'What is some recent soccer news?: ("soccer news" OR "football news" OR "soccer updates" OR "football updates") -is:retweet -is:reply lang:en -has:links -is:reply'
                            'What stocks are people buying?: ("stocks" OR "stock market" OR "investing" OR "investments") ("buying" OR "purchasing" OR "investing") -is:retweet -is:reply lang:en -has:links'}]
    
    messages.append({"role": "user", "content": "Based on my previous messages, "
                                                "what is the most relevant Twitter search query for the text below?\n\n"
                                                "Text: " + query + "\n\n"
                                                                    "Query:"})
    



    search_query = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
    )['choices'][0]['message']['content']

    print(search_query.strip("\""))
    return search_query.strip("\"")
    

def twitter_search(query):
    search_url = "https://api.twitter.com/2/tweets/search/recent"

    query_params = {
        'query': query,
        'tweet.fields': 'author_id',
        'user.fields': 'username',
        'expansions': 'author_id',
        'max_results': 50
    }

    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    def connect_to_endpoint(url, params):
        response = requests.get(url, auth=auth, params=params)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def print_tweets(json_response):
        i = 0
        all_tweets = ""
        if 'data' in json_response:
            for tweet in json_response['data']:
                user = next(user for user in json_response['includes']['users'] if user['id'] == tweet['author_id'])
                tweet_url = f"https://twitter.com/{user['username']}/status/{tweet['id']}"
                tweet_text = f"{user['username']}: {tweet['text']}\n"
                #print(tweet_text)
                #print(f"Tweet URL: {tweet_url}\n")
                all_tweets += tweet_text
        return all_tweets

    json_response = connect_to_endpoint(search_url, query_params)
    all_tweets = print_tweets(json_response)
    
    print(all_tweets)

    return all_tweets

    
def AIResponse(query, tweets):
        messages = [{"role": "system",
                     "content": "You are a bot that answers questions to the best of your ability based on search results from twitter. Do not apologize or mention what you are not capable of, make your response very brief "
                     "do not start your response with anything like 'Based on the search results'"}]
    
        messages.append({"role": "user", "content": "Answer the question to the best of your ability based on the search results and the query"
                                
                                                    "results: " + tweets + "\n\n"
                                                                        "Query:" + query})

        search_query = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0,
        )['choices'][0]['message']['content']

        return search_query #.strip("\"")

def main(query_text):
    generated_query = get_search_query(query_text)
    ans = twitter_search(generated_query)
    return AIResponse(query_text, ans)


iface = gr.Interface(
    fn=main,
    inputs=[gr.inputs.Textbox(lines=3, label="Question:")],
    outputs=[gr.outputs.Textbox(label="Output:")],
    title="TwitterGPT",
    description="Enter your question and get a consensus from a curated twitter search summarized by AI.",
)


iface.launch()
