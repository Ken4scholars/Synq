import requests
from json import JSONDecodeError
from django.conf import settings
from django.utils.encoding import force_str, force_text


class SynqException(Exception):
    def __init__(self, message, code=None):
        super(SynqException, self).__init__(message, code)

        self.message = message
        self.code = code

    def __repr__(self):
        return force_str('<{}: code={}>'.format(
            self.__class__.__name__, self.code or 'None'))

    def __str__(self):
        return force_text('Could not sync due to error code {} : {}'.format(self.code, self.message))


class Synq(object):

    def __init__(self):
        self.base_url = settings.SYNC_DOMAIN + '/api/'
        self._headers = {
            'Content-type': 'application/json; charset=UTF-8',
            settings.SYNC_HEADER: settings.SYNC_HEADER_VALUE
        }

    def __enter__(self):
        self.session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None

    def _get_headers(self, extra_headers=None):
        request_headers = self._headers.copy()
        if extra_headers:
            request_headers.update(extra_headers)
        return request_headers

    def __execute__(self, method, path, **kwargs):
        absolute_url = self.base_url + path

        response = self.session.request(method, absolute_url, **kwargs)

        try:
            response_data = response.json()
        except JSONDecodeError as ex:
            return ex.msg

        if not response.ok:
            raise SynqException(str(response_data), code=response.status_code)
        print(response_data)
        return response_data

    def create_order(self, pk, number, name):
        payload = {'id': pk, 'number': number, 'name': name}
        response = self.__execute__('post', 'orders/', json=payload, headers=self._headers)
        return response

    def update_order(self, pk, **kwargs):
        response = self.__execute__('put', 'orders/{}/'.format(pk), json=kwargs, headers=self._headers)
        return response

    def delete_order(self, pk):
        response = self.__execute__('delete', 'orders/{}/'.format(pk), headers=self._headers)
        return response
