import itertools as it
import random

import pytest

import pylib


def test_get_longevity_level_of_mapped_position():
    assert [
        pylib.longevity_ordering_common.get_longevity_level_of_mapped_position(
            mapped_position,
            1,
        )
        for mapped_position in range(1)
    ] == [0]

    assert [
        pylib.longevity_ordering_common.get_longevity_level_of_mapped_position(
            mapped_position,
            2,
        )
        for mapped_position in range(2)
    ] == [0, 1]

    assert [
        pylib.longevity_ordering_common.get_longevity_level_of_mapped_position(
            mapped_position,
            4,
        )
        for mapped_position in range(4)
    ] == [0, 2, 1, 2]

    assert [
        pylib.longevity_ordering_common.get_longevity_level_of_mapped_position(
            mapped_position,
            8,
        )
        for mapped_position in range(8)
    ] == [0, 3, 2, 3, 1, 3, 2, 3]

    assert [
        pylib.longevity_ordering_common.get_longevity_level_of_mapped_position(
            mapped_position,
            16,
        )
        for mapped_position in range(16)
    ] == [0, 4, 3, 4, 2, 4, 3, 4, 1, 4, 3, 4, 2, 4, 3, 4]


@pytest.mark.parametrize("num_indices", [2**x for x in range(64)])
def test_inverse_get_longevity_level_of_index(num_indices):
    random.seed(num_indices)

    for index in it.chain(
        range(min(3000, num_indices)),
        (random.randrange(num_indices) for __ in range(3000)),
    ):

        mapped_position = pylib.longevity_ordering_naive.get_longevity_mapped_position_of_index(
            index,
            num_indices,
        )
        longevity_level_of_index = (
            pylib.longevity_ordering_common.get_longevity_level_of_index(
                index,
            )
        )

        assert (
            pylib.longevity_ordering_common.get_longevity_level_of_mapped_position(
                mapped_position,
                num_indices,
            )
            == longevity_level_of_index
        )
