# Copyright (c) 2021, Lemuria
# This code is licensed under the GNU GPL v3

from math import ceil
import random
import json
import string

HAB_MODIFIERS = json.load(open('seed.json', 'r'))

debug = False


class Calc():
    def star_make(star_name: str):
        """
        Return a set containing star attributes which you can pass to `hab_score` to get a habitability score.

        `spectral`: Star's spectral class.
        `temp_kelvin`: Star temperature in Kelvin.
        `mass`: Star's mass in solar masses (a star with mass 2SM has twice as much mass than the Sun)
        """

        spectral    = random.choice (HAB_MODIFIERS['star-types'])
        temp_kelvin = random.uniform(HAB_MODIFIERS['star-type-limits'][spectral]['min-temp'],HAB_MODIFIERS['star-type-limits'][spectral]['max-temp'])
        mass        = random.uniform(HAB_MODIFIERS['star-type-limits'][spectral]['min-mass'],HAB_MODIFIERS['star-type-limits'][spectral]['max-mass'])
        min_chz     = temp_kelvin * mass / 10 * 2
        max_chz     = min_chz * 4

        output = {'name':star_name,'spectral': spectral, 'temp_kelvin': temp_kelvin, 'mass': mass, 'min-chz': min_chz, 'max-chz': max_chz}
        return(output)
    def hab_score(distanceFromStar: int, star: set):
        
        """
        Calculate a habitability rating from 0-100 based on attributes given to the function. Ignores gravitational pull.

        ### `distanceFromStar`
        Distance of the planet from the star in light seconds (1 ls = ~299,758km)
        """
        # Get initial variables to base the calculations off on.
        starType = star['spectral']
        modifier = HAB_MODIFIERS['star-type-hab-modifiers'][(starType)]

        min_chz = star['min-chz']
        max_chz = star['max-chz']
        # Define the 'goldilocks zone' or circumstellar habitable zone
        # of the star type.
        # CHZ = circumstellar habitable zone (more commonly the goldilocks zone)
        # distance measured in light-seconds (Earth is roughly 480 ls from the Sun)
        # 1 lightsecond:
        # 299792.458 km
        # Penalize or reward the HabScore based on the orbital radius of the planet.
        # Penalize if planet is too close to star.
        if distanceFromStar > min_chz:
            if distanceFromStar < max_chz:
                modifier += random.uniform(0.30000, 1.50000)
            else:
                do_nothing = 0
        else:
            # For every 50 ls the planet is too close, add to the modifier.
            modifier += min_chz - distanceFromStar / 50
        if distanceFromStar > max_chz:
            # For every 100 ls the planet is too far, add to the modifier.
            modifier -= distanceFromStar - max_chz / 100
        # Penalize if planet is too far away.
        # Add positive or punitive modifier based on star type.
        dist_rating = distanceFromStar / modifier
        rand_modifier = random.uniform(0.00000000, 1.50000000)
        if modifier > -1:
            modif = abs(modifier)
            score = dist_rating*modif*rand_modifier
        else:
            modif = abs(modifier)
            score = dist_rating/modif*rand_modifier
        if debug:
            return(f'{int(score)} / chz: min {min_chz}ls, max {max_chz}ls')
        else:
            return(int(score))
    def choosePlanet(habScore: int):
        # Assign the planet a tier which will determine it's type.
        if   habScore > 600:
            tier = 't5'
        elif habScore > 520:
            tier = 't4'
        elif habScore > 300:
            tier = 't3'
        elif habScore > 100:
            tier = 't2'
        else:
            tier = 't1'

        Planet_Type_chosen = random.choice(HAB_MODIFIERS['planet-types-2'][tier])

        return(Planet_Type_chosen)
class Name():
    def star():
        region =     ''.join(random.choices(string.digits, k=3))
        quadrant_x = ''.join(random.choices(string.digits, k=2))
        quadrant_y = ''.join(random.choices(string.digits, k=2))
        quadrant_z = ''.join(random.choices(string.digits, k=2))
        star_num =   ''.join(random.choices(string.digits, k=5))
        return(f'LACOS1.r{region}.qx{quadrant_x}-y{quadrant_y}-z{quadrant_z}.s{star_num}')

# for xp in range(250):
#     p = + 100
#     print((str(Calc.hab_score(1033, p, 'G-4')))+' /'+(str(p)))
