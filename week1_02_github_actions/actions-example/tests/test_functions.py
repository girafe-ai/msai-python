# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def our_great_fixture():
    lst = [1]
    print(f"Our list: {lst!r}")

    yield lst

    lst.clear()
    print(f"Our list: {lst!r}")


def test_simple(our_great_fixture):
    assert our_great_fixture == [1]
