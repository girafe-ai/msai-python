# -*- coding: utf-8 -*-
import pytest

from my_awesome_package import prepend


class TestPrepend:
    def test_mutable_structure(self):
        test_case = (1, [1, 2, 3])
        expected_result = [1, 1, 2, 3]

        assert list(prepend(*test_case)) == expected_result

    # Well ok, but what if we have too much test cases ?

    @pytest.mark.parametrize(
        "test_case,expected_result",
        [
            ((1, [1, 2, 3]), [1, 1, 2, 3]),
            (([1, 2], (3, 4, 5)), [[1, 2], 3, 4, 5]),
            (("a", "asd"), ["a", "a", "s", "d"]),
        ],
    )
    def test_multiple_mutable_structure(self, test_case, expected_result):
        assert list(prepend(*test_case)) == expected_result