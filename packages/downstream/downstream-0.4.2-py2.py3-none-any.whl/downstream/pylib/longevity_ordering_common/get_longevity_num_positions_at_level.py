def get_longevity_num_positions_at_level(level: int) -> int:
    return 1 << (level - 1) if level else 1
