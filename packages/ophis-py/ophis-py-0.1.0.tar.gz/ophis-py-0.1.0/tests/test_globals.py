from contextvars import copy_context
from ophis.globals import app_context, Request, Response


def test_context():
    app_context.inject('foo', 'bar', "MY_SCOPE")
    app_context.inject('some_value', 'This is a global', 'MY_SCOPE')
    app_context.inject('rqu', 'value', 'REQUEST')
    assert app_context.resolve('MY_SCOPE') == {
        'foo': 'bar',
        'some_value': 'This is a global'
    }

    assert list(app_context.scopes()) == ['GLOBAL', 'MY_SCOPE', 'REQUEST']
    assert list(app_context.keys_in_scope('MY_SCOPE')) == ['foo', 'some_value']


def test_request():
    request = Request()
    request.headers = {'content-type': 'application/json'}
    request.cookies = ['abc=123']
    ctx = copy_context()

    def change_context():
        request.headers = {'content-type': 'text/plain'}
        request.cookies = ['efg=456']
        return {
            'headers': request.headers,
            'cookies': request.cookies
        }

    assert ctx.run(change_context) == {
        'headers': {'content-type': 'text/plain'},
        'cookies': ['efg=456']
    }
    assert request.headers == {'content-type': 'application/json'}
    assert request.cookies == ['abc=123']

    try:
        request.farts
        assert False
    except AttributeError:
        assert True


def test_response():
    response = Response()
    response.headers = {'content-type': 'text/plain'}
    response.status_code = 404
    response.body = "Not found"
    ctx = copy_context()

    def change_context():
        response.headers = {'content-type': 'application/json'}
        response.status_code = 200
        response.body = {'message': 'Hello World!'}
        return {
            'headers': response.headers,
            'statusCode': response.status_code,
            'body': response.body
        }

    assert ctx.run(change_context) == {
        'headers': {'content-type': 'application/json'},
        'statusCode': 200,
        'body': {'message': 'Hello World!'}
    }

    assert response.status_code == 404
    assert response.headers == {'content-type': 'text/plain'}
    assert response.body == "Not found"
