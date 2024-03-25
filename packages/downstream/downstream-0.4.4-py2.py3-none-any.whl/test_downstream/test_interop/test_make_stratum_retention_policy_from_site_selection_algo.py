import types

from hstrat import hstrat
import pytest

from downstream import downstream


@pytest.mark.parametrize(
    "interop_algo",
    [
        downstream.stratum_retention_interop_hybrid_algo,
        downstream.stratum_retention_interop_steady_algo,
        downstream.stratum_retention_interop_tilted_algo,
        downstream.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_GenDropRanks(interop_algo: types.ModuleType, surface_size: int):
    policy = interop_algo.Policy(surface_size)

    for rank in range(surface_size):
        assert [*policy.GenDropRanks(rank)] == []

    # hybrid algo needs tighter bound than others
    nrank = min(100, 2 ** (surface_size // 2 - 1) - 1)
    for rank in range(surface_size, nrank):
        site = interop_algo._site_selection_algo.pick_deposition_site(
            rank, surface_size
        )
        assert [*policy.GenDropRanks(rank)] == [
            interop_algo._site_selection_algo.calc_resident_deposition_rank(
                site, surface_size, rank
            )
        ]


@pytest.mark.parametrize(
    "interop_algo",
    [
        downstream.stratum_retention_interop_hybrid_algo,
        downstream.stratum_retention_interop_steady_algo,
        downstream.stratum_retention_interop_tilted_algo,
        downstream.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_CalcNumStrataRetainedExact(
    interop_algo: types.ModuleType, surface_size: int
):
    policy = interop_algo.Policy(surface_size)

    for rank in range(200):
        assert policy.CalcNumStrataRetainedExact(rank) == min(
            rank, surface_size
        )


@pytest.mark.parametrize(
    "interop_algo",
    [
        downstream.stratum_retention_interop_hybrid_algo,
        downstream.stratum_retention_interop_steady_algo,
        downstream.stratum_retention_interop_tilted_algo,
        downstream.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_CalcRankAtColumnIndex(
    interop_algo: types.ModuleType, surface_size: int
):
    policy = interop_algo.Policy(surface_size)

    assert policy.CalcNumStrataRetainedExact(0) == 0
    for rank in range(1, 100):
        column_ranks = [
            policy.CalcRankAtColumnIndex(index, rank)
            for index in range(policy.CalcNumStrataRetainedExact(rank))
        ]
        assert column_ranks == sorted(
            set(  # have to deduplicate rank 0 entries
                interop_algo._site_selection_algo.iter_resident_deposition_ranks(
                    surface_size, rank
                ),
            ),
        )


@pytest.mark.parametrize(
    "interop_algo",
    [
        downstream.stratum_retention_interop_hybrid_algo,
        downstream.stratum_retention_interop_steady_algo,
        downstream.stratum_retention_interop_tilted_algo,
        downstream.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_CalcNumStrataRetainedUpperBound(
    interop_algo: types.ModuleType, surface_size: int
):
    policy = interop_algo.Policy(surface_size)

    for rank in range(200):
        assert policy.CalcNumStrataRetainedExact(
            rank
        ) <= policy.CalcNumStrataRetainedUpperBound(rank)


@pytest.mark.parametrize(
    "interop_algo",
    [
        downstream.stratum_retention_interop_hybrid_algo,
        downstream.stratum_retention_interop_steady_algo,
        downstream.stratum_retention_interop_tilted_algo,
        downstream.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_IterRetainedRanks(interop_algo: types.ModuleType, surface_size: int):
    policy = interop_algo.Policy(surface_size)

    assert [*policy.IterRetainedRanks(0)] == []
    for rank in range(1, 200):
        column_ranks = [*policy.IterRetainedRanks(rank)]
        assert column_ranks == sorted(
            set(  # have to deduplicate rank 0 entries
                interop_algo._site_selection_algo.iter_resident_deposition_ranks(
                    surface_size, rank
                ),
            ),
        )


@pytest.mark.parametrize(
    "interop_algo",
    [
        downstream.stratum_retention_interop_hybrid_algo,
        downstream.stratum_retention_interop_steady_algo,
        downstream.stratum_retention_interop_tilted_algo,
        downstream.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 16],
)
def test_hstrat_test_drive_integration(
    interop_algo: types.ModuleType, surface_size: int
):
    population_size = 1024
    num_generations = 1000
    alife_df = hstrat.evolve_fitness_trait_population(
        num_islands=4,
        num_niches=4,
        num_generations=num_generations,
        population_size=population_size,
        tournament_size=1,
    )

    extant_population = hstrat.descend_template_phylogeny_alifestd(
        alife_df,
        seed_column=hstrat.HereditaryStratigraphicColumn(
            interop_algo.Policy(surface_size)
        ),
    )
    assert len(extant_population) == population_size
    assert all(
        c.GetNumStrataDeposited() == num_generations + 2
        for c in extant_population
    )


@pytest.mark.parametrize(
    "always_store_rank_in_stratum",
    [True, False],
)
@pytest.mark.parametrize(
    "interop_algo",
    [
        downstream.stratum_retention_interop_hybrid_algo,
        downstream.stratum_retention_interop_steady_algo,
        downstream.stratum_retention_interop_tilted_algo,
        downstream.stratum_retention_interop_tilted_sticky_algo,
    ],
)
@pytest.mark.parametrize(
    "surface_size",
    [8, 32, 64],
)
def test_hstrat_column_integration(
    always_store_rank_in_stratum: bool,
    interop_algo: types.ModuleType,
    surface_size: int,
):
    column = hstrat.HereditaryStratigraphicColumn(
        always_store_rank_in_stratum=always_store_rank_in_stratum,
        stratum_differentia_bit_width=8,
        stratum_retention_policy=interop_algo.Policy(surface_size),
    )
    policy = column._stratum_retention_policy
    ssa = policy.GetSpec()._site_selection_algo
    nrank = min(100, 2 ** (surface_size // 2 - 1) - 1)
    for g in range(nrank - 1):
        assert set(column.IterRetainedRanks()) == set(
            ssa.iter_resident_deposition_ranks(surface_size, g + 1),
        )
        column.DepositStratum()


def test_eq():
    assert downstream.stratum_retention_interop_hybrid_algo.Policy(
        8
    ) != downstream.stratum_retention_interop_hybrid_algo.Policy(16)

    assert downstream.stratum_retention_interop_hybrid_algo.Policy(
        8
    ) == downstream.stratum_retention_interop_hybrid_algo.Policy(8)

    assert downstream.stratum_retention_interop_tilted_sticky_algo.Policy(
        8
    ) != downstream.stratum_retention_interop_hybrid_algo.Policy(8)

    assert downstream.stratum_retention_interop_tilted_algo.Policy(
        64
    ) == downstream.stratum_retention_interop_tilted_algo.Policy(64)

    policy = downstream.stratum_retention_interop_tilted_algo.Policy(32)
    assert policy == policy
