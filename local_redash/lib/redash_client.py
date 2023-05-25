import json
import time

import httpx
import requests
from local_redash.models.redash_client import DataSourceList, Query, QueryList
from redash_toolbelt import Redash


class RedashClient:

    def __init__(self, redash: Redash, redash_url: str, api_key: str) -> None:
        self._client = redash
        if redash_url.endswith('/'):
            redash_url = redash_url[:-1]

        self.redash_url = redash_url
        self.request_headers = {"Authorization": f"Key {api_key}"}

    def search_query(self, search_name: str) -> Query | None:
        all_queries = self.get_query_list()
        result = None
        for query in all_queries:
            if query.name == search_name:
                result = query
                break

        return result

    def update_query(self, query_id: int, query: str, options: dict = None):

        if options is None or not isinstance(options, dict):
            options = {}

        payload = {'query': query, 'options': options}
        result = self._post(f'api/queries/{query_id}', payload)

        # result = self._client.update_query(query_id, payload)
        return result

    def create_query(self,
                     data_source_id: int,
                     name: str,
                     query: str,
                     description: str = "",
                     options: dict = None):

        if options is None or not isinstance(options, dict):
            options = {}

        payload = {
            "data_source_id": data_source_id,
            "name": name,
            "query": query,
            "description": description,
            "options": options
        }
        result = self._client.create_query(payload)
        return result

    def get_data_source_list(self) -> DataSourceList:
        response = self._get('api/data_sources')
        return DataSourceList.parse_obj(response)

    def get_query_list(self) -> QueryList:
        query_list = []
        result = self._get_paginate('api/queries')
        return QueryList.parse_obj(result)

    def query_result(self, query_id: str, params={}):
        session = self._client.session

        payload = dict(max_age=0, parameters=params)
        response = session.post('{}/api/queries/{}/results'.format(
            self._client.redash_url, query_id),
                                data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception('Refresh failed.')

        result_id = self.__polling_job(session, response.json()['job'])

        if result_id:
            response = session.get('{}/api/queries/{}/results/{}.json'.format(
                self._client.redash_url, query_id, result_id))
            if response.status_code != 200:
                raise Exception('Failed getting results.')
        else:
            raise Exception('Query execution failed.')

        return response.json()['query_result']['data']['rows']

    def __polling_job(self, session, job):
        # TODO: add timeout
        while job['status'] not in (3, 4):
            response = session.get('{}/api/jobs/{}'.format(
                self._client.redash_url, job['id']))
            job = response.json()['job']
            time.sleep(1)

        if job['status'] == 3:
            return job['query_result_id']

        return None

    def _get_paginate(self, path: str, params={}):
        if not 'page' in params:
            params = {**params, **{'page': 1}}

        response = self._get(path, params)
        results = response['results']

        page = response['page']
        page_size = response['page_size']

        if page * page_size >= response['count']:
            return results
        else:
            return [
                *results,
                *self._get_paginate(path, {
                    **params,
                    **{
                        'page': page + 1
                    }
                }),
            ]

    def _get(self, path: str, params=None):
        response = httpx.get(f"{self.redash_url}/{path}",
                             headers=self.request_headers,
                             params=params)
        if httpx.codes.is_success(response.status_code):
            return response.json()
        else:
            response.raise_for_status()

    def _post(self, path: str, payload=None):
        response = httpx.post(f"{self.redash_url}/{path}",
                              headers=self.request_headers,
                              json=payload)
        if httpx.codes.is_success(response.status_code):
            return response.json()
        else:
            response.raise_for_status()
