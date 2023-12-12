import logging
from typing import List

import pytest
from src.utils import binary_search

logger = logging.getLogger(__name__)
fh = logging.FileHandler("log.txt")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def test_simple_correct():
    arr = [1, 2, 3, 4, 5]
    assert binary_search(arr, 3) == True


def test_simple_incorrect():
    arr = [1, 2, 3, 4, 5]
    assert binary_search(arr, 0) == False


def test_simple():
    arr = [1, 3, 5]
    assert binary_search(arr, 4) == False


@pytest.mark.parametrize(
    "arr,target,expected",
    (
        ([1, 2, 3, 4, 5], 3, True),
        ([1, 2, 3, 4, 5], 0, False),
        ([1, 3, 5], 4, False),
    ),
)
def test_with_args(arr: List[int], target: int, expected: bool):
    assert binary_search(arr, target) == expected


# # scopes are [ function, class, module, package or session]
@pytest.fixture(scope="session", params=(6, 7, 8, 9))
def arr(request: pytest.FixtureRequest):
    logger.warning("Fixture setup")
    # data acquisition
    data = [1, 2, 3, 4, 5, request.param]

    # data finalization
    def resource_teardown():
        logger.warning("Fixture teardown")
        data.clear()

    request.addfinalizer(resource_teardown)
    return data


def test_with_fixture_1(arr):
    assert binary_search(arr, 3) == True


def test_with_fixture_2(arr):
    assert binary_search(arr, 2) == True


def test_with_fixture_3(arr):
    assert binary_search(arr, 3) == True


def test_with_fixture_4(arr):
    assert binary_search(arr, 9) == False


@pytest.fixture(scope="module")
def resource_setup(request):
    # data acquisition
    # db initialization or network request

    # initialize db
    db = {"R": 1, "G": 2, "B": 3}

    # data finalization
    def resource_teardown():
        # db cleanup
        db.clear()

    request.addfinalizer(resource_teardown)
    return db
