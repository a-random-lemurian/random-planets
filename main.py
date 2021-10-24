# Copyright (c) 2021, Lemuria
# This code is licensed under the GNU GPL v3


from typing import Optional
import typer
import json
import random
import rich
import secrets
import planetcalcs as pcal
import os
import uuid
import tqdm

app = typer.Typer()

CONFIG = json.load(open('seed.json'))
FILE_FORMAT = CONFIG['config.OUTPUT_FORMAT']

PLANET_TYPES = CONFIG['planet-types']
GOVERNMENTS  = CONFIG['governments']

PLANET_SURVEYS = CONFIG['planet-surveys']
STAR_SURVEYS   = CONFIG['star-surveys']

if FILE_FORMAT == 'json':
    do_nothing = 0
elif FILE_FORMAT == 'csv':
    do_nothing = 0
else:
    raise Exception(f'File format {FILE_FORMAT} not supported, please use json/csv.')

import csv

# All the good stuff.

@app.command()
def stars(starstomake: int):
    
    stars   = []
    planets = []
    
    for i in tqdm.tqdm(range(starstomake),desc='generating planets & stars'):
        
        star_name = pcal.Name.Choose.Choose()
        star = pcal.Calc.star_make(star_name)
        stars.append(star)
        
        dfs = random.randint(230,450)
        for pl in range(random.randint(4,16)):
            habScore    = pcal.Calc.hab_score(distanceFromStar=dfs,star=star)
            planet_type = pcal.Calc.choosePlanet(int(habScore))
            planet_name = f'{star_name}.p{pl}'
            
            dfs += random.randint(65,150)*(random.uniform(0.00000000,1.40000000))
            atmoScore = pcal.Calc.atmo_score(hab_score=habScore,planetType=planet_type)
            resScore  = pcal.Calc.res_score(hab_score=habScore,planetType=planet_type)
            radius    = pcal.Calc.radius(hab_score=habScore,planetType=planet_type)

            atmoTier = pcal.Calc.atmo_tier(habScore)
            resTier  = pcal.Calc.res_tier(habScore)
            planet = {
                'name':planet_name,
                'star':star_name,
                'planetType':planet_type,
                'habScore':habScore,
                'atmoScore':atmoScore,
                'resScore':resScore,
                'atmoTier':atmoTier,
                'resTier':resTier,
                'radius':radius
                    }
            planets.append(planet)
    dirname = f'query-{uuid.uuid4()}'
    os.mkdir(f'star-queries/{dirname}')
    for i in tqdm.tqdm(range(1),desc='Writing stars to disk'):
        with open(f'star-queries/{dirname}/stars.json','x') as f_stars:
            json.dump(stars, f_stars)
            print('Star data written to disk.')
    for i in tqdm.tqdm(range(1),desc='Writing planets to disk'):
        with open(f'star-queries/{dirname}/planets.json','x') as f_planets:
            json.dump(planets, f_planets)
            print('Planet data written to disk.')
    print('DONE')

if __name__ == "__main__":
    app()
