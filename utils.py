import os
import requests
import redis
import json
import time


r = redis.Redis(host=os.getenv('REDIS_SERVER'), port=6379, db=1, charset="utf-8", decode_responses=True)


def get_searches_from_redis(query):
    return r.get(f'search "{query}"')


def push_searches_to_redis(query, results):
    r.set(f'search "{query}"', json.dumps(results), ex=60*60*24)


def get_search_results(author, query_string):
    """
    Util Function for
        1) fetching results from Google
        2) Creating or updating the Query model
        3) Bulk creating or updating the QueryLink Model
    :param query_string:
    :return: list of top 5 URLs for the given query_string
    """
    r.zadd(f'recent "{author}"', {query_string: time.time()})

    results = get_searches_from_redis(query_string)
    if results:
        return json.loads(results)
    results = list()

    # Google Search API configurations
    url = 'https://www.googleapis.com/customsearch/v1'
    query_params = dict()
    query_params['q'] = query_string
    query_params['key'] = os.getenv('GOOGLE_API_KEY')
    query_params['cx'] = os.getenv('GOOGLE_SEARCH_ENGINE')
    # Results from Google Search API
    response = requests.get(url, params=query_params)
    if response and response.status_code == 200:
        data = response.json()
        if 'items' in data:
            items = data['items'][:5]           # Top 5 links selected
            for index, item in enumerate(items):
                link = item['link']
                results.append(link)
    push_searches_to_redis(query_string, results)
    return results


def get_recent_queries(author, string=None):
    if not string:
        return r.zrevrange(f'recent "{author}"', 0, 4)
    all_queries = r.zrevrange(f'recent "{author}"', 0, -1)
    recent_queries = list()
    for query in all_queries:
        if string in query:
            recent_queries.append(query)
        if len(recent_queries) == 5:
            break
    if not recent_queries:
        recent_queries.append('No recent queries found')
    return recent_queries