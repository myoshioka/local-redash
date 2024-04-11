import json
import sys
import time
from ctypes import resize
from typing import Any

import httpx
from local_redash.exceptions import AuthenticationError
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
        self._authentication()

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

        try:
            payload = {
                "data_source_id": data_source_id,
                "name": name,
                "query": query,
                "description": description,
                "options": options
            }
            result = self._post('api/queries', payload)
            return QueryDetail.parse_obj(result)
        except httpx.HTTPStatusError as exc:
            # Without printing a traceback
            sys.tracebacklimit = -1
            raise Exception('Failed to create query.') from None

    def get_query(self, id: int) -> QueryDetail | None:
        try:
            response = self._get(f'api/queries/{id}')
            return QueryDetail.parse_obj(response)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            else:
                raise exc

    def get_data_source(self, id: int) -> DataSourceDetail:
        response = self._get(f'api/data_sources/{id}')
        return DataSourceDetail.parse_obj(response)

    def get_data_source_list(self) -> DataSourceList:
        response = self._get('api/data_sources')
        return DataSourceList.parse_obj(response)

    def get_query_list(self) -> QueryList:
        result = self._get_paginate('api/queries')
        return QueryList.parse_obj(result)

    def query_result(self, query_id: int, params={}) -> QueryResultData | None:
        try:
            payload = {'max_age': 0, 'parameters': params}
            results_response = self._post(f'api/queries/{query_id}/results',
                                          payload)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            else:
                raise exc

        result_id = self._polling_job(results_response['job']['id'])

        if result_id is None:
            raise Exception('Query execution timed out.')

        response = self._get(
            f'api/queries/{query_id}/results/{result_id}.json')

        return QueryResultData.parse_obj(response['query_result']['data'])

    def _authentication(self):
        # Request for authentication check. Because each API has a
        # different response code for authentication errors.
        self._get('api/users')

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
                # Without printing a traceback
                sys.tracebacklimit = -1
                print(job_result.error)
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
        response = None
        try:
            response = httpx.get(f"{self.redash_url}/{path}",
                                 headers=self.request_headers,
                                 params=params)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            if self._is_authentication_error(response):
                # Without printing a traceback
                sys.tracebacklimit = -1
                raise AuthenticationError() from None
            else:
                self._print_response_error(response)
                raise exc

    def _post(self, path: str, payload=None) -> Any:
        response = None
        try:
            response = httpx.post(f"{self.redash_url}/{path}",
                                  headers=self.request_headers,
                                  json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            if self._is_authentication_error(response):
                # Without printing a traceback
                sys.tracebacklimit = -1
                raise AuthenticationError() from None
            else:
                self._print_response_error(response)
                raise exc

    def _print_response_error(self, response: httpx.Response | None) -> None:
        print('Error: API request failed.')
        if response is not None:
            if self._is_json(response.content):
                print(f'Response body: {response.json()}')
            else:
                print(f'Response body: {response.text}')

    def _is_json(self, json_constant) -> bool:
        try:
            json.loads(json_constant)
        except ValueError as e:
            return False
        return True

    def _is_authentication_error(self,
                                 response: httpx.Response | None) -> bool:
        if response is not None and self._is_json(
                response.content) and 'message' in response.json().keys():
            if response.json(
            )['message'] == "Couldn't find resource. Please login and try again.":
                return True

        return False
