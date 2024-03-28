from contextvars import ContextVar
import logging
import os


logger = logging.getLogger(__name__)


class _ContextContainer:
    """
    Base class for context aware values. Extensions of this class
    define fields that fundamentally ContextVar with tags and values.
    """
    def __init__(self, name, fields) -> None:
        self.__context = {}
        for tag in fields:
            self.__context[tag] = ContextVar(f'{name}_{tag}')

    def __getattr__(self, __name: str) -> any:
        if __name.endswith('__context'):
            return self.__dict__['__context']
        if __name in self.__context:
            return self.__context[__name].get(None)
        raise AttributeError(f'attribute {__name} does not exist')

    def __setattr__(self, __name: str, __value: any) -> None:
        if __name.endswith('__context'):
            self.__dict__['__context'] = __value
        elif __name in self.__context:
            self.__context[__name].set(__value)
        else:
            raise AttributeError(f'attribute {__name} does not exist')


class Context(_ContextContainer):
    """
    This context aware class represents the "application context".
    The intention is to stuff values in this class with "inject"
    that is scoped internally to different things. Think of it
    as a dependency injection / inversion of code utility class.
    """
    def __init__(self) -> None:
        super().__init__('application', [
            'internal_scopes',
        ])

    def inject(self, name, value, scope='GLOBAL', force=False):
        """
        Inject a value, by name, in a specific scope (defaulting to GLOBAL).
        If a name is already in use a warning is emitted. Use the force
        flag to overwrite the value. This is useful in testing to override
        values intended for a live system in unit or integration tests.

        app_context.inject('myname', 'myvalue')
        assert app_context.resolve('GLOBAL')['myname'] == 'myvalue'
        """
        if self.internal_scopes is None:
            self.internal_scopes = {}
        if scope not in self.internal_scopes:
            self.internal_scopes[scope] = {}
        if force or name not in self.internal_scopes[scope]:
            self.internal_scopes[scope][name] = value
        else:
            logger.warning(f'Trying to override {name}, use remove or force')

    def remove(self, name, scope='GLOBAL'):
        """
        Explicitly removes a value injected in a scope.

        app_context.remove('myname')
        """
        return self.internal_scopes[scope].pop(name)

    def scopes(self):
        """
        Lists the available scopes the Context is tracking.

        app_context.scopes() == ['GLOBAL']
        """
        if self.internal_scopes is None:
            return []
        return self.internal_scopes.keys()

    def keys_in_scope(self, scope="GLOBAL"):
        """
        Lists the names within a scope the Context is tracking.

        app_context.keys_in_scope() == ['myname']
        """
        return self.resolve(scope).keys()

    def resolve(self, scope="GLOBAL"):
        """
        Returns the cache of values injected in a specified scope.

        app_context.resolve() == {'myname': 'myvalue'}
        """
        if self.internal_scopes is None:
            return {}
        if scope not in self.internal_scopes:
            return {}
        return self.internal_scopes[scope]


class Request(_ContextContainer):
    """
    This context aware class is intended to map to an incoming
    AWS Lambda invocation. The input "event" and "context" are
    set by the router, as well as cookie, query parameters, and
    header information.
    """
    def __init__(self) -> None:
        super().__init__("request", [
            "headers",
            "cookies",
            "body",
            "queryparams",
            "event",
            "context"
        ])

    def request_context(self, key, default_value=None):
        """
        This method is a helper to pull a key out of the
        "requestContext", which is AWS LAmbda hydrated metdata
        frequently used in websocket and HTTP API endpoints.
        """
        return self.event['requestContext'].get(key, default_value)

    def authorizer(self):
        return self.request_context('authorizer')

    def username(self):
        return self.authorizer()['jwt']['claims']['username']

    def account_id(self, osenv_hint='ACCOUNT_ID'):
        return self.request_context('accountId', os.getenv(osenv_hint))

    def api_id(self):
        return self.request_context('apiId')

    def remote_addr(self):
        return self.request_context('http')['sourceIp']

    def method(self):
        return self.request_context('http')['method']


class Response(_ContextContainer):
    """
    This context aware class represents the response data used
    in Router decorated methods. This includes the status_code,
    headers, and any body information.
    """
    def __init__(self) -> None:
        super().__init__("response", [
            "abort",
            "headers",
            "body",
            "status_code"
        ])

    def is_aborted(self):
        """
        Helper method to determine if the response was aborted
        in mid execution.
        """
        return self.abort is True

    def break_continuation(self):
        """
        This method is intended to be used by filter decorations
        from a Router instance to terminate execution and immediately
        dispatch output. This allows an application to stack multiple
        filters and conditionally invoke break_continuation() from
        further execution.
        """
        self.abort = True
        return self
