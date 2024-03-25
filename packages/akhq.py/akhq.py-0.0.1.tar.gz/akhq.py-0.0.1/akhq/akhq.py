import requests

class client:
    r"""
    A client for the AKHQ server.
    """
    def __init__(self, url, username: str = None, password: str = None):
        self._url = url
        self.http_session()
        self._username = username
        self._password = password
        self._auth = None
        if username and password:
            self._auth = (username, password)

        # Try to connect to the AKHQ server
        try:
            self.auth(username, password)
        except Exception as e:
            raise Exception(f'Failed to connect to AKHQ server at {url}: {e}')
        
    def http_session(self):
        self.http = requests.Session()
        self.http.headers.update({'Content-Type': 'application/json'})

    def auth(self, username, password):
        self._auth = (username, password)
        self._me = self.get('/api/me').json()
        if self._me['logged'] == False:
            raise Exception('Failed to connect to AKHQ server: not logged in')

    def clusters(self):
        return self.get('/api/cluster').json()

    def topics(self, cluster_id):
        return self.get(f'/api/{cluster_id}/topic').json()['results']

    def consumer_groups(self, cluster_id):
        return self.get(f'/api/{cluster_id}/group').json()['results']

    def get(self, path):
        return self.http.get(self._url + path, auth=self._auth)

    def post(self, path, data):
        return self.http.post(self._url + path, json=data, auth=self._auth)

    def me(self):
        self._me = self.get('/api/me').json()
        return self._me