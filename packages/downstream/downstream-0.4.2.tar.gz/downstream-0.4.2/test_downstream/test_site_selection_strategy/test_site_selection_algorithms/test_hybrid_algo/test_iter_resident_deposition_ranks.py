import itertools as it

import numpy as np
import pytest

from downstream.downstream import hybrid_algo as algo


@pytest.mark.parametrize("surface_size", [2**x for x in range(2, 12)])
@pytest.mark.parametrize(
    "rank",
    [
        *range(128),
        *map(int, np.linspace(0, 2**62, 100, dtype=int)),
        *map(int, np.geomspace(1, 2**62, 100, dtype=int)),
        *map(int, np.random.RandomState(seed=1).randint(0, 2**62, 100)),
    ],
)
def test_iter_resident_deposition_ranks(surface_size: int, rank: int) -> int:
    if rank > 2 ** (surface_size.bit_length() - 1) - 1:
        return

    expected = (
        algo.calc_resident_deposition_rank(site, surface_size, rank)
        for site in range(surface_size)
    )
    actual = algo.iter_resident_deposition_ranks(surface_size, rank)
    assert all(it.starmap(int.__eq__, zip(actual, expected, strict=True)))
