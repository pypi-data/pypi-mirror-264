import pytest

from downstream.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_fractional_downgrade_num_reservations_provided,
    get_fractional_downgrade_state,
)


@pytest.mark.parametrize("hanoi_value", range(4))
@pytest.mark.parametrize("surface_size", [8, 32, 128])
@pytest.mark.parametrize("rank", range(0, 255, 12))
def test_get_fractional_downgrade_state(
    hanoi_value: int, surface_size: int, rank: int
):
    # just a smoke test
    fractional_downgrade_state = get_fractional_downgrade_state(
        hanoi_value, surface_size, rank
    )
    if fractional_downgrade_state is not None:
        actual_result = get_fractional_downgrade_num_reservations_provided(
            hanoi_value, surface_size, rank, fractional_downgrade_state
        )
        assert isinstance(actual_result, int)
