from ..exceptions import APIException

__all__ = ('Connections')

class Connections:
    __slots__ = (
        'token',
        'session',
    )

    def __init__(self, session, token):
        self.token, self.session = token, session

    async def post(self, method, body):
        url = 'https://messengerg2b1.iranlms.ir/v3/{}/{}'.format(
            self.token,
            method,
        )
        while True:
            async with self.session.post(url, json=body) as response:
                if response.ok:
                    status_code = response.status
                    response = await response.json()
                    if response.get('status') == 'OK':
                        return response.get('data')
                    else:
                        raise APIException(
                            'Response(status_code: {}, body: {}'.format(
                                status_code,
                                response or {},
                            )
                        )