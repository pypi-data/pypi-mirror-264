def get_nth_segment_bin_count(n: int) -> int:
    if n == 0:
        return 1
    else:
        return 1 << (n - 1)
