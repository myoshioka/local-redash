import time
from typing import Any

import httpx
from local_redash.models.redash_client import (DataSourceDetail,
                                               DataSourceList, JobResult,
                                               JobResultStatus, Query,
                                               QueryDetail, QueryList,
                                               QueryResultData)
from timeout_decorator import timeout

QUERY_TIME_OUT = 10


class RedashClient:

    def __init__(self, redash_url: str, api_key: str) -> None:
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

    def update_query(self,
                     query_id: int,
                     query: str,
                     options: dict | None = None) -> QueryDetail:

        if options is None or not isinstance(options, dict):
            options = {}

        payload = {'query': query, 'options': options}
        result = self._post(f'api/queries/{query_id}', payload)
        return QueryDetail.parse_obj(result)

    def create_query(self,
                     data_source_id: str,
                     name: str,
                     query: str,
                     description: str = "",
                     options: dict | None = None) -> QueryDetail:

        if options is None or not isinstance(options, dict):
            options = {}

        payload = {
            "data_source_id": data_source_id,
            "name": name,
            "query": query,
            "description": description,
            "options": options
        }
        result = self._post('api/queries', payload)
        return QueryDetail.parse_obj(result)

    def get_query(self, id: int) -> QueryDetail:
        response = self._get(f'api/queries/{id}')
        return QueryDetail.parse_obj(response)

    def get_data_source(self, id: int) -> DataSourceDetail:
        response = self._get(f'api/data_sources/{id}')
        return DataSourceDetail.parse_obj(response)

    def get_data_source_list(self) -> DataSourceList:
        response = self._get('api/data_sources')
        return DataSourceList.parse_obj(response)

    def get_query_list(self) -> QueryList:
        result = self._get_paginate('api/queries')
        return QueryList.parse_obj(result)

    def query_result(self, query_id: int, params={}) -> QueryResultData:
        payload = {'max_age': 0, 'parameters': params}
        results_response = self._post(f'api/queries/{query_id}/results',
                                      payload)
        result_id = self._polling_job(results_response['job']['id'])

        if result_id is None:
            raise Exception('Query execution timed out.')

        response = self._get(
            f'api/queries/{query_id}/results/{result_id}.json')

        return QueryResultData.parse_obj(response['query_result']['data'])

    @timeout(QUERY_TIME_OUT)
    def _polling_job(self, job_id: str) -> int | None:
        job_status: int | None = None
        job_query_result_id: int | None = None

        while True:
            response = self._get(f'api/jobs/{job_id}')

            job_result = JobResult.parse_obj(response['job'])
            job_status = job_result.status
            if job_status == JobResultStatus.FINISHED:
                job_query_result_id = job_result.query_result_id
                break
            if job_status == JobResultStatus.FAILED:
                raise Exception('Query execution failed.')

            time.sleep(1)

        return job_query_result_id

    def _get_paginate(self, path: str, params={}) -> list:
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

    def _get(self, path: str, params=None) -> Any:
        response = httpx.get(f"{self.redash_url}/{path}",
                             headers=self.request_headers,
                             params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, payload=None) -> Any:
        response = httpx.post(f"{self.redash_url}/{path}",
                              headers=self.request_headers,
                              json=payload)
        response.raise_for_status()
        return response.json()
