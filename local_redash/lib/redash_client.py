from redash_toolbelt import Redash
import requests
import json
import time
from local_redash.models.redash_client import Query


class RedashClient:

    def __init__(self, redash: Redash) -> None:
        self._client = redash

    def search_query(self, search_name: str) -> Query | None:
        all_queries = self._client.paginate(self._client.queries)
        result = None
        for query in all_queries:
            if query['name'] == search_name:
                result = Query.parse_obj(query)
                break

        return result

    def update_query(self, query_id: int, query: str, options: dict = None):

        if options is None or not isinstance(options, dict):
            options = {}

        payload = {"query": query, "options": options}
        result = self._client.update_query(query_id, payload)
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

    def get_data_source_list(self):
        return self._client.get_data_sources()

    def get_query_list(self):
        return self._client.paginate(self._client.queries)

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
