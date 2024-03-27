import dataclasses
import sys
import logging
from typing import List

import requests

from src.dbrepo.api.dto import User, UserBrief, ContainerBrief, Database, CreateUser, CreateDatabase, UpdateUser, \
    UpdateUserTheme, UpdateUserPassword
from src.dbrepo.api.exceptions import ErrorResponseCode


class RestClient:
    endpoint: str = None
    username: str = None
    password: str = None
    secure: bool = None

    def __init__(self,
                 endpoint: str = 'http://gateway-service',
                 username: str = None,
                 password: str = None,
                 secure: bool = True) -> None:
        logging.getLogger('requests').setLevel(logging.INFO)
        logging.getLogger('urllib3').setLevel(logging.INFO)
        logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-6s %(message)s', level=logging.DEBUG,
                            stream=sys.stdout)
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.secure = secure

    def _wrapper(self, method: str, url: str, payload=None) -> requests.Response:
        url = f'{self.endpoint}{url}'
        logging.debug(f'url: {url}, secure: {self.secure}')
        if payload is not None:
            logging.debug(f'payload: {payload}')
            payload = dataclasses.asdict(payload)
        if self.username is not None and self.password is not None:
            logging.debug(f'username: {self.username}, password: (hidden)')
            return requests.request(method=method, url=url, auth=(self.username, self.password), verify=self.secure,
                                    json=payload)
        return requests.request(method=method, url=url, verify=self.secure, json=payload)

    def get_users(self) -> List[User]:
        url = f'/api/user'
        response = self._wrapper(method="get", url=url)
        if response.status_code == 200:
            body = response.json()
            return User.schema().load(body, many=True)
        raise ErrorResponseCode(f'Failed to fetch users: response code: {response.status_code} is not 200 (OK)')

    def get_user(self, user_id: str) -> User:
        url = f'/api/user/{user_id}'
        response = self._wrapper(method="get", url=url)
        if response.status_code == 200:
            body = response.json()
            return User.schema().load(body)
        raise ErrorResponseCode(
            f'Failed to fetch user with id {user_id}: response code: {response.status_code} is not 200 (OK)')

    def create_user(self, username: str, password: str, email: str) -> UserBrief:
        url = f'/api/user'
        response = self._wrapper(method="post", url=url,
                                 payload=CreateUser(username=username, password=password, email=email))
        if response.status_code == 201:
            body = response.json()
            return UserBrief.schema().load(body)
        if response.status_code == 404:
            raise ErrorResponseCode(
                f'Failed to create user: default role not found')
        if response.status_code == 409:
            raise ErrorResponseCode(
                f'Failed to create user: user with username exists')
        if response.status_code == 417:
            raise ErrorResponseCode(
                f'Failed to create user: user with e-mail exists')
        raise ErrorResponseCode(
            f'Failed to create user: response code: {response.status_code} is not 201 (CREATED)')

    def update_user(self, user_id: str, firstname: str = None, lastname: str = None, affiliation: str = None,
                    orcid: str = None) -> User:
        url = f'/api/user/{user_id}'
        response = self._wrapper(method="put", url=url,
                                 payload=UpdateUser(firstname=firstname, lastname=lastname, affiliation=affiliation,
                                                    orcid=orcid))
        if response.status_code == 202:
            body = response.json()
            return User.schema().load(body)
        if response.status_code == 400:
            raise ErrorResponseCode(
                f'Failed to update user: invalid values')
        if response.status_code == 404:
            raise ErrorResponseCode(
                f'Failed to update user: user not found')
        if response.status_code == 405:
            raise ErrorResponseCode(f'Failed to update user: foreign user')
        raise ErrorResponseCode(
            f'Failed to update user: response code: {response.status_code} is not 202 (ACCEPTED)')

    def update_user_theme(self, user_id: str, theme: str) -> User:
        url = f'/api/user/{user_id}/theme'
        response = self._wrapper(method="put", url=url, payload=UpdateUserTheme(theme=theme))
        if response.status_code == 202:
            body = response.json()
            return User.schema().load(body)
        if response.status_code == 400:
            raise ErrorResponseCode(
                f'Failed to update user theme: invalid values')
        if response.status_code == 404:
            raise ErrorResponseCode(
                f'Failed to update user theme: user not found')
        if response.status_code == 405:
            raise ErrorResponseCode(f'Failed to update user theme: foreign user')
        raise ErrorResponseCode(
            f'Failed to update user theme: response code: {response.status_code} is not 202 (ACCEPTED)')

    def update_user_password(self, user_id: str, password: str) -> User:
        url = f'/api/user/{user_id}/password'
        response = self._wrapper(method="put", url=url, payload=UpdateUserPassword(password=password))
        if response.status_code == 202:
            body = response.json()
            return User.schema().load(body)
        if response.status_code == 400:
            raise ErrorResponseCode(
                f'Failed to update user password: invalid values')
        if response.status_code == 404:
            raise ErrorResponseCode(
                f'Failed to update user password: user not found')
        if response.status_code == 405:
            raise ErrorResponseCode(f'Failed to update user password: foreign user')
        if response.status_code == 503:
            raise ErrorResponseCode(f'Failed to update user password: keycloak error')
        raise ErrorResponseCode(
            f'Failed to update user theme: response code: {response.status_code} is not 202 (ACCEPTED)')

    def get_containers(self) -> List[ContainerBrief]:
        url = f'/api/container'
        response = self._wrapper(method="get", url=url)
        if response.status_code == 200:
            body = response.json()
            return ContainerBrief.schema().load(body, many=True)
        raise ErrorResponseCode(f'Failed to fetch containers: response code: {response.status_code} is not 200 (OK)')

    def get_databases(self) -> List[Database]:
        url = f'/api/database'
        response = self._wrapper(method="get", url=url)
        if response.status_code == 200:
            body = response.json()
            return Database.schema().load(body, many=True)
        raise ErrorResponseCode(f'Failed to fetch databases: response code: {response.status_code} is not 200 (OK)')

    def get_database(self, database_id: int) -> Database:
        url = f'/api/database/{database_id}'
        response = self._wrapper(method="get", url=url)
        if response.status_code == 200:
            body = response.json()
            return Database.schema().load(body)
        raise ErrorResponseCode(
            f'Failed to fetch database with id {database_id}: response code: {response.status_code} is not 200 (OK)')

    def create_database(self, name: str, container_id: int, is_public: bool) -> Database:
        url = f'/api/database'
        response = self._wrapper(method="post", url=url,
                                 payload=CreateDatabase(name=name, container_id=container_id, is_public=is_public))
        if response.status_code == 201:
            body = response.json()
            return Database.schema().load(body)
        raise ErrorResponseCode(
            f'Failed to create database: response code: {response.status_code} is not 201 (CREATED)')
