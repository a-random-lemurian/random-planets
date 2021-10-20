# IMPORTANT
Install the Typer library before using! [get typer here](https://github.com/a-random-lemurian/random-planets/edit/master/README.md)

# Introduction
This is a Python script to generate random star systems. Use it for anything.
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
