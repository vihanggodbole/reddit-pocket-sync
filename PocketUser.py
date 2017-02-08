import requests
import webbrowser
import sys
from pprint import pprint


class PocketUser:
    '''A pocket user class'''
    def __init__(self, consumer_key):
        self.consumer_key = consumer_key
        self.access_code = ''

    def get_request_token(self):
        request_token_params = {'consumer_key': self.consumer_key, 'redirect_uri': 'http://127.0.0.1:5000/'}
        request_token = requests.post('https://getpocket.com/v3/oauth/request', data=request_token_params)
        if request_token.status_code == 200:
            request_token_code = request_token.content.decode('utf-8').split('=')[1]
        else:
            print('Request token not found. Error - {}'.format(request_token.status_code))
            sys.exit()

        auth_url = 'https://getpocket.com/auth/authorize?request_token=' + request_token_code + '&redirect_uri=http://127.0.0.1:5000/'
        webbrowser.open_new_tab(auth_url)
        return request_token_code

    def get_access_token(self, request_token_code):
        access_token_params = {'consumer_key': self.consumer_key, 'code': request_token_code}
        access_token = requests.post('https://getpocket.com/v3/oauth/authorize', data=access_token_params)
        if access_token.status_code == 200:
            access_token_code = access_token.content.decode('utf-8').split('&')[0]
            access_token_code = access_token_code.split('=')[1]
        else:
            print('Access token not found. Error - {}'.format(access_token.status_code))
            pprint(vars(access_token))
            sys.exit()
        return access_token_code

    def login(self):
        '''Logs in the user using OAuth and returns the access token code for use.'''
        request_code = self.get_request_token()
        input('Once you have authorized your account in the web browser, please press any to continue...')
        self.access_code = self.get_access_token(request_token_code=request_code)


    def batch_add(self, bulk_params):
        '''Add multiple items in one call.'''
        params = {'consumer_key': self.consumer_key, 'access_token': self.access_code, 'actions': bulk_params}
        add_response = requests.post('https://getpocket.com/v3/send', json=params)
        if add_response.status_code == 200:
            return True
        else:
            print('Could not add items.\nError code - {}'.format(add_response.status_code))
            pprint(vars(add_response.headers))
            return False
