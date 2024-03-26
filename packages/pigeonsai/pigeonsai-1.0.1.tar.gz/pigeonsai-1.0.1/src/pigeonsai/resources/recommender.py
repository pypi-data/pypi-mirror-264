# resources/recommender.py
from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from .._constants import (BASE_URL_V2)

import httpx

if TYPE_CHECKING:
    from .._client import PigeonsAI
    from .data_connector import DataConnector


class Recommender:
    def __init__(self, client: PigeonsAI):
        self.client = client
        self._vae = VAE(client)
        self._transformer = Transformer(client)

    @property
    def vae(self):
        return self._vae

    @property
    def transformer(self):
        return self._transformer


class BaseModelTrainer:
    def __init__(self, client: PigeonsAI, model_architecture: str):
        self.client = client
        self.model_architecture = model_architecture

    def _train(self, custom_model_name: str, train_set_pri: Optional[str] = None, **kwargs):
        if not train_set_pri and DataConnector.train_set_pri_global:
            train_set_pri = DataConnector.train_set_pri_global

        if not train_set_pri:
            raise ValueError("train_set_pri must be provided")

        data = {
            'custom_model_name': custom_model_name,
            'data_source_pri': train_set_pri,
            'original_model_name': 'Recommender',
            'model_architecture': self.model_architecture,
        }
        data.update(kwargs)

        url = BASE_URL_V2 + '/train'
        headers = self.client.auth_headers

        print(f'\033[38;2;229;192;108m      Initializing {custom_model_name} training \033[0m')

        response = self.client._request("POST", url, headers=headers, data=data)
        response_json = response.json()

        print(f'\033[38;2;85;87;93m Training job creation successful.\033[0m')

        print(
            f'\033[38;2;85;87;93m Unique Identifier:\033[0m \033[92m{response_json["data"]["unique_identifier"]}\033[0m')
        print(f'\033[38;2;85;87;93m Endpoint:\033[0m \033[92m{response_json["data"]["endpoint"]}\033[0m')
        print(f'\033[38;2;85;87;93m Message:\033[0m \033[92m{response_json["message"]}\033[0m')

        return response

    def _inference(
        self,
        user_history_ids: Optional[str] = None,
        user_id: Optional[int] = None,
        k: int = 10,
        model_uri: str = None,
        model_name: str = None
    ):
        if user_history_ids is None and user_id is None:
            raise ValueError("Either user_id or user_history_ids must be provided.")

        if model_name and model_uri:
            raise ValueError("Both model_name and model_uri are provided. Either one of them will be used.")

        model_uri = _construct_model_url(model_uri=model_uri, model_name=model_name)

        headers = self.client.auth_headers
        data = {
            "k": k,
            "user_id": user_id,
            "history_ids": user_history_ids,
        }

        try:
            response = self.client._http_client.post(model_uri, headers=headers, json=data, timeout=300.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"Status code: {e.response.status_code}, Error: {e.response.text}"
            print(error_message)
        except Exception as e:
            raise e


class Transformer(BaseModelTrainer):
    def __init__(self, client: PigeonsAI):
        super().__init__(client, model_architecture='transformer')

    def train(
        self,
        custom_model_name: str,
        train_set_pri: Optional[str] = None,
        n_epochs: Optional[str] = None,
        batch_size: Optional[str] = None,
        learn_rate: Optional[str] = None,
    ):
        kwargs = {
            'n_epochs': n_epochs,
            'batch_size': batch_size,
            'learn_rate': learn_rate,
        }
        return self._train(custom_model_name, train_set_pri, **{k: v for k, v in kwargs.items() if v is not None})

    def inference(
        self,
        user_history_ids: Optional[str] = None,
        user_id: Optional[int] = None,
        k: int = 10,
        model_uri: str = None,
        model_name: str = None
    ):
        return self._inference(
            user_history_ids=user_history_ids,
            user_id=user_id,
            k=k,
            model_uri=model_uri,
            model_name=model_name
        )


class VAE(BaseModelTrainer):
    def __init__(self, client: PigeonsAI):
        super().__init__(client, model_architecture='autoencoder')

    def train(
        self,
        custom_model_name: str,
        train_set_pri: Optional[str] = None,
        n_epochs: Optional[str] = None,
        batch_size: Optional[str] = None,
        learn_rate: Optional[str] = None,
        beta: Optional[str] = None,
        verbose: Optional[str] = None,
        train_prop: Optional[str] = None,
        random_seed: Optional[str] = None,
        latent_dims: Optional[str] = None,
        hidden_dims: Optional[str] = None,
        recall_at_k: Optional[str] = None,
        eval_iterations: Optional[str] = None,
        act_fn: Optional[str] = None,
        likelihood: Optional[str] = None,
        data_subset_percent: Optional[str] = None,
    ):
        kwargs = {
            'n_epochs': n_epochs,
            'batch_size': batch_size,
            'learn_rate': learn_rate,
            'beta': beta,
            'verbose': verbose,
            'train_prop': train_prop,
            'random_seed': random_seed,
            'latent_dims': latent_dims,
            'hidden_dims': hidden_dims,
            'recall_at_k': recall_at_k,
            'eval_iterations': eval_iterations,
            'act_fn': act_fn,
            'likelihood': likelihood,
            'data_subset_percent': data_subset_percent,
        }
        return self._train(custom_model_name, train_set_pri, **{k: v for k, v in kwargs.items() if v is not None})

    def retrain(
        self,
        unique_identifier: str,
        pull_latest_data: bool,
    ):
        if not unique_identifier:
            print('unique_identifier is required.')
        if not pull_latest_data:
            print('automatic_data_revision is required.')

        data = {
            'unique_identifier': unique_identifier,
            'pull_latest_data': pull_latest_data,
        }

        url = BASE_URL_V2 + '/retrain'
        headers = self.client.auth_headers

        return self.client._request("POST", url, headers=headers, data=data)

    def inference(
        self,
        user_history_ids: Optional[str] = None,
        user_id: Optional[int] = None,
        k: int = 10,
        model_uri: str = None,
        model_name: str = None
    ):
        return self._inference(
            user_history_ids=user_history_ids,
            user_id=user_id,
            k=k,
            model_uri=model_uri,
            model_name=model_name
        )


def _construct_model_url(model_name: Optional[str] = None, model_uri: Optional[str] = None) -> str:
    if model_name:
        return f"https://{model_name}.apps.api1.pigeonsai.cloud/recommend"
    elif model_uri:
        return f"{model_uri.rstrip('/')}/recommend"
    else:
        raise ValueError("Either model_name or model_uri must be provided")
