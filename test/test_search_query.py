import os
from dotenv import load_dotenv
from os.path import join, dirname
from redash_toolbelt import Redash
from local_redash import main

load_dotenv(join(dirname(__file__), '../local_redash/.env'))


def test_search_query():

    redash_url = os.environ['REDASH_URL']
    api_key = os.environ['API_KEY']
    client = Redash(redash_url, api_key)
    result = main.search_query(client, 'query_test')

    assert result is not None
    print(result)
