# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(autouse=True)
def auto_fixture():
    print("Set Up")
    yield
    print("Tear Down")
