# IMPORTANT
Install the Typer library before using! [get typer here](https://github.com/tiangolo/typer)

# Introduction
This is a Python script to generate random star systems. Use it for anything. As long as that 'anything' doesn't violate the GNU GPL v3.
# The Details

The script generates a star with random attributes and selects how many planets to generate (from 4 to 16).

Based on the star type and the generated attributes of a planet, it is assigned a habitability score (HabScore) which is used to weigh certain planet types depending on habitability.

## Penalties (HabScore reductions):
* Planet too close or too far to it's star.
* The type of star (OBAF).
## Rewards (HabScore increases):
* Planet is in the circumstellar habitable/goldilocks zone (CHZ).
* The type of star (GKM).
## Star types (+ rewards, - penalizes)
```
Star Type  Modifier
O          -4
B          -3
A          -2
F          -1
G          x3
K          x2
M          x1
```
# Command help
## legacy-stars (deprecated)
Old star system & planet generator. No longer available.

## legacy-planets (deprecated)
Old planet generator. No longer available.

## stars
Generate stars. Depending on the setting of `config.OUTPUT_FORMAT`, it will either output 2 JSON or CSV files named `planets` and `stars`.


## man (do not use)
`man` is a leftover relic of an older private version and will be removed soon.
