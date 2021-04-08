# -*- coding: utf-8 -*-
import pytest

from my_awesome_package import take


class TestTake:
    """
    This test case is testing 'take' function from package 'my_awesome_package'
    This function should do: ...
    """

    def test_take(self):
        """ Testing that take returns list of first 'n' elements from 'iterable' """
        assert take(1, "asd") == ["a"]

    def test_fail(self):
        with pytest.raises(TypeError):
            take(1, 100)
