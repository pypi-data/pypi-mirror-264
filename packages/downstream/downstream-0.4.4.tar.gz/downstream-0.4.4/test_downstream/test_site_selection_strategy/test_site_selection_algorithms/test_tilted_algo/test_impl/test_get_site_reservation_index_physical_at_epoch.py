import typing

import pytest

from downstream.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_site_reservation_index_physical_at_epoch,
)


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 1, 2, 2, 3],
        [0, 0, 0, 0, 0, 1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7],
        [0, 0, 0, 1],
    ],
)
def test_get_site_reservation_index_physical_at_epoch_epoch0(
    expected: typing.List[int],
):
    assert len(expected).bit_count() == 1  # power of 2
    actual = [
        get_site_reservation_index_physical_at_epoch(site, 0, len(expected))
        for site in range(len(expected))
    ]
    assert expected == actual


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3],
        [0, 0, 0, 0],
    ],
)
def test_get_site_reservation_index_physical_at_epoch_epoch1(
    expected: typing.List[int],
):
    assert len(expected).bit_count() == 1  # power of 2
    actual = [
        get_site_reservation_index_physical_at_epoch(site, 1, len(expected))
        for site in range(len(expected))
    ]
    assert expected == actual


@pytest.mark.parametrize(
    "expected",
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    ],
)
def test_get_site_reservation_index_physical_at_epoch_epoch2(
    expected: typing.List[int],
):
    surface_size = len(expected)
    assert surface_size.bit_count() == 1  # power of 2
    actual = [
        get_site_reservation_index_physical_at_epoch(site, 2, surface_size)
        for site in range(surface_size)
    ]
    assert expected == actual
