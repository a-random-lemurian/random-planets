# Copyright (c) 2021, Lemuria
# This code is licensed under the GNU GPL v3

from math import ceil
import random
import json
import string

# Initial 'seed', used to feed the script data to base it's generation off on.
SEED = json.load(open('seed.json', 'r'))

debug = False


class Calc():
    def star_make(star_name: str):
        """
        Return a set containing star attributes which you can pass to `hab_score` to get a habitability score.

        `spectral`: Star's spectral class.
        `temp_kelvin`: Star temperature in Kelvin.
        `mass`: Star's mass in solar masses (a star with mass 2SM has twice as much mass than the Sun)
        """

        # Fetch a random spectral type.
        spectral    = random.choice (SEED['star-types'])

        # Then, choose a random temperature and mass for the star.
        temp_kelvin = random.uniform(SEED['star-type-limits'][spectral]['min-temp'],SEED['star-type-limits'][spectral]['max-temp'])
        mass        = random.uniform(SEED['star-type-limits'][spectral]['min-mass'],SEED['star-type-limits'][spectral]['max-mass'])

        
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
        modifier = SEED['star-type-hab-modifiers'][(starType)]

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

        # The modifier is made a positive number, if it is negative at the
        # time of score calculation.
        if modifier > -1:
            modif = abs(modifier)                  
            score = dist_rating*modif*rand_modifier
        else:
            modif = abs(modifier) # Just in case.
            score = dist_rating/modif*rand_modifier
        if debug: # Debug mode, allows to check the 'chz'.
            return(f'{int(score)} / chz: min {min_chz}ls, max {max_chz}ls')
        else:
            return(int(score)) # Just return the HabScore.

    def choosePlanet(habScore: int):
        """Assign the planet a tier which will determine it's type"""
        if   habScore > 640:
            tier = 't5'
        elif habScore > 550:
            tier = 't4'
        elif habScore > 500:
            tier = 't3'
        elif habScore > 70:
            tier = 't2'
        else:
            tier = 't1'

        Planet_Type_chosen = random.choice(SEED['planet-types-2'][tier])

        return(Planet_Type_chosen)

# These two functions work quite similarly.
    
    def atmo_score(hab_score: int, planetType: str):
        atmo_modifier = SEED['planet-type-modifiers'][planetType]['atmo']
        atmo = hab_score * atmo_modifier / random.uniform(1.2000,1.4000)
        return(atmo)
    
    def res_score(hab_score: int, planetType: str):
        res_modifier = SEED['planet-type-modifiers'][planetType]['resource']
        res = hab_score * res_modifier / random.uniform(1.6000, 4.0000)
        return(res)

# Grants a planet two labels depending on their resource and atmosphere score.

    def atmo_tier(atmo_score: int):
        if atmo_score > 1200:
            return('Perfect')
        elif atmo_score > 700:
            return('Breathable')
        elif atmo_score > 450:
            return('Slightly unbreathable')
        elif atmo_score > 100:
            return('Deadly')
        else:
            return('Extremely deadly')

    def res_tier(res_score: int):
        if res_score > 900:
            return('Extremely mineral-rich')
        if res_score > 600:
            return('Mineral-rich')
        if res_score > 200:
            return('Normal')
        else:
            return('Poor')

# Gives the planet a radius in km. For reference, the Earth is roughly 20,000km in diameter.

    def radius(hab_score: int, planetType: str):
        size_modifier = SEED['planet-type-modifiers'][planetType]['size-modif']
        radius = size_modifier * random.uniform(1.3000000000000000000000000000000000000,
                                                3.4000000000000000000000000000000000000) * random.uniform(1.3000000000000000000000000000000000000,
                                                                                                          16243.4000000000000000000000000000000000000)
        return(radius)




class Name():
    
    # Functions for assigning names to stars.
    # LACOS doesn't mean anything.
    class Components():
        def numbers(kk:int):
            return(''.join(random.choices(string.digits,k=kk)))

        def lowercase(kk:int):
            return(''.join(random.choices(string.ascii_lowercase,k=kk)))
    
    class Star():
        def lacos():
            # Not a real star catalog.
            region =     Name.Components.numbers(3)
            quadrant_x = Name.Components.numbers(2)
            quadrant_y = Name.Components.numbers(2)
            quadrant_z = Name.Components.numbers(2)
            star_num =   Name.Components.numbers(5)
            return(f'LACOS1.r{region}.qx{quadrant_x}-y{quadrant_y}-z{quadrant_z}.s{star_num}')
        
        def earth_catag():
            # Not a real star catalog.
            star_num = Name.Components.numbers(16)
            return(f'ECAOAS {star_num}')

        def mesulos():
            # Not a real star catalog.
            star_letter = Name.Components.lowercase(4)
            star_num    = Name.Components.numbers(8)
            return(f'Mesulos {star_letter}-{star_num}')

        def meaningless_1():
            # Component star names which ed_style_2 can use.
            component_1 = random.choice(SEED['names']['meaningless-1']['component_1'])
            component_2 = random.choice(SEED['names']['meaningless-1']['component_2'])
            return(f'{component_1}{component_2}') 

        def ed_style():
            # Not a real star catalog.
            star_letter_1 = Name.Components.lowercase(2)
            star_letter_2 = Name.Components.lowercase(2)
            star_number = Name.Components.numbers(6)
            return(f'Arrolix {star_letter_1}-{star_letter_2} {star_number}')

        def ed_style_2():
            # Not a real star catalog. Relies on meaningless_1 for a component of it's star names.
            component_1 = random.choice(
                SEED['names']['meaningless-1']['component1'])
            component_2 = random.choice(
                SEED['names']['meaningless-1']['component2'])
            comp = f'{component_1}{component_2}'
            star_letter_1 = Name.Components.lowercase(2)
            star_letter_2 = Name.Components.lowercase(2)
            star_number = Name.Components.numbers(6)
            return(f'{comp} {star_letter_1}-{star_letter_2} {star_number}')
            

    class Choose():
        def Choose(nameType: str):
            if   nameType.lower().strip() == 'lacop':
                return(Name.Star.lacos())
            
            elif nameType.lower().strip() == 'ecaoas':
                return(Name.Star.earth_catag())

            elif nameType.lower().strip() == 'mesulos':
                return(Name.Star.mesulos())

            elif nameType.lower().strip() == 'ed_style_1':
                return(Name.Star.ed_style())

            elif nameType.lower().strip() == 'ed_style_2':
                return(Name.Star.ed_style_2())

# for xp in range(250):
#     p = + 100
#     print((str(Calc.hab_score(1033, p, 'G-4')))+' /'+(str(p)))
