# resources/data_connector.py
from __future__ import annotations

from typing import TYPE_CHECKING
from .._constants import (BASE_URL_V2)

import httpx
import os
import json

if TYPE_CHECKING:
    from .._client import PigeonsAI


class DataConnector:
    data_connection_pri_global = None
    train_set_pri_global = None

    def __init__(self, client: PigeonsAI):
        self.client = client

    def create_connector(
        self,
        connection_name: str,
        connection_type: str,
        db_host: str,
        db_name: str,
        db_username: str,
        db_password: str,
        db_port: int
    ):
        url = f"{BASE_URL_V2}/create-data-connector"
        headers = self.client.auth_headers
        data = {
            "conn_id": connection_name,
            "conn_type": connection_type,
            "host": db_host,
            "login": db_username,
            "password": db_password,
            "port": db_port,
            "schema_param": db_name
        }

        response = self.client._request("POST", url, headers=headers, data=data)
        response_json = response.json()

        _data = response_json['data']

        DataConnector.data_connection_pri_global = _data['data_connection_pri']

        filtered_res = {
            'id': _data['id'],
            'created_at': _data['created_at'],
            'created_by': _data['created_by'],
            'data_connection_pri': _data['data_connection_pri'],
        }

        print(
            f'\033[38;2;85;87;93m Connector creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
        print(f'\033[38;2;85;87;93m Data connector URI:\033[0m \033[92m{_data["data_connection_pri"]}\033[0m')

        return filtered_res

    def create_train_set(
        self,
        type: str,
        train_set_name: str,
        columns_map: dict,
        file_path: str = None,
        data_connection_pri: str = None,
        table_name: str = None,
    ):

        # Use the global data_connection_pri if not provided
        if not data_connection_pri and DataConnector.data_connection_pri_global:
            data_connection_pri = DataConnector.data_connection_pri_global

        if (file_path and data_connection_pri) or (file_path and table_name):
            print("Only one of file or connector_details with table_name should be provided.")
            return

        elif not file_path and not data_connection_pri and not table_name:
            print("Either file or connector_details with table_name must be provided.")
            return

        type = type.lower()
        if not type:
            print('Please provide type as either file or connection. Use file option if you want to upload file or use connection if you want to fetch data directly from the database using data connector. ')
            return

        headers = self.client.auth_headers

        if type == 'file':
            if not file_path:
                print('Missing file path.')
                return
            return _prepare_data_with_file(
                headers=headers,
                train_set_name=train_set_name,
                file_path=file_path,
                columns_map=columns_map
            )

        if type == 'connection':
            if not table_name:
                print('Missing table name. table_name param is the name of the table you want to fetch data from.')
                return

            return _prepare_data_with_connector(
                client=self.client,
                headers=headers,
                train_set_name=train_set_name,
                data_connection_pri=data_connection_pri,
                table_name=table_name,
                columns_map=columns_map
            )

    def revision_train_set_with_file(
        self,
        train_set_pri: str,
        file_path: str,
    ):
        url = f"{BASE_URL_V2}/revision-data-source-with-file"
        headers = self.client.auth_headers
        if 'Content-Type' in headers:
            headers.pop('Content-Type')
        data = {
            'train_set_pri': train_set_pri,
        }

        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f)}
                response = httpx.post(url, headers=headers, files=files, data=data, timeout=300.0)
                response.raise_for_status()
            response_json = response.json()

            data_source_pri = response_json['data']

            filtered_res = {
                'train_set_pri': data_source_pri
            }

            DataConnector.train_set_pri_global = data_source_pri

            print(
                f'\033[38;2;85;87;93m Train set new revision creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
            print(f'\033[38;2;85;87;93m Train set URI:\033[0m \033[92m{data_source_pri}\033[0m')

            return filtered_res
        except httpx.HTTPStatusError as e:
            error_message = f"Status code: {e.response.status_code}, detail: {e.response.text}"
            print(error_message)
        except Exception as e:
            print(f'Status code: {e.response.status_code}, detail: {e.response.text}')
            raise e

    def revision_train_set_with_connector(
        self,
        train_set_pri: str,
    ):
        url = f"{BASE_URL_V2}/revision-data-source-with-connector"
        headers = self.client.auth_headers

        data = {'train_set_pri': train_set_pri}

        response = self.client._request("POST", url, headers=headers, data=data)
        response_json = response.json()

        data_source_pri = response_json['data']

        filtered_res = {
            'train_set_pri': data_source_pri
        }

        DataConnector.train_set_pri_global = data_source_pri

        print(
            f'\033[38;2;85;87;93m Train set creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
        print(f'\033[38;2;85;87;93m Train set URI:\033[0m \033[92m{data_source_pri}\033[0m')

        return filtered_res

    def delete_train_set(self, train_set_pri: str):
        url = f"{BASE_URL_V2}/delete-data-source"
        data = {"train_set_pri": train_set_pri}
        headers = self.client.auth_headers

        return self.client._request("POST", url, headers=headers, data=data)

    def delete_data_connector(self, data_connector_pri: str):
        url = f"{BASE_URL_V2}/delete-data-connector"
        data = {"data_connector_pri": data_connector_pri}
        headers = self.client.auth_headers

        return self.client._request("POST", url, headers=headers, data=data)


def _prepare_data_with_file(
    headers,
    train_set_name: str,
    file_path: str,
    columns_map: dict
):
    url = f"{BASE_URL_V2}/create-data-source-with-file"

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    if 'Content-Type' in headers:
        headers.pop('Content-Type')

    data = {
        'data_source_name': train_set_name,
        'file_name': file_name,
        'file_size': str(file_size),
        'columns_map': json.dumps(columns_map)
    }
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = httpx.post(url, headers=headers, files=files, data=data, timeout=300.0)
            response.raise_for_status()
        response_json = response.json()

        _data = response_json['data']

        filtered_res = {
            'id': _data['id'],
            'created_at': _data.get('created_at'),
            'created_by': _data.get('created_by'),
            'train_set_pri': _data.get('data_source_pri')
        }

        DataConnector.train_set_pri_global = _data.get("data_source_pri", "")

        print(
            f'\033[38;2;85;87;93m Train set creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
        print(f'\033[38;2;85;87;93m Train set URI:\033[0m \033[92m{_data.get("data_source_pri", "")}\033[0m')

        return filtered_res
    except Exception as e:
        print(f'Status code: {e.response.status_code}, detail: {e.response.text}')
        raise e


def _prepare_data_with_connector(
    client: PigeonsAI,
    train_set_name: str,
    data_connection_pri: str,
    table_name: str,
    columns_map: dict,
    headers,
):
    url = f"{BASE_URL_V2}/create-data-source-with-connector"
    data = {
        'data_source_name': train_set_name,
        'data_connection_pri': data_connection_pri,
        'table_name': table_name,
        'columns_map': columns_map
    }
    response = client._request("POST", url, headers=headers, data=data)
    response_json = response.json()

    _data = response_json['data']

    filtered_res = {
        'id': _data['id'],
        'created_at': _data.get('created_at'),
        'created_by': _data.get('created_by'),
        'train_set_pri': _data.get('data_source_pri')
    }

    DataConnector.train_set_pri_global = _data.get("data_source_pri", "")

    print(
        f'\033[38;2;85;87;93m Train set creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
    print(f'\033[38;2;85;87;93m Train set URI:\033[0m \033[92m{_data.get("data_source_pri", "")}\033[0m')

    return filtered_res
