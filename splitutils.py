import math
import itertools
import os

import numpy as np

def get_data(fname):
    """Given a filename FNAME, return list of lines with trailing whitespace stripped."""

    with open(fname) as fh:
        tmp = fh.readlines()
    return [v.rstrip() for v in tmp]

def get_subset_from_range(rmin, rmax, count):
    """Given a range RMIN to RMAX, return COUNT integers in range.

    If the COUNT is greater than the number of items in the range,
    return the entire range.

    In any event, the results are shuffled randomly.
    """
    r = range(rmin, rmax)
    if len(r) < count:
        tmp = list(r)
        np.random.shuffle(tmp)
        return tmp

    s = list(np.random.choice(r, size=count, replace=False))
    return s

def make_geometric_series(sum_of_terms, term_count, first_term_minimum, ratio=2.0):
    """Compute a geometric series.

    The sum of the series is SUM_OF_TERMS, the number of terms
    is TERM_COUNT, and the ratio between terms is RATIO. The first
    term of the series is minimum FIRST_TERM_MINIMUM.

    Each term is an integer, so the ratios may not exactly equal the
    requested value due to rounding.  The computation for each term is
    rounded up, and in no case will the sum be different than requested.

    Special cases:
        If requested sum is non-positive, a sequence of zeros is returned
        If the count of terms is non-positive, and empty list is returned
        If the ratio is non-positive, the entire sum is in the first term and
            remaining terms are 0.
    """
    if sum_of_terms <= 0:
        return [0] * term_count
    elif term_count <= 0:
        return []
    elif term_count == 1:
        return [sum_of_terms]
    elif ratio <= 0:
        return [sum_of_terms] + [0] * (term_count - 1)

    divisor = term_count
    if ratio != 1:
        divisor = abs((ratio ** term_count - 1) /
                      (ratio - 1))
    number_for_first_tier = math.ceil(sum_of_terms / divisor)
    if number_for_first_tier < first_term_minimum:
        number_for_first_tier = min(sum_of_terms, first_term_minimum)

    sum_of_terms -= number_for_first_tier
    term_count -= 1
    first_term_minimum = math.ceil(
        first_term_minimum * ratio)
    tail = make_geometric_series(
        sum_of_terms, term_count, first_term_minimum, ratio)

    value = [number_for_first_tier] + tail
    return value

def compute_ranges(values):
    """Given an iterable of VALUES, return sequence of pairs (min, max)
    
    The first value returned is (0, values[0]).  Return value i is
    (rv[i-1].min + values[i-1], rv[i-1].max + values[i]).
    For example, the input [1,2,3,4] returns the list
    [(0,1), (1, 3), (3,6), (6,10))].
    
    The empty list returns the empty list.
    """
    if not values :
        return []

    ends = list(itertools.accumulate(values))
    starts = [0] + ends[:-1]
    return list(zip(starts, ends))

def partition_by_index(data, indexes):
    """Partition a sequence of data into a list from matching index in INDEXS and the rest."""
    included, excluded = [], []
    for i,v in enumerate(data) :
        if i in indexes :
            included.append(v)
        else :
            excluded.append(v)
    return included, excluded

def write_or_unlink(data, fname, writer):
    """Write DATA to FNAME if there is data, else unlink FNAME
    
    Write the data using WRITER.

    Catch exceptions if FNAME does not exist and needs to be deleted.
    """
    if data:
        with open(fname, 'w') as fh:
            writer(fh)
    else:
        try:
            os.unlink(fname)
        except:
            pass
