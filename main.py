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
    
    for i in range(starstomake):
        
        star_name = pcal.Name.star()
        star = pcal.Calc.star_make(star_name)
        stars.append(star)
        
        dfs = random.randint(230,450)
        for pl in range(random.randint(4,16)):
            habScore    = pcal.Calc.hab_score(distanceFromStar=dfs,star=star)
            planet_type = pcal.Calc.choosePlanet(int(habScore))
            planet_name = f'{star_name}.p{pl}'
            
            dfs += random.randint(65,150)*(random.uniform(0.00000000,1.40000000))
            
            planet = {'habScore':habScore, 'planetType':planet_type, 'name':planet_name, 'star':star_name}
            planets.append(planet)
            
    print('Stars generated. Now writing star data to disk.')
    
    dirname = f'query-{uuid.uuid4()}'
    
    os.mkdir(f'star-queries/{dirname}')
    with open(f'star-queries/{dirname}/stars.json','x') as f_stars:
        json.dump(stars, f_stars)
        print('Star data written to disk.')
        
    with open(f'star-queries/{dirname}/planets.json','x') as f_planets:
        json.dump(planets, f_planets)
        print('Planet data written to disk.')
        
    print('DONE')

if __name__ == "__main__":
    app()
