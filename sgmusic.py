from bisect import bisect_left
from collections.abc import Iterable
from typing import Tuple

from sympy import Integral, symbols

# from typing import Dict, List, Tuple

# Tool for custom rounding
class CustomRound:
    def __init__(self, iterable):
        self.data = sorted(iterable)

    def __call__(self, x):
        data = self.data
        ndata = len(data)
        idx = bisect_left(data, x)
        if idx <= 0:
            return data[0]
        elif idx >= ndata:
            return data[ndata - 1]
        x0 = data[idx - 1]
        x1 = data[idx]
        if abs(x - x0) < abs(x - x1):
            return x0
        return x1


custom_round_values_base = [
    0,
    1 / 5,
    1 / 4,
    1 / 3,
    2 / 5,
    1 / 2,
    3 / 5,
    2 / 3,
    3 / 4,
    4 / 5,
]
custom_round_values = [i + j for i in range(20) for j in custom_round_values_base]
custom_round = CustomRound(custom_round_values)

a, a1, b, b1, c, c1, d, s = symbols("a:2 b:2 c:2 d s")
t, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 = symbols("t:11")


# Ramp code
# %%
def ramp(start_tempo, end_tempo, total_beats, bound_beat, bottom_bound_beat=0):
    """This integral is equal to the timecode at the bound_beat."""
    return Integral(
        1
        / (
            start_tempo / 60
            + (x / total_beats) * (S(end_tempo) / 60 - start_tempo / 60)
        ),
        (x, bottom_bound_beat, bound_beat),
    )


# starting with an unknown function:
# %%
# _test1 = Eq(f(a, b, c, 20) + f(b, b1, c1, s), t)
# display(_test1)
# display(_test1.replace(f, ramp))
# display(_test1.replace(f, ramp).doit())  # this is equal to tempoeq2

# Tools for list of tempo relations in piece


def separatetempolist(combined_list: list) -> Iterable[tuple]:
    """
    See _demotempolist() for an example.
    This function can separate out a list which occassionally contains tuples.
    """

    def separate(item):
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            return item
        else:
            return item, ""

    return zip(*(separate(i) for i in combined_list))


def _demotempolist():
    t, t1, t2 = symbols("t:3")
    tempolist_combined = [(t, "start"), t1, (t2, "somewhere")]
    tempolist, sections = separatetempolist(tempolist_combined)
    return tempolist, sections
