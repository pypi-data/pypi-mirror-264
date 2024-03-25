import numpy as np

from downstream.pylib.hanoi import get_hanoi_value_index_offset
from downstream.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_global_num_reservations,
)


def _expected8(rank: int) -> int:
    if rank < get_hanoi_value_index_offset(3):
        return 4
    elif rank < get_hanoi_value_index_offset(4):
        return 2
    else:
        return 1


def test_get_global_num_reservations8():
    surface_size = 8
    for rank in range(2**8):
        assert get_global_num_reservations(rank, surface_size) == _expected8(
            rank,
        )


def _expected16(rank: int) -> int:
    if rank < get_hanoi_value_index_offset(4):
        return 8
    elif rank < get_hanoi_value_index_offset(5):
        return 4
    elif rank < get_hanoi_value_index_offset(8):
        return 2
    else:
        return 1


def test_get_global_num_reservations16():
    surface_size = 16
    for rank in range(2**16):
        assert get_global_num_reservations(rank, surface_size) == _expected16(
            rank,
        )


def _expected32(rank: int) -> int:
    if rank < get_hanoi_value_index_offset(5):
        return 16
    elif rank < get_hanoi_value_index_offset(6):
        return 8
    elif rank < get_hanoi_value_index_offset(9):
        return 4
    elif rank < get_hanoi_value_index_offset(16):
        return 2
    else:
        return 1


def test_get_global_num_reservations32():
    surface_size = 32
    for rank in range(2**16):
        assert get_global_num_reservations(rank, surface_size) == _expected32(
            rank
        )

    for rank in np.random.randint(0, 2**32, size=10000):
        rank = int(rank)
        assert get_global_num_reservations(rank, surface_size) == _expected32(
            rank
        )


def _expected64(rank: int) -> int:
    if rank < get_hanoi_value_index_offset(6):
        return 32
    elif rank < get_hanoi_value_index_offset(7):
        return 16
    elif rank < get_hanoi_value_index_offset(10):
        return 8
    elif rank < get_hanoi_value_index_offset(17):
        return 4
    elif rank < get_hanoi_value_index_offset(32):
        return 2
    else:
        return 1


def test_get_global_num_reservations64():
    surface_size = 64
    for rank in range(2**16):
        assert get_global_num_reservations(rank, surface_size) == _expected64(
            rank,
        )

    for rank in np.random.randint(0, 2**63, size=10000):  # signed precision
        rank = int(rank)
        assert get_global_num_reservations(rank, surface_size) == _expected64(
            rank,
        )
