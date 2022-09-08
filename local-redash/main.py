import os
import requests
import time
import json
from redash_toolbelt import Redash


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


def poll_job(s, redash_url, job):
    # TODO: add timeout
    while job['status'] not in (3, 4):
        response = s.get('{}/api/jobs/{}'.format(redash_url, job['id']))
        job = response.json()['job']
        time.sleep(1)

    if job['status'] == 3:
        return job['query_result_id']

    return None


def get_fresh_query_result(redash_url, query_id, api_key, params):
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


if __name__ == '__main__':
    params = {'some_parameter': 1}
    query_id = 26
    redash_url = os.environ['REDASH_URL']
    api_key = os.environ['API_KEY']

    client = Redash(redash_url, api_key)
    queries = client.queries()
    print(json.dumps(queries))

    # data_source_id = 2
    # name = 'query-test'
    # query = 'select * from users where id = 7327;'
    # result = create_query(api_key, redash_url, data_source_id, name, query)
    # result = get_fresh_query_result(redash_url, result['id'], api_key, params)

    # print(json.dumps(result))
