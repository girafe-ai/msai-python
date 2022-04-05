import requests


try:
    response = requests.get('https://goojdiudoeiwul3dgle.com/')
except (requests.ConnectionError, requests.Timeout):
    print('ConnectionError happened')
    raise  # re raising caught exception
except requests.RequestException as e:
    print(f'Something goes wrong in requests: {type(e)} {e}')
    raise  # re raising caught exception
else:
    print(response)
finally:
    print('Request handling is finished')


class StrListException(Exception):
    def __init__(self, data=None, *args):
        super().__init__(*args)
        self.data = data


class WrongType(StrListException, TypeError):
    pass


class WrongSize(StrListException, ValueError):
    pass


class StrList:
    """
    StrList is list-like container for strings.
    """

    @classmethod
    def _validate_state(cls, state: list[str] | None) -> list[str]:
        if state is None:
            return []

        if not isinstance(state, list):
            raise WrongType(f'state of {cls.__name__} must be list[str]')

        for element in state:
            if not isinstance(element, str):
                raise WrongType(f'state of {cls.__name__} must be list[str]')

        return state

    @staticmethod
    def _validate_str(element: str) -> str:
        if not isinstance(element, str):
            raise WrongType('element must be str')
        return element

    @staticmethod
    def _validate_int(value: int) -> int:
        if not isinstance(value, int):
            raise WrongType('value must be int')
        if value <= 0:
            raise WrongSize('value must be positive integer')
        return value

    # ...


try:
    StrList._validate_int(10)
except StrListException:
    pass
