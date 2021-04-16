# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python (multi-group-venv)
#     language: python
#     name: multi-group-venv
# ---

# %% [markdown] colab_type="text" id="view-in-github"
# <a href="https://colab.research.google.com/github/SG60/2021-multi-group-piece/blob/main/Tempos.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %% [markdown] id="VSyKJN8dnb6j"
# #Basic Setup

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="pacUyi3eKdQX" outputId="16022003-308b-4997-b0cb-9ada86dc014b"
from IPython.display import HTML, display


def set_css():
    display(
        HTML(
            """
  <style>
    pre {
        white-space: pre-wrap;
    }
  </style>
  """
        )
    )


get_ipython().events.register("pre_run_cell", set_css)

from sympy import init_session

init_session()

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="yeIJhWt4lmWX" outputId="ae74806b-c2e0-4192-b660-f25c0eb88b9c"
# Tool for custom rounding
from bisect import bisect_left


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

# %% [markdown] id="CkEZ_CLRXTkF"
# # assigments

# %% colab={"base_uri": "https://localhost:8080/", "height": 17} id="uQUh_YL6XQdU" outputId="a9f155b3-8fd5-48e8-9ca9-d9a365e43c4d"
a, a1, b, b1, c, c1, d, s = symbols("a:2 b:2 c:2 d s")
t, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 = symbols("t:11")


# %% [markdown] id="FSN2ZttFEe8A"
# # Ramp code

# %% colab={"base_uri": "https://localhost:8080/", "height": 17} id="a8l4dRchz_nt" outputId="1204d9b2-e399-4d6a-eaae-49363031419c"
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


# %% colab={"base_uri": "https://localhost:8080/", "height": 141} id="pcSTL-cnTGDs" outputId="1e0a2a93-85a9-4c9a-875e-677176de1da6"
# or another way, starting with an unknown function:
_test1 = Eq(f(a, b, c, 20) + f(b, b1, c1, s), t)
display(_test1)
display(_test1.replace(f, ramp))
display(_test1.replace(f, ramp).doit())  # this is equal to tempoeq2

# %% [markdown] id="JoVSpR7pnju0"
# #Wind up+down ramp in A section

# %% [markdown] id="dzxO9ZT8nmak"
# ##Up Ramp

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="yuyDaSI1IfeU" outputId="72c80c7f-ba89-490d-83fe-774fd7ddb266"
a, a1, b, b1, c, c1, s, t = symbols("a:2 b:2 c:2 s t")
# a = start tempo of ramp
# b = end tempo of ramp
# c = length of ramp in beats
# s = beat we are interested in
# t = timecode of that beat
tempoeq = Eq(integrate(1 / (a / 60 + (x / c) * (b / 60 - a / 60)), (x, 0, s)), t)
tempoeq

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="CocA-YZDrbiI" outputId="17a0d209-359d-493d-d072-71f45039ad03"
Eq(Integral(1 / (a / 60 + (x / c) * (b / 60 - a / 60)), (x, 0, s)), t)

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="MY4lqYuYTNjj" outputId="8ac5c715-35cb-460b-d05b-b54937c48fb0"
s_solved = solveset(tempoeq, s).args[0]
display(s_solved)

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="oRJzwbt04SJs" outputId="a829a064-7e06-4065-a3fa-01fa447ff8d3"
# @title Values for steady part
number_of_beats = 13  # @param {type:"integer"}
steady_tempo = 96  # @param {type:"integer"}

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="acZBH-aq4yaK" outputId="f19fefcd-849b-443f-c779-5be95846b739"
# @title Values for ramp part
start_tempo = 96  # @param {type:"integer"}
end_tempo = 240  # @param {type:"integer"}
length_in_beats = 20  # @param {type:"integer"}

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="sROOBAlRvr_g" outputId="8b375bee-891b-44c2-ef28-e6dc78c23cbd"
temposteady = steady_tempo
beatlength = S(60) / steady_tempo
# beats = [0, S(1)/3, 2, 4]
beats = range(number_of_beats)
beattimecodes_up_ramp = [beatlength * i for i in beats]
outbeats = [
    s_solved.n(6, {a: start_tempo, b: end_tempo, c: length_in_beats, t: i}, chop=True)
    for i in beattimecodes_up_ramp
]
for i in range(len(outbeats)):
    print(beats[i], outbeats[i])

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="s0whC0B12col" outputId="955a9bc4-2128-433d-a52b-9be67aec1575"
print(1 / 5, 1 / 4, 1 / 3, 2 / 5, 1 / 2, 3 / 5, 2 / 3, 3 / 4, 4 / 5)

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="1AK2TZB5IQFz" outputId="654ef989-8af5-4659-ed27-0b994be293ad"
display(beattimecodes_up_ramp[12].n())
display([i.n() for i in beattimecodes_up_ramp])

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="2Y_GIxPUJHpY" outputId="809afcbc-1ead-4eca-a2ae-2eed81669239"
# Timecode at beat 20
solveset(tempoeq.subs({a: start_tempo, b: end_tempo, c: length_in_beats, s: 20}), t).n(
    6
)

# %% [markdown] id="DzLdtjCVnqxG"
# ##Down Ramp

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="BQi6KWgwKdcT" outputId="b836b9ed-f9b1-4068-ebdd-0af92fa67eba"
# b1 = end tempo of down ramp
# c1 = number of beats in down ramp
tempoeq2_not_done = Eq(
    Integral(1 / (a / 60 + (x / c) * (b / 60 - a / 60)), (x, 0, 20))
    + Integral(1 / (b / 60 + (x / c1) * (b1 / 60 - b / 60)), (x, 0, s)),
    t,
)
display(tempoeq2_not_done)
tempoeq2 = tempoeq2_not_done.doit()
display(tempoeq2)

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="ybp5oRGJNS7X" outputId="ff0e8169-9dad-41dd-941f-90a19b83ec9d"
s2_solved = solveset(tempoeq2, s).args[0]
# display(s2_solved.args[0])
s2_solved_subbed = s2_solved.subs({a: 96, b: 240, c: 20, b1: 60, c1: 16})
display(s2_solved_subbed)
# values for slowing down ramp
beats_down_ramp = range(13, floor(16 / beatlength))
beattimecodes_down_ramp = [beatlength * i for i in beats_down_ramp]
display([i.n() for i in beattimecodes_down_ramp])
outbeats_down_ramp = [
    s2_solved_subbed.n(6, {t: i}, chop=True) for i in beattimecodes_down_ramp
]
for i in range(len(outbeats_down_ramp)):
    print(
        beats_down_ramp[i], outbeats_down_ramp[i], custom_round(outbeats_down_ramp[i])
    )  # beat values (from start of ramp)

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="JIHGjDRby1QH" outputId="79a6eaa9-349c-437a-9809-e80a35f0e9a6"
# total length of both ramps in seconds:
solveset(tempoeq2, t).args[0].subs({a: 96, b: 240, c: 20, b1: 60, c1: 16, s: 16}).n(6)

# %% [markdown] id="lc5ieYY8Ey2_"
# # New section

# %% colab={"base_uri": "https://localhost:8080/", "height": 0} id="7rdfHD4lKfef" outputId="0fabcf6c-1fe5-46f7-c3f0-0917c4b148e1"
# String accel section length in seconds
ramp(60, 180, 9 * 4, 9 * 4).doit() * 2

# %% [markdown] id="WU-kOg_dEI0Z"
# # Tempo relations in piece

# %% colab={"base_uri": "https://localhost:8080/", "height": 17} id="gNQjd66b3FG4" outputId="cf5c65d8-cc2e-49df-c950-c978204933dc"
from collections.abc import Iterable


def separate(item):
    if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
        return item
    else:
        return item, ""


# %% colab={"base_uri": "https://localhost:8080/", "height": 296} id="ZfCvs7-HEH_B" outputId="b888a0db-d696-49c5-abe0-25e44c994cb6"
tempolist_combined = (
    (t, "start"),
    t1,
    (t2, "wind accel + rit"),
    t3,
    t4,
    t5,
    t1,
    (t5, "middle"),
    t6,
)
tempolist, sections = zip(*(separate(i) for i in tempolist_combined))
tempo_equations = {
    t: t1 * 5 / 4,
    t1: 128,
    t2: t1 * 3 / 4,
    t3: t2 * 5 / 2,
    t4: t3 * 1 / 4,
    t5: t4 * 3,
    t6: t5 / 2,
}
print("equations:\n")
display(tempo_equations)
print("\nresultant tempi:", "\n------------------------------------")
for i in range(len(tempolist)):
    x = tempolist[i]
    print(x, "\t| ", N(x, 3, subs=tempo_equations), "\t| ", sections[i])

# %% [markdown] id="n_Qr0YHCWzKZ"
# # Middle Section

# %% colab={"base_uri": "https://localhost:8080/", "height": 364} id="0MdjDJsYWysk" outputId="c45b9493-46fa-48f0-ed06-617fa2b3d2e7"
# downwards ramp
middle_ramp_1_total_length = 5 + 4 + 4 + 5 + 4 + 3 + 4
middle_ramp_1_f = Eq(f(180, 90, middle_ramp_1_total_length, s, a), t)
display(middle_ramp_1_f)
middle_ramp_1 = middle_ramp_1_f.replace(f, ramp).doit()
print("length of one downwards ramp in seconds:")
middle_ramp_1_length_seconds = solveset(
    middle_ramp_1.subs({s: middle_ramp_1_total_length, a: 0}), t
).args[0]
display(middle_ramp_1_length_seconds.n(3))

print(
    "\nlength of a crotchet at 180bpm:\n\nbeat\t| length (beats)",
    "\n-----------------------------",
)
crotchet_in_seconds = S(60) / 180
crotchet_in_beats = solveset(middle_ramp_1.subs(t, crotchet_in_seconds), s).args[0] - a
beats_to_inspect = [
    0,
    middle_ramp_1_total_length * 0.25,
    middle_ramp_1_total_length * 0.5,
    middle_ramp_1_total_length * 0.75,
    middle_ramp_1_total_length - 1,
]
for location in (
    (i, crotchet_in_beats.n(3, {a: i}, chop=True)) for i in beats_to_inspect
):
    print(location[0], "\t| ", location[1])


print(
    "\n\nproportion\t| beat\t\t| time",
    "\n-----------------------------------------------",
)
for i in [0.25, 0.5, 0.75]:
    location_seconds = (i * middle_ramp_1_length_seconds).n(3)
    location = solveset(middle_ramp_1.subs({t: location_seconds, a: 0}), s).args[0].n(3)
    print(i, "\t\t| beat", location, "\t|", location_seconds, "seconds")
