from lona.unique_ids import generate_unique_id2


class Request:
    def __init__(self, view_runtime, connection):
        self._view_runtime = view_runtime
        self.connection = connection

        self._id = generate_unique_id2()
        self.url = self._view_runtime.url

        if self.url:
            self.GET = dict(self._view_runtime.url.query)
            self.POST = self._view_runtime.post_data or {}

        else:
            self.GET = {}
            self.POST = {}

        self.method = 'POST' if self.POST else 'GET'

    @property
    def id(self):
        return self._id

    @property
    def interactive(self):
        return self.connection.interactive

    @property
    def user(self):
        return getattr(self.connection, 'user', None)

    @user.setter
    def user(self, new_value):
        self.connection.user = new_value

    @property
    def frontend(self):
        return self._view_runtime.frontend

    @property
    def server(self):
        return self._view_runtime.server

    @property
    def route(self):
        return self._view_runtime.route

    @property
    def match_info(self):
        return self._view_runtime.match_info
