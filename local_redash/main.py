import os
import requests
import time
import json
from redash_toolbelt import Redash
from dotenv import load_dotenv
from os.path import join, dirname
from tabulate import tabulate
import click

os.environ['NO_PROXY'] = '127.0.0.1,localhost'


def create_query(api_key,
                 redash_url: str,
                 data_source_id: int,
                 name: str,
                 query: str,
                 description: str = "",
                 options: dict = None):

    session = requests.Session()
    session.headers.update({'Authorization': 'Key {}'.format(api_key)})

    if options is None or not isinstance(options, dict):
        options = {}

    payload = {
        "data_source_id": data_source_id,
        "name": name,
        "query": query,
        "description": description,
        "options": options
    }

    res = session.post('{}/api/queries'.format(redash_url),
                       data=json.dumps(payload))

    print(res.status_code)
    return res.json()


def update_query(api_key,
                 redash_url: str,
                 query_id: int,
                 query: str,
                 options: dict = None):

    session = requests.Session()
    session.headers.update({'Authorization': 'Key {}'.format(api_key)})

    if options is None or not isinstance(options, dict):
        options = {}

    payload = {"query": query, "options": options}

    res = session.post('{}/api/queries/{}'.format(redash_url, query_id),
                       data=json.dumps(payload))

    print(res.status_code)
    return res.json()


def search_query(client, search_name):

    all_queries = client.paginate(client.queries)
    result = None
    for query in all_queries:
        if query['name'] == search_name:
            result = query
            break

    return result


def get_data_source_list(client):
    return client.get_data_sources()


def poll_job(s, redash_url, job):
    # TODO: add timeout
    while job['status'] not in (3, 4):
        response = s.get('{}/api/jobs/{}'.format(redash_url, job['id']))
        job = response.json()['job']
        time.sleep(1)

    if job['status'] == 3:
        return job['query_result_id']

    return None


def get_fresh_query_result(redash_url, query_id, api_key, params={}):
    s = requests.Session()
    s.headers.update({'Authorization': 'Key {}'.format(api_key)})

    payload = dict(max_age=0, parameters=params)

    response = s.post('{}/api/queries/{}/results'.format(redash_url, query_id),
                      data=json.dumps(payload))

    if response.status_code != 200:
        raise Exception('Refresh failed.')

    result_id = poll_job(s, redash_url, response.json()['job'])

    if result_id:
        response = s.get('{}/api/queries/{}/results/{}.json'.format(
            redash_url, query_id, result_id))
        if response.status_code != 200:
            raise Exception('Failed getting results.')
    else:
        raise Exception('Query execution failed.')

    return response.json()['query_result']['data']['rows']


def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path).split('.')[0]


def get_query(query_file_path: str) -> str:
    with open(query_file_path, 'r', encoding='utf-8') as f:
        query = f.read()
    return query


@click.command()
@click.option('--query-file', required=True, type=str, help='')
@click.option('--data-source-id', required=True, type=int, help='')
def main(query_file: str, data_source_id: int):

    load_dotenv(join(dirname(__file__), '.env'))

    redash_url = os.environ['REDASH_URL']
    api_key = os.environ['API_KEY']

    client = Redash(redash_url, api_key)

    data_source_list = get_data_source_list(client)
    print(
        tabulate(data_source_list,
                 headers="keys",
                 tablefmt="psql",
                 stralign='center'))

    # query_path = os.path.dirname(__file__) + '/../queries/query_test.sql'
    query_path = query_file
    query_str = get_query(query_path)
    print(query_str)

    file_name = get_file_name(query_path)
    print(file_name)

    target_query = search_query(client, file_name)
    if target_query is None:
        created_query = create_query(api_key, redash_url, data_source_id,
                                     file_name, query_str)
        result = get_fresh_query_result(redash_url, created_query['id'],
                                        api_key)
    else:
        updated_query = update_query(api_key, redash_url, target_query['id'],
                                     query_str)
        result = get_fresh_query_result(redash_url, target_query['id'],
                                        api_key)
    print(tabulate(result, headers="keys", tablefmt="psql", stralign='center'))


if __name__ == '__main__':
    main()
