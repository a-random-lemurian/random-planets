# Copyright (c) 2021, Lemuria
# This code is licensed under the GNU GPL v3


from typing import Optional
from click.exceptions import FileError
import typer
import json
import random
import csv
import planetcalcs as pcal
import os
import uuid
import tqdm

app = typer.Typer()

CONFIG = json.load(open('seed.json'))
FILE_FORMAT = CONFIG['config.OUTPUT_FORMAT']

PLANET_TYPES = CONFIG['planet-types']
GOVERNMENTS  = CONFIG['governments']

if FILE_FORMAT == 'json':
    do_nothing = 0
elif FILE_FORMAT == 'csv':
    do_nothing = 0
else:
    raise FileError(f'File format {FILE_FORMAT} not supported, please use json/csv.')

import csv

# All the good stuff.

@app.command()
def stars(starstomake: int,
          format: Optional[str] = typer.Argument(FILE_FORMAT),
          naming: Optional[str] = typer.Argument(CONFIG['config.STAR_NAMES']),
          ):
    
    stars   = []
    planets = []

    if naming.lower().strip() == 'meaningless_1':
        print(f'''
HOLD UP, WAIT A MINUTE!

The Meaningless-1 name set does not have that many names.
Using it might result in duplicate names. Do you want to use it?

[Y]es / [N]o
              ''')
        x = input(f'> ')
        if x.lower().strip() == 'y':
            pass
        else:
            print('Aborted generation.')
            exit()

    if format.lower().strip() == 'csv':

        dirname = f'query-{uuid.uuid4()}'

        os.mkdir(f'star-queries/{dirname}/')

        csv_planet = open(f'star-queries/{dirname}/planets.csv','x')
        csv_star   = open(f'star-queries/{dirname}/stars.csv','x')

        csv_planet.write('name,star,planetType,habScore,atmoScore,resScore,atmoTier,resTier,radius\n')
        csv_star.write('name,spectral,temp_kelvin,mass,min_chz,max_chz\n')
    
    for i in tqdm.tqdm(range(starstomake),desc='generating planets & stars'):
        
        star_name = pcal.Name.Choose.Choose(naming)
        star = pcal.Calc.star_make(star_name)

        if format.lower().strip() == 'csv':
            csv_star.write(str(star['name'])+','+str(star['spectral'])+','+str(star['temp_kelvin'])+','+str(star['mass'])+','+str(star['min-chz'])+','+str(star['max-chz'])+'\n')
            
        stars.append(star)
        
        dfs = random.randint(230,450) # Distance from star
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

            if format.lower().strip() == 'json':
                planets.append(planet)

            if format.lower().strip() == 'csv':
                csv_planet.write(planet_name+','+star_name+','+planet_type+','+str(habScore)+','+str(atmoScore)+','+str(resScore)+','+atmoTier+','+resTier+','+str(radius)+'\n')
            
    dirname = f'query-{uuid.uuid4()}'
    
    if format.lower().strip() == 'json':
        
        os.mkdir(f'star-queries/{dirname}')
    
        for i in tqdm.tqdm(range(1),desc='Writing stars to disk'):
            with open(f'star-queries/{dirname}/stars.json','x') as f_stars:
                json.dump(stars, f_stars)
                print('Star data written to disk.')
                
        for i in tqdm.tqdm(range(1),desc='Writing planets to disk'):
            with open(f'star-queries/{dirname}/planets.json','x') as f_planets:
                json.dump(planets, f_planets)
                print('Planet data written to disk.')

    else:
        print('DONE')

if __name__ == "__main__":
    app()
